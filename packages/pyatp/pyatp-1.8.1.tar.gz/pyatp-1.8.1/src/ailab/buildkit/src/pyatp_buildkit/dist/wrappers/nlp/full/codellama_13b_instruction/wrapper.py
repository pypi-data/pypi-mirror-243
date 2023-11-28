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
import threading
from threading import Thread
from aiges.core.types import *
try:
    from aiges_embed import ResponseData, Response, DataListNode, DataListCls, SessionCreateResponse, callback, init_rq  # c++
except:
    from aiges.dto import Response, ResponseData, DataListNode, DataListCls, SessionCreateResponse, callback, init_rq

from aiges.sdk import WrapperBase, \
    ImageBodyField, \
    StringBodyField, StringParamField
from aiges.utils.log import log, getFileLogger
from transformers import TextIteratorStreamer
TEST=0

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
    input1 = StringBodyField(key="text", value=b"I have a problem with my iphone that needs to be resolved asap!!")


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
        self.lock = threading.Lock()

    def wrapperInit(self, config: {}) -> int:
        #log.info("Initializing ...")
        from transformers import AutoTokenizer, AutoModelForCausalLM, TextStreamer
        tokenizer_path = os.environ.get("TOKENIZER_PATH")
        model_path = os.environ.get("FULL_MODEL_PATH")
        infer_type = os.environ.get("INFER_TYPE")
        if not model_path or not tokenizer_path:
            log.error("should have environ(FULL_MODEL_PATH,MODEL_PATH,TOKENIZER_PATH)")
            return -1

        def load_model_tokenizer(model_path, tokenizer_path):
            tokenizer = AutoTokenizer.from_pretrained(tokenizer_path, trust_remote_code=True)
            model = AutoModelForCausalLM.from_pretrained(model_path, device_map="auto", trust_remote_code=True)
            return model,tokenizer

        self.base_model, self.base_tokenizer = load_model_tokenizer(model_path,tokenizer_path)
        self.filelogger = getFileLogger()
        self.filelogger.info("wrapperInit end")
        self.infer_type = infer_type

        session_total = config.get("common.lic", 0)
        if session_total > 0:
            init_rq()
            self.session.init_wrapper_config(config)
            self.session.init_handle_pool("thread", 1, MyReqDataThread)
        return 0

    def _base_model_inference(self, reqData: DataListCls, stream_cls) -> str:
        tokenizer = self.base_tokenizer
        model = self.base_model

        input_text = reqData.get("text").data.decode('utf-8')
        self.filelogger.info("got input_text , %s" % input_text)
        model_name = os.environ.get("PRETRAINED_MODEL_NAME")
        from ailab.atp_finetuner.constant import Model
        prompt_model = [Model.atom_7b]
        if model_name in prompt_model:
            from ailab.utils.template import Template
            template_dict = {
                Model.atom_7b: "atom",
            }
            prompt_template = Template(template_dict.get(model_name))
            history = []
            input_text = prompt_template.get_prompt(input_text, history, "")
        inputs = tokenizer(input_text, return_tensors='pt')

        def predict(model, input_ids):
            streamer = TextIteratorStreamer(tokenizer, timeout=60.0, skip_prompt=True, skip_special_tokens=True)
            gen_kwargs = {
                "input_ids": input_ids,
                "streamer": streamer,
                "max_new_tokens": 512,
                "repetition_penalty": 1.1,
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
        
        inputs = inputs.to(model.device)
        output = predict(model, inputs.input_ids)
        self.filelogger.info("got result , %s" % output)
        return output

    def _full_model_infence(self, reqData: DataListCls, stream_cls) -> str:
        model_name = os.environ.get("PRETRAINED_MODEL_NAME")
        if not model_name:
            log.error("should have environ PRETRAINED_MODEL_NAME")
            return None
        tokenizer = self.base_tokenizer
        model = self.base_model

        input_text = reqData.get("text").data.decode('utf-8')
        self.filelogger.info("got input_text , %s" % input_text)

        from transformers import TextIteratorStreamer
        from ailab.utils.template import get_template_and_fix_tokenizer
        from ailab.atp_finetuner.constant import Model
        from threading import Thread
        import torch

        template_dict = {
            Model.baichuan_7b : "default",
            Model.baichuan_13b : "default",
            Model.bloomz_7b1_mt : "default",
            Model.falcon_7b : "default",
            Model.moss_moon_003_base : "moss",
            Model.llama2_7b : "llama2",
            Model.internlm_7b : "default",
            Model.belle_7b_2m : "belle",
            Model.xverse_13b : "vanilla",
            Model.lawgpt_llama : "alpaca",
            Model.atom_7b: "atom",
            Model.chatglm3_6b: "chatglm3",
        }

        prompt_template = get_template_and_fix_tokenizer(template_dict.get(model_name),tokenizer)
        def predict_and_print(query) -> list:
            history = []
            prompt, _ = prompt_template.encode_oneturn(tokenizer=tokenizer, query=query, 
                                                       resp="", history=history, system=None)
            input_ids = torch.tensor([prompt], device=model.device)

            streamer = TextIteratorStreamer(tokenizer, timeout=60.0, skip_prompt=True, skip_special_tokens=True)
            gen_kwargs = {
                "input_ids": input_ids,
                "streamer": streamer,
                "do_sample": True,
                "temperature": 0.95,
                "top_p": 0.7,
                "top_k": 50,
                "num_beams": 1,
                "max_new_tokens": 512,
                "repetition_penalty": 1.0,
                "length_penalty": 1.0,
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

        result = predict_and_print(input_text)
        self.filelogger.info("got result , %s" % result)
        return result

    def wrapperOnceExec(self, params: {}, reqData: DataListCls, usrTag:str="",persId: int = 0) -> Response:
        self.filelogger.info("got reqdata , %s" % reqData.list)
        self.lock.acquire()
        if self.infer_type == 'base':
            result = self._base_model_inference(reqData, None)
        else:
            result = self._full_model_infence(reqData, None)
        self.lock.release()
        if not result:
            self.filelogger.info("#####")
            return -1

        self.filelogger.info("got result , %s" % result)
        # 使用Response封装result
        res = Response()
        resd = ResponseData()
        resd.key = "result"
        resd.setDataType(DataText)
        resd.status = Once
        resd.setData(result.encode("utf-8"))

        res.list = [resd]
        return res

    def wrapperFini(cls) -> int:
        return 0

    def wrapperError(cls, ret: int) -> str:
        if ret == 100:
            return "user error defined here"
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
