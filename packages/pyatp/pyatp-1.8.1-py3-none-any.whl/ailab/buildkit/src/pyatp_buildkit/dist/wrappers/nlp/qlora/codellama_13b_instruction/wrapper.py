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

try:
    from aiges_embed import callback_metric
except:
    callback_metric=None

TEST=0

# 定义模型的超参数和输入参数
class UserRequest(object):
    input1 = StringBodyField(key="text", value=b"I have a problem with my iphone that needs to be resolved asap!!")


# 定义模型的输出参数
class UserResponse(object):
    accept1 = StringBodyField(key="result")

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
        self.patch_id = {}
        self.first_load_lora = True
        self.lock = threading.Lock()

    def wrapperInit(self, config: {}) -> int:
        #log.info("Initializing ...")
        from transformers import AutoTokenizer, AutoModelForCausalLM, AutoConfig,BitsAndBytesConfig
        self.pretrained_name = os.environ.get("PRETRAINED_MODEL_NAME")

        if not self.pretrained_name: 
            log.error("should have environ(PRETRAINED_MODEL_NAME,MODEL_PATH(lora weight dir）,TOKENIZER_PATH)")
            return -1

        tokenizer_path = os.environ.get("TOKENIZER_PATH")
        base_model = os.environ.get("FULL_MODEL_PATH")
        finetune_type = os.environ.get("FINETUNE_TYPE",'lora')

        if not os.path.isdir(base_model):
            log.error(f"not find the base_model in {base_model}")
            return -1
        if not base_model or not tokenizer_path:
            log.error("should have environ(FULL_MODEL_PATH,(base or full ）,TOKENIZER_PATH)")
            return -1

        tokenizer = AutoTokenizer.from_pretrained(tokenizer_path, trust_remote_code=True)

        if finetune_type == 'qlora':
            import torch
            model_config = AutoConfig.from_pretrained(base_model,trust_remote_code=True)
            model = AutoModelForCausalLM.from_pretrained(
                base_model,
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
            model = AutoModelForCausalLM.from_pretrained(base_model, device_map="auto", trust_remote_code=True)
        self.model = model
        self.tokenizer = tokenizer
        self.filelogger = getFileLogger()
        self.filelogger.info("wrapperInit end")

        session_total = config.get("common.lic", 0)
        if session_total > 0:
            init_rq()
            self.session.init_wrapper_config(config)
            self.session.init_handle_pool("thread", 1, MyReqDataThread)
        return 0

    def checkValidLora(self, pretrained_name, lora_path):
        import json
        confjson = "adapter_config.json"
        if not os.path.isdir(lora_path):
            msg = "not find  %s"%lora_path
            log.error(msg)
            return False, msg
        files = os.listdir(lora_path)
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

    def wrapperLoadRes(self, reqData: DataListCls, patch_id: int) -> int:
        from peft import PeftModel
        if patch_id in self.patch_id:
            log.warn("patch_id has exist.Please first to UnloadRes")
            return 0
        lora_weight_path = "/home/.atp/lora_weight/"
        lora_weight_path = os.path.join(lora_weight_path, str(patch_id))
        if os.path.exists(lora_weight_path):
            log.warn("zip file has exist.Please first to UnloadRes")

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
        self.lock.acquire()
        adapter_name = str(patch_id)
        if self.first_load_lora == True:
            self.model = PeftModel.from_pretrained(self.model, lora_weight_path, adapter_name=adapter_name)
            self.first_load_lora = False
        else:
            self.model.load_adapter(lora_weight_path, adapter_name)

        self.patch_id[patch_id] = lora_weight_path
        self.lock.release()
        log.info("Load Resource Successfully...")
        return 0

    def wrapperUnloadRes(self, presid: int) -> int:
        if presid not in self.patch_id:
            log.error("patch_id not exist")
            return 0 
        lora_weight_path = self.patch_id[presid]
        if not os.path.exists(lora_weight_path):
            log.error("lora weigth path not exist")
            return 0
        
        self.lock.acquire()
        import shutil
        shutil.rmtree(lora_weight_path)
        del self.patch_id[presid]
        self.lock.release()
        return 0

    def _base_model_inference(self, reqData: DataListCls, stream_cls) -> str:
        tokenizer = self.tokenizer
        model = self.model

        input_text = reqData.get("text").data.decode('utf-8')
        self.filelogger.info("got input_text , %s" % input_text)
        model_name = self.pretrained_name
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

        if hasattr(model, 'disable_adapter'):
            with model.disable_adapter():
                inputs = inputs.to(model.device)
                output = predict(model, inputs.input_ids)
                self.filelogger.info("got result , %s" % output)
                return output
        else:
            inputs = inputs.to(model.device)
            output = predict(model, inputs.input_ids)
            self.filelogger.info("got result , %s" % output)
            return output

    def _lora_model_infence(self, reqData: DataListCls, patch_id:int, stream_cls) -> str:
        if patch_id not in self.patch_id:
            log.error("patch_id not exist")
            return None
        model_name = self.pretrained_name
        tokenizer = self.tokenizer
        model = self.model
        lora_weight = self.patch_id[patch_id]
        model.load_adapter(lora_weight,patch_id)
        model.set_adapter(str(patch_id))

        input_text = reqData.get("text").data.decode('utf-8')
        self.filelogger.info("got input_text , %s" % input_text)

        from transformers import TextIteratorStreamer
        from ailab.utils.template import get_template_and_fix_tokenizer
        from ailab.atp_finetuner.constant import Model
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
        patch_id = params.get("atp_patch_id", 0)
        self.filelogger.info("got reqdata , %s" % reqData.list)
        self.lock.acquire()
        if patch_id == 0 or patch_id == "0":
            result = self._base_model_inference(reqData,None)
        else:
            result = self._lora_model_infence(reqData, patch_id,None)
        self.lock.release()
        res= Response()
        if not result:
            self.filelogger.info("no result")
            return res.response_err(100)

        # 使用Response封装result
        resd = ResponseData()
        resd.key = "result"
        resd.setDataType(DataText)
        resd.status = Once
        resd.setData(result.encode("utf-8"))

        if callback_metric:
            ret = callback_metric(usrTag, "business.total", 1)
            self.filelogger.info("calc business.total, count: %d " %ret)
        res.list = [resd]
        return res

    def wrapperFini(cls) -> int:
        return 0

    def wrapperError(cls, ret: int) -> str:
        if ret == 100:
            return "no result.."
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


    def testLoad(self,patch_id):
        from peft import PeftModel
        lora_weight_path = "/home/.atp/lora_weight/"
        lora_weight_path = os.path.join(lora_weight_path, str(patch_id))
        if self.first_load_lora == True:
            self.model = PeftModel.from_pretrained(self.model, lora_weight_path, adapter_name=patch_id)
            self.first_load_lora = False
        else:
            self.model.load_adapter(lora_weight_path, patch_id)
        self.patch_id[patch_id] = lora_weight_path
        self.model.eval()


    def run_once_test(self):
        # 1. 模拟调用初始化引擎
        #  传入配置当前模拟为空
        self.wrapperInit(self.config)
        self.testLoad("1111")
        #import pdb
        #pdb.set_trace()

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
            params['atp_patch_id'] = '1111'
            response = self.wrapperOnceExec(params, req)
            params['atp_patch_id'] = '0'
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
            wrapper_cls._base_model_inference(reqData,self)
        else:
            wrapper_cls._lora_model_infence(reqData, patch_id,self)

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


