#!/usr/bin/env python
# coding:utf-8
"""
@license: Apache License2
@file: wrapper.py
@time: 2022-08-19 02:05:07.467170
@project: mnist
@project: ./
"""
import os.path
from threading import Thread
from aiges.core.types import *
try:
    from aiges_embed import ResponseData, Response, DataListNode, DataListCls, SessionCreateResponse, callback, init_rq  # c++
except:
    from aiges.dto import Response, ResponseData, DataListNode, DataListCls, SessionCreateResponse, callback, init_rq

from aiges.sdk import WrapperBase, \
    ImageBodyField, \
    StringBodyField, StringParamField

try:
    from aiges_embed import callback_metric
except:
    callback_metric=None

from aiges.utils.log import log, getFileLogger
import threading
import torch

DataNone = -1
DataBegin = 0  # 首数据
DataContinue = 1  # 中间数据
DataEnd = 2  # 尾数据
def transform_stream_state(cur_state:int, print_len:int, text):
    if cur_state == DataNone and text and print_len > 0:
        return DataBegin
    elif cur_state == DataBegin and text and print_len > 0:
        return DataContinue
    return cur_state


# 定义模型的超参数和输入参数
class UserRequest(object):
    input1 = StringBodyField(key="text", value='''这道试题类型属于 判断推理，类比推理，逻辑关系，逻辑关系-并列关系中的一种。 试题: QQ：微信：FaceBook
 请从下列选项选出一个最恰当的答案: A. 手提电脑：打印机：数字电视
B. 微博：论坛：互联网
C. 人民日报：工人日报：光明日报
D. 医生：护士：患者
'''.encode('utf-8'))
    input2 = StringParamField(key="atp_patch_id", value="179387562041344")


# 定义模型的输出参数
class UserResponse(object):
    accept1 = StringBodyField(key="result")


# 定义服务推理逻辑
class Wrapper(WrapperBase):
    serviceId = "chinese_alpaca"
    version = "v1"
    requestCls = UserRequest()
    responseCls = UserResponse()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filelogger = None
        self.lock = threading.Lock()

    def wrapperInit(self, config: {}) -> int:
        logger = log

        logger.info("Initializing ...")
        from transformers import LlamaTokenizer, LlamaForCausalLM,AutoModelForCausalLM
        tokenizer_path = os.environ.get("TOKENIZER_PATH")
        model_path = os.environ.get("FULL_MODEL_PATH")
        infer_type = os.environ.get("INFER_TYPE")
        if not model_path or not tokenizer_path :
            log.error("should have environ(TOKENIZER_PATH,FULL_MODEL_PATH)")
            return -1
        
        def load_model_tokenizer(model_path, tokenizer_path):
            load_type = torch.float16
            tokenizer = LlamaTokenizer.from_pretrained(tokenizer_path)

            if (len(tokenizer)) == 55296: #v2 49954:v1
                from ailab.utils.attn_and_long_ctx_patches import apply_attention_patch, apply_ntk_scaling_patch
                apply_attention_patch(use_memory_efficient_attention=True)
                apply_ntk_scaling_patch(1.0)

            model = LlamaForCausalLM.from_pretrained(
                model_path,
                load_in_8bit=False,
                torch_dtype=load_type,
                low_cpu_mem_usage=True,
                device_map='auto',
                )

            model_vocab_size = model.get_input_embeddings().weight.size(0)
            tokenzier_vocab_size = len(tokenizer)
            logger.info(f"Vocab of the base model: {model_vocab_size}")
            logger.info(f"Vocab of the tokenizer: {tokenzier_vocab_size}")
            if model_vocab_size!=tokenzier_vocab_size:
                assert tokenzier_vocab_size > model_vocab_size
                logger.info("Resize model embeddings to fit tokenizer")
                model.resize_token_embeddings(tokenzier_vocab_size)
            return model,tokenizer

        self.base_model, self.base_tokenizer = load_model_tokenizer(model_path,tokenizer_path)
        self.filelogger = getFileLogger()
        self.infer_type = infer_type

        session_total = config.get("common.lic", 0)
        if session_total > 0:
            init_rq()
            self.session.init_wrapper_config(config)
            self.session.init_handle_pool("thread", 1, MyReqDataThread)
        return 0


    def evaluate(self, instruction: str, model , tokenizer, stream_cls) -> str:
        # The prompt template below is taken from llama.cpp
        # and is slightly different from the one used in training.
        # But we find it gives better results
        if (len(tokenizer)) == 49954:
            prompt_input = (
                "Below is an instruction that describes a task. "
                "Write a response that appropriately completes the request.\n\n"
                "### Instruction:\n\n{instruction}\n\n### Response:\n\n"
            )
            def generate_prompt(instruction, input=None):
                if input:
                    instruction = instruction + '\n' + input
                return prompt_input.format_map({'instruction': instruction})
        elif (len(tokenizer)) == 55296:
            prompt_input = (
                "[INST] <<SYS>>\n"
                "{system_prompt}\n"
                "<</SYS>>\n\n"
                "{instruction} [/INST]"
            )
            DEFAULT_SYSTEM_PROMPT = """You are a helpful assistant. 你是一个乐于助人的助手。"""
            def generate_prompt(instruction, system_prompt=DEFAULT_SYSTEM_PROMPT):
                return prompt_input.format_map({'instruction': instruction,'system_prompt': system_prompt})

        with torch.no_grad():
            input_text = generate_prompt(instruction=instruction)
            inputs = tokenizer(input_text,return_tensors="pt")  #add_special_tokens=False ?
            input_ids = inputs["input_ids"].to(model.device)
            attention_mask = inputs['attention_mask'].to(model.device)

            from transformers import TextIteratorStreamer
            streamer = TextIteratorStreamer(tokenizer, timeout=60.0, skip_prompt=True, skip_special_tokens=True)
            gen_kwargs = {
                "input_ids": input_ids,
                "streamer": streamer,
                "attention_mask":attention_mask,
                "eos_token_id":tokenizer.eos_token_id,
                "pad_token_id":tokenizer.pad_token_id,
                "temperature" :0.2,
                "top_k":40,
                "top_p":0.9,
                "do_sample":True,
                "num_beams":1,
                "repetition_penalty":1.3,
                "max_new_tokens":400,
            }

            thread = Thread(target=model.generate, kwargs=gen_kwargs)
            thread.start()

            response = ""
            cur_state = DataNone
            for new_text in streamer:
                if stream_cls:
                    cur_state = transform_stream_state(cur_state, streamer.print_len, new_text)
                    stream_cls.on_stream_infer(new_text,cur_state)
                response += new_text
            if stream_cls and cur_state == DataContinue:
                stream_cls.on_stream_infer('.',DataEnd)
            return response

    def _base_model_inference(self, reqData: DataListCls, stream_cls) -> str:
        tokenizer = self.base_tokenizer
        model = self.base_model
            
        input_text = reqData.get("text").data.decode('utf-8')
        self.filelogger.info("got input_text , %s" % input_text)

        return self.evaluate(input_text,model,tokenizer, stream_cls)

    def _full_model_infence(self, reqData: DataListCls, stream_cls) -> str:
        tokenizer = self.base_tokenizer
        model = self.base_model

        instruction = reqData.get("text").data.decode('utf-8')
        return self.evaluate(instruction,model,tokenizer,stream_cls)

    def wrapperOnceExec(self, params: {}, reqData: DataListCls, usrTag:str="",persId: int = 0) -> Response:
        self.filelogger.info("got reqdata , %s" %( reqData.list))

        self.lock.acquire()
        if self.infer_type == 'base':
            result = self._base_model_inference(reqData,None)
        else:
            result = self._full_model_infence(reqData,None)
        self.lock.release()
        res = Response()
        if not result:
            self.filelogger.info("#####")
            return res.response_err(100)
        self.filelogger.info("got result , %s" % result)
        # 使用Response封装result
        resd = ResponseData()
        resd.key = "result"
        resd.setDataType(DataText)
        resd.status = Once
        resd.setData(result.encode("utf-8"))
        print("###")
        self.filelogger.info("###")

        self.filelogger.info(result)
        if callback_metric:
            ret = callback_metric(usrTag, "business.total", 1)
            self.filelogger.info("calc +1 ret: %d"%ret)
        res.list = [resd]
        return res

    def wrapperFini(cls) -> int:
        return 0

    def wrapperError(cls, ret: int) -> str:
        if ret == 100:
            return "not get result...."
        return ""
    
    def wrapperWrite(self, handle: str, req: DataListCls, sid: str) -> int:
        """
        会话模式下: 上行数据写入接口
        :param handle: 会话handle 字符串
        :param req:  请求数据结构
        :param sid:  请求会话ID
        :return:
        """
        _session = self.session.get_session(handle=handle)
        if _session == None:
            log.info("can't get this handle:" % handle)
            return -1
        _session.in_q.put(req)
        return 0
    
    def wrapperCreate(self, params: {}, sid: str, persId: int = 0) -> SessionCreateResponse:
        s = SessionCreateResponse()
        # 这里是取 handle
        handle = self.session.get_idle_handle()
        if not handle:
            log.info('get_idle_handle failed')
            s.error_code = -1
            s.handle = ""
            return s
        _session = self.session.get_session(handle=handle)
        if _session == None:
            log.info("can't create this handle:" % handle)
            return -1
        params['wrapper'] = self
        _session.setup_sid(sid)
        _session.setup_params(params)
        _session.setup_callback_fn(callback)
        s = SessionCreateResponse()
        s.handle = handle
        s.error_code = 0
        return s

    def wrapperDestroy(self, handle: str) -> int:
        _session = self.session.get_session(handle=handle)
        if _session == None:
            log.info("can't get this handle:" % handle)
            return -1
        self.session.set_idle_session(handle)
        return 0

    '''
        此函数保留测试用，不可删除
    '''

    def wrapperTestFunc(cls, data: [], respData: []):
        pass


from aiges.stream import StreamHandleThread
import queue
class MyReqDataThread(StreamHandleThread):
    def __init__(self, session_thread, in_q, out_q):
        super().__init__(session_thread, in_q, out_q)
        self.setDaemon(False)
        self.is_stopping = False

    def stop(self):
        self.is_stopping = True

    def on_stream_infer(self, text, state):
        if text and state != DataNone:
            res= Response()
            # 使用Response封装result
            resd = ResponseData()
            resd.key = "result"
            resd.setDataType(DataText)
            resd.status = state
            resd.setData(text.encode("utf-8"))
            res.list = [resd]
            self.session_thread.callback_fn(res, self.session_thread.sid)
            if resd.status == DataEnd:
                self.session_thread.reset()

    def infer(self, reqData: DataListCls):
        params = self.session_thread.params
        wrapper_cls = params['wrapper']
        if wrapper_cls.infer_type == 'base':
            wrapper_cls._base_model_inference(reqData,self)
        else:
            wrapper_cls._full_model_infence(reqData,self)

    def run(self):
        while not self.is_stopping:
            try:
                req = self.in_q.get(timeout=5)
                self.infer(req)
            except queue.Empty as e:
                pass

if __name__ == '__main__':
    m = Wrapper()
    m.run()
    #print(m.schema())


