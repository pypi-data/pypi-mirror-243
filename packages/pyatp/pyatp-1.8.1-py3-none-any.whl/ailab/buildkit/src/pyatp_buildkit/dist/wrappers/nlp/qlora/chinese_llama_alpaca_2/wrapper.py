#!/usr/bin/env python
# coding:utf-8
"""
@license: Apache License2
@file: wrapper.py
@time: 2022-08-19 02:05:07.467170
@project: mnist
@project: ./
"""
from threading import Thread
import os.path
from aiges.core.types import *
try:
    from aiges_embed import ResponseData, Response, DataListNode, DataListCls, DataListCls, SessionCreateResponse, callback, init_rq  # c++
except:
    from aiges.dto import Response, ResponseData, DataListNode, DataListCls, DataListCls, SessionCreateResponse, callback, init_rq

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
import copy
from peft import PeftModel
TEST=1

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
    serviceId = "effcient"
    version = "v1"
    requestCls = UserRequest()
    responseCls = UserResponse()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filelogger = None
        self.model = None
        self.tokenizer = None
        self.patch_id_map = {}
        self.first_load_lora = True
        self.lock = threading.Lock()

    def wrapperInit(self, config: {}) -> int:
        logger = log

        logger.info("Initializing ...")
        from transformers import LlamaTokenizer, LlamaForCausalLM,AutoModelForCausalLM,AutoConfig,BitsAndBytesConfig
        self.pretrained_name = os.environ.get("PRETRAINED_MODEL_NAME")

        if not self.pretrained_name:
            log.error("should have environ(PRETRAINED_MODEL_NAME,MODEL_PATH(lora weight dir）,TOKENIZER_PATH)")
            return -1


        tokenizer_path = os.environ.get("TOKENIZER_PATH")
        base_model_path = os.environ.get("FULL_MODEL_PATH")
        finetune_type = os.environ.get("FINETUNE_TYPE",'lora')
            
        if not os.path.isdir(base_model_path):
            log.error(f"not find the base_model in {base_model_path}")
            return -1
        if not base_model_path or not tokenizer_path:
            log.error("should have environ(FULL_MODEL_PATH,(base or full ）,TOKENIZER_PATH)")
            return -1

        tokenizer = LlamaTokenizer.from_pretrained(tokenizer_path)

        if (len(tokenizer)) == 55296: #v2 49954:v1
            from ailab.utils.attn_and_long_ctx_patches import apply_attention_patch, apply_ntk_scaling_patch
            apply_attention_patch(use_memory_efficient_attention=True)
            apply_ntk_scaling_patch(1.0)
        if finetune_type == 'qlora':
            model_config = AutoConfig.from_pretrained(base_model_path,trust_remote_code=True)
            base_model = AutoModelForCausalLM.from_pretrained(
                base_model_path,
                config=model_config,
                torch_dtype=torch.float16,
                low_cpu_mem_usage=True,
                load_in_4bit=True,
                device_map="auto", 
                trust_remote_code=True,
                quantization_config= BitsAndBytesConfig(
                    load_in_4bit=True,
                    bnb_4bit_compute_dtype=torch.float16,
                    bnb_4bit_use_double_quant=True,
                    bnb_4bit_quant_type='nf4'))
        else:
            base_model = LlamaForCausalLM.from_pretrained(
                base_model_path,
                load_in_8bit=False,
                torch_dtype=torch.float16,
                low_cpu_mem_usage=True,
                device_map='auto',
                )

        model_vocab_size = base_model.get_input_embeddings().weight.size(0)
        tokenzier_vocab_size = len(tokenizer)
        logger.info(f"Vocab of the base model: {model_vocab_size}")
        logger.info(f"Vocab of the tokenizer: {tokenzier_vocab_size}")
        if model_vocab_size!=tokenzier_vocab_size:
            assert tokenzier_vocab_size > model_vocab_size
            logger.info("Resize model embeddings to fit tokenizer")
            base_model.resize_token_embeddings(tokenzier_vocab_size)

        self.model = base_model
        self.tokenizer = tokenizer
        self.filelogger = getFileLogger()

        session_total = config.get("common.lic", 0)
        if session_total > 0:
            init_rq()
            self.session.init_wrapper_config(config)
            self.session.init_handle_pool("thread", 1, MyReqDataThread)
        return 0


    def checkValidLora(self, pretrained_name, lora_path):
        import json
        confjson = "adapter_config.json"
        files = os.listdir(lora_path)
        if not os.path.isdir(lora_path):
            msg = "not find  %s"%lora_path
            log.error(msg)
            return False, msg
        if not confjson in files:
            msg = "%s doesnt have file adapter_config.json" % lora_path
            log.error(msg)
            return False, msg
        fp = open(os.path.join(lora_path, confjson),'rb')
        conf = json.load(fp)
        base_model_path = conf.get("base_model_name_or_path","")
        if not base_model_path:
            msg = "config json not contains base_model_name_or_path...c=" % lora_path
            log.error(msg)
            return False, msg
        user_pretrained_name = os.path.basename(base_model_path)
        if pretrained_name != user_pretrained_name.strip():
            msg = f"current runntime model is {pretrained_name}, but you pass the {user_pretrained_name}, Error"
            log.error(msg)
            return False, msg
        else:
            return True, "Check Success..."

    def testLoad(self,patch_id):
        lora_weight_path = "/home/.atp/lora_weight/"
        lora_weight_path = os.path.join(lora_weight_path, str(patch_id))
        if self.first_load_lora == True:
            self.model = PeftModel.from_pretrained(self.model, lora_weight_path, adapter_name=patch_id)
            self.first_load_lora = False
        else:
            self.model.load_adapter(lora_weight_path, patch_id)
        self.model.eval()
        self.patch_id_map[patch_id] = (patch_id,lora_weight_path)
    def wrapperLoadRes(self, reqData: DataListCls, patch_id) -> int:
        if patch_id in self.patch_id_map:
            log.warn("patch_id has exist.Please first to UnloadRes")
            return 0
        lora_weight_path = "/home/.atp/lora_weight/"
        lora_weight_path = os.path.join(lora_weight_path, str(patch_id))
        #if os.path.exists(lora_weight_path):
        #    log.error("zip file has exist.Please first to UnloadRes")
        #    return -1

        import io
        import zipfile
        byte_stream = io.BytesIO(reqData.list[0].data)
        # 解压缩 zip 文件到指定目录
        with zipfile.ZipFile(byte_stream, 'r') as zip_ref:
            zip_ref.extractall(lora_weight_path)

        if not TEST:
            valid, msg = self.checkValidLora(self.pretrained_name, lora_weight_path)
            if not valid:
                return -1
            log.info(msg)

        if self.first_load_lora == True:
            self.model = PeftModel.from_pretrained(self.model, lora_weight_path, adapter_name=patch_id)
            self.first_load_lora = False
        else:
            self.model.load_adapter(lora_weight_path, patch_id)
        self.model.eval()
        self.patch_id_map[patch_id] = (patch_id,lora_weight_path)
        return 0

    def wrapperUnloadRes(self, patch_id: int) -> int:
        if patch_id not in self.patch_id_map:
            log.error("patch_id not exist")
            return 0
        lora_weight_path = self.patch_id_map[patch_id][1]
        if not os.path.exists(lora_weight_path):
            log.error("lora weigth path not exist")
            return 0
        import shutil
        shutil.rmtree(lora_weight_path)
        del self.patch_id_map[patch_id]
        return 0

    def evaluate(self, instruction: str, model , tokenizer, adapter, stream_cls) -> str:
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

    def _base_model_inference(self, reqData: DataListCls, adapter_name, stream_cls) -> str:
        tokenizer = self.tokenizer
        model = self.model

        if hasattr(model, 'disable_adapter'):
            with model.disable_adapter():
                input_text = reqData.get("text").data.decode('utf-8')
                self.filelogger.info("got input_text , %s" % input_text)
                return self.evaluate(input_text,model,tokenizer, adapter_name, stream_cls)
        else:
            input_text = reqData.get("text").data.decode('utf-8')
            self.filelogger.info("got input_text , %s" % input_text)
            return self.evaluate(input_text,model,tokenizer, adapter_name, stream_cls)

    def _lora_model_infence(self, reqData: DataListCls, adapter_name, stream_cls) -> str:
        if adapter_name not in self.patch_id_map:
            log.error(f"resid not exist,adapter_name {adapter_name},patch_id_map {self.patch_id_map}")
            return ""
        tokenizer = self.tokenizer
        lora_weight = self.patch_id_map[adapter_name][1]
        model = self.model
        model.load_adapter(lora_weight,adapter_name)
        model.set_adapter(str(adapter_name))

        instruction = reqData.get("text").data.decode('utf-8')
        return self.evaluate(instruction,self.model,tokenizer,adapter_name, stream_cls)

    def wrapperOnceExec(self, params: {}, reqData: DataListCls, usrTag:str="",persId: int = 0) -> Response:
        patch_id = params.get("atp_patch_id", 0)
        self.filelogger.info("got reqdata , %s, patch_ID %s" %( reqData.list, patch_id))

        self.lock.acquire()
        if patch_id == 0 or patch_id == "0":
            result = self._base_model_inference(reqData, "0", None)
        else:
            result = self._lora_model_infence(reqData, patch_id, None)
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
        params['patch_id'] = persId
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

    def run_once(self):
        # 1. 模拟调用初始化引擎
        #  传入配置当前模拟为空
        self.wrapperInit(self.config)
        self.testLoad("179387562041344")

        try:
            # 2. 准备wrapperOnceExec需要的数据
            inputs_fields, inputs_body = self._parse_inputs()

            params_fields, required_params = self._parse_params()
            params = self.params_test_values
            reqData = []
            reqData.append(self.inputs_test_values)
            req = DataListCls()
            tmp = []
            for key, value in self.inputs_test_values.items():
                node = DataListNode()
                node.key = key
                node.data = value
                node.len = len(value)
                typeStr = inputs_fields[key]["dataType"]
                node.type = 0
                tmp.append(node)

            req.list = tmp
            # 3. 模拟调用 exec，并返回数据
#            response = self.wrapperOnceExec(params, req)
            params['atp_patch_id'] = '0'
            response = self.wrapperOnceExec(params, req)
            params['atp_patch_id'] = '179387562041344'
            response = self.wrapperOnceExec(params, req)
            if self.check_resp(response):
                log.info("wrapper.py has been verified... Congratulations ...!")
            else:
                log.error("Sorry, Please Check The Log Output Above ...")
        except Exception as e:
            # 4. 模拟检查 wrapperOnceExec返回
            log.error(e)
            self.wrapperError(-1)

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
        patch_id = params['patch_id']
        if patch_id == 0 or patch_id == "0":
            wrapper_cls._base_model_inference(reqData, "0", self)
        else:
            wrapper_cls._lora_model_infence(reqData, patch_id, self)

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



