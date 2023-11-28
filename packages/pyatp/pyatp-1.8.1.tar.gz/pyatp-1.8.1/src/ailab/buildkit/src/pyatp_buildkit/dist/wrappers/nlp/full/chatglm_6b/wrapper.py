#!/usr/bin/env python
# coding:utf-8
"""
@license: Apache License2
@file: wrapper.py
@time: 2022-08-19 02:05:07.467170
@project: mnist
@project: ./
"""
import json
import torch
import os.path
import threading
from aiges.core.types import *
try:
    from aiges_embed import ResponseData, Response, DataListNode, DataListCls, SessionCreateResponse, callback, init_rq  # c++
except:
    from aiges.dto import Response, ResponseData, DataListNode, DataListCls, SessionCreateResponse, callback, init_rq

from aiges.sdk import WrapperBase, \
    ImageBodyField, \
    StringBodyField, StringParamField
from aiges.utils.log import log, getFileLogger
from ailab.log import logger

# 定义模型的超参数和输入参数
class UserRequest(object):
    input1 = StringBodyField(key="text", value=b"I have a problem with my iphone that needs to be resolved asap!!")


# 定义模型的输出参数
class UserResponse(object):
    accept1 = StringBodyField(key="result")


# 定义服务推理逻辑
class Wrapper(WrapperBase):
    serviceId = "chatglm"
    version = "v1"
    requestCls = UserRequest()
    responseCls = UserResponse()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model = None
        self.tokenizer = None
        self.resid_map = {}
        self.filelogger = None
        self.first_load_lora = True
        self.lock = threading.Lock()

    def wrapperInit(self, config: {}) -> int:
        logger.info("Initializing ...")
        from transformers import AutoTokenizer, AutoModel, AutoConfig
        tokenizer_path = os.environ.get("TOKENIZER_PATH")
        model_path = os.environ.get("FULL_MODEL_PATH")
        infer_type = os.environ.get("INFER_TYPE")

        if not tokenizer_path or not model_path:
            log.error("should have environ(FULL_MODEL_PATH,TOKENIZER_PATH)")
            return -1

        def load_model_tokenizer(model_path, tokenizer_path):
            tokenizer = AutoTokenizer.from_pretrained(
                tokenizer_path,
                use_fast=False,
                padding_side="left",
                trust_remote_code=True
            )

            config = AutoConfig.from_pretrained(model_path,trust_remote_code=True)
            model = AutoModel.from_pretrained(model_path, config=config, 
                                            trust_remote_code=True, device_map={"": 0})
            model.requires_grad_(False) # fix all model params
            model = model.half() # cast all params to float16 for inference
            model = model.cuda()
            model.eval()
            assert tokenizer.eos_token_id is not None, "Please update the *.json and *.py files of ChatGLM-6B from HuggingFace."
            return model, tokenizer
        
        self.base_model, self.base_tokenizer = load_model_tokenizer(model_path,tokenizer_path)
        self.filelogger = getFileLogger()
        self.infer_type = infer_type

        session_total = config.get("common.lic", 0)
        if session_total > 0:
            init_rq()
            self.session.init_wrapper_config(config)
            self.session.init_handle_pool("thread", 1, MyReqDataThread)
        return 0
    
    def _base_model_inference(self, reqData: DataListCls) -> str:
        tokenizer = self.base_tokenizer
        model = self.base_model

        input_text = reqData.get("text").data.decode('utf-8')
        self.filelogger.info("got input_text , %s" % input_text)
        response, history = model.chat(tokenizer, input_text, history=[])
        return response

    def _full_model_infence(self, reqData: DataListCls) -> str:
        tokenizer = self.base_tokenizer
        model = self.base_model
        instruction = reqData.get("text").data.decode('utf-8')

        history = []
        generating_args = {
            "do_sample":True,
            "temperature":0.95,
            "top_p":0.9,
            "top_k":60,
            "num_beams":1,
            "max_length":2048,
            "max_new_tokens":None,
            "repetition_penalty":1.1,
        }
        def evalute(query):
            from typing import Optional,List,Tuple
            def get_prompt(query: str, history: Optional[List[Tuple[str, str]]] = None, prefix: Optional[str] = None) -> str:
                prefix = prefix + "\n" if prefix else "" # add separator for non-empty prefix
                history = history or []
                prompt = ""
                for i, (old_query, response) in enumerate(history):
                    prompt += "[Round {}]\n\n问：{}\n\n答：{}\n\n".format(i+1, old_query, response)
                prompt += "[Round {}]\n\n问：{}\n\n答：".format(len(history)+1, query)
                prompt = prefix + prompt
                return prompt
            
            prefix = ""
            inputs = tokenizer([get_prompt(query, history, prefix)], return_tensors="pt")
            inputs = inputs.to(model.device)
            input_ids = inputs["input_ids"]

            from transformers import TextIteratorStreamer
            from threading import Thread
            streamer = TextIteratorStreamer(tokenizer, timeout=60.0, skip_prompt=True, skip_special_tokens=True)
            generating_args.update(dict(input_ids=input_ids,streamer=streamer))
            thread = Thread(target=model.generate, kwargs=generating_args)
            thread.start()

            response = ""
            for new_text in streamer:
                response += new_text

            return response

        result = evalute(instruction)
        return result
    
    def wrapperOnceExec(self, params: {}, reqData: DataListCls, usrTag:str="",persId: int = 0) -> Response:
        self.filelogger.info("got reqdata , %s" % reqData.list)

        self.lock.acquire()
        if self.infer_type == 'base':
            result = self._base_model_inference(reqData)
        else:
            result = self._full_model_infence(reqData)
        self.lock.release()

        if not result:
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

    def infer(self, reqData: DataListCls):
        params = self.session_thread.params
        wrapper_cls = params['wrapper']
        if wrapper_cls.infer_type == 'base':
            result = wrapper_cls._base_model_inference(reqData)
        else:
            result = wrapper_cls._full_model_infence(reqData)

        res= Response()
        if not result:
            return res.response_err(100)

        # 使用Response封装result
        resd = ResponseData()
        resd.key = "result"
        resd.setDataType(DataText)
        resd.status = DataEnd
        resd.setData(result.encode("utf-8"))
        res.list = [resd]
        self.session_thread.callback_fn(res, self.session_thread.sid)
        self.session_thread.reset()

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
