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
from aiges.core.types import *
from peft import PeftModel
from transformers import LlamaForCausalLM, AutoTokenizer, AutoConfig, AutoModelForCausalLM, BitsAndBytesConfig
from typing import List
import torch.nn.functional as F
import torch

try:
    from aiges_embed import ResponseData, Response, DataListNode, DataListCls  # c++
except:
    from aiges.dto import Response, ResponseData, DataListNode, DataListCls

from aiges.sdk import WrapperBase, ImageBodyField, StringBodyField, StringParamField
from aiges.utils.log import log, getFileLogger

try:
    from aiges_embed import callback_metric
except:
    callback_metric = None


# 定义模型的超参数和输入参数
class UserRequest(object):
    input1 = StringBodyField(key="text", value=b"I have a problem with my iphone that needs to be resolved asap!!")


# 定义模型的输出参数
class UserResponse(object):
    accept1 = StringBodyField(key="result")


def zero_pad_sequences(sequences: List[torch.Tensor], side: str = "left", padding_value: int = 0) -> torch.Tensor:
    assert side in ("left", "right")
    max_len = max(seq.size(0) for seq in sequences)
    padded_sequences = []
    for seq in sequences:
        pad_len = max_len - seq.size(0)
        padding = (pad_len, 0) if side == "left" else (0, pad_len)
        padded_sequences.append(F.pad(seq, padding, value=padding_value))
    return torch.stack(padded_sequences, dim=0)


def generate(queries: List[str], tokenizer: AutoTokenizer, model: LlamaForCausalLM, device: int = 0, **generate_kwargs):
    def _apply_prefix(query):
        return f"<human>:{query.strip()}\n<bot>:"

    def _tokenizing(queries):
        input_ids = []
        for query in queries:
            query = _apply_prefix(query)
            input_ids.append(torch.tensor(tokenizer(query).input_ids))
        inputs = zero_pad_sequences(input_ids, side="left", padding_value=generate_kwargs["pad_token_id"])
        return inputs

    input_ids = _tokenizing(queries).to(device)
    pad_token_id = generate_kwargs["pad_token_id"]
    input_attention_mask = input_ids.not_equal(pad_token_id).to(dtype=torch.bool, device=device)
    sequences = model.generate(inputs=input_ids.to(device), attention_mask=input_attention_mask, **generate_kwargs)
    output = []
    for seq in sequences:
        out_text = tokenizer.decode(seq.tolist(), skip_special_tokens=False).split("<bot>:")[-1]
        output.append(out_text.replace("<s>", "").replace("</s>", ""))
    return output


# 定义服务推理逻辑
class Wrapper(WrapperBase):
    serviceId = "ziya_llama_13b"
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
        # log.info("Initializing ...")
        from transformers import AutoTokenizer, AutoModelForCausalLM, TextStreamer

        tokenizer_path = os.environ.get("TOKENIZER_PATH")
        base_model = os.environ.get("MODEL_PATH")
        self.pretrained_name = os.environ.get("PRETRAINED_MODEL_NAME")

        if not self.pretrained_name:
            log.error("should have environ(PRETRAINED_MODEL_NAME,MODEL_PATH(lora weight dir）,TOKENIZER_PATH)")
            return -1

        # 加载基础模型
        # base_model = f"/home/.atp/models/{self.pretrained_name}"
        # tokenizer_path = f"/home/.atp/models/{self.pretrained_name}"
        if not os.path.isdir(base_model):
            log.error(f"not find the base_model in {base_model}")
            return -1
        if not base_model or not tokenizer_path:
            log.error("should have environ(FULL_MODEL_PATH,(base or full ）,TOKENIZER_PATH)")
            return -1

        tokenizer = AutoTokenizer.from_pretrained(tokenizer_path, trust_remote_code=True)
        model = AutoModelForCausalLM.from_pretrained(base_model, device_map="auto", trust_remote_code=True)

        self.model = model
        self.tokenizer = tokenizer
        self.filelogger = getFileLogger()
        self.filelogger.info("wrapperInit end")
        return 0

    def checkValidLora(self, pretrained_name, lora_path):
        import json

        confjson = "adapter_config.json"
        if not os.path.isdir(lora_path):
            msg = "not find  %s" % lora_path
            log.error(msg)
            return False, msg
        files = os.listdir(lora_path)
        if not confjson in files:
            msg = "%s doesnt have file adapter_config.json" % lora_path
            log.error(msg)
            return False, msg
        fp = open(os.path.join(lora_path, confjson), "rb")
        conf = json.load(fp)
        base_model_path = conf.get("base_model_name_or_path", "")
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
        with zipfile.ZipFile(byte_stream, "r") as zip_ref:
            zip_ref.extractall(lora_weight_path)

        # valid, msg = self.checkValidLora(self.pretrained_name, lora_weight_path)
        # if not valid:
        #    return -1
        # log.info(msg)
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

    def _base_model_inference(self, reqData: DataListCls) -> str:
        tokenizer = self.tokenizer
        model = self.model

        input_text = reqData.get("text").data.decode("utf-8")
        self.filelogger.info("got input_text , %s" % input_text)

        generate_kwargs = {
            "do_sample": True,
            "top_p": 1.0,
            "top_k": 0,
            "max_length": 2048,
            "repetition_penalty": 1.0,
            "temperature": 0.8,
            "pad_token_id": tokenizer.eos_token_id,
            "eos_token_id": tokenizer.eos_token_id,
        }
        queries = [input_text]
        ans = generate(queries=queries, tokenizer=tokenizer, model=model, device=0, **generate_kwargs)
        return ans[0].split("<bot> :")[1]


    def _lora_model_infence(self, reqData: DataListCls, patch_id: int) -> str:
        if patch_id not in self.patch_id:
            log.error("patch_id not exist")
            return None
        model_name = self.pretrained_name
        tokenizer = self.tokenizer
        model = self.model
        lora_weight = self.patch_id[patch_id]
        model.load_adapter(lora_weight, patch_id)
        model.set_adapter(str(patch_id))

        input_text = reqData.get("text").data.decode("utf-8")
        self.filelogger.info("got input_text , %s" % input_text)

        generate_kwargs = {
            "do_sample": True,
            "top_p": 1.0,
            "top_k": 0,
            "max_length": 2048,
            "repetition_penalty": 1.0,
            "temperature": 0.8,
            "pad_token_id": tokenizer.eos_token_id,
            "eos_token_id": tokenizer.eos_token_id,
        }
        queries = [input_text]
        ans = generate(queries=queries, tokenizer=tokenizer, model=model, device=0, **generate_kwargs)
        return ans[0].split("<bot> :")[1]

    def wrapperOnceExec(self, params: {}, reqData: DataListCls, usrTag: str = "", persId: int = 0) -> Response:
        patch_id = params.get("atp_patch_id", 0)
        self.filelogger.info("got reqdata , %s" % reqData.list)
        self.lock.acquire()
        if patch_id == 0 or patch_id == "0":
            result = self._base_model_inference(reqData)
        else:
            result = self._lora_model_infence(reqData, patch_id)
        self.lock.release()
        res = Response()
        if not result:
            self.filelogger.info("no result")
            return res.response_err(100)

        self.filelogger.info("got result , %s" % result)
        # 使用Response封装result
        resd = ResponseData()
        resd.key = "result"
        resd.setDataType(DataText)
        resd.status = Once
        resd.setData(result.encode("utf-8"))
        self.filelogger.info("###")

        #self.filelogger.info(result)
        if callback_metric:
            ret = callback_metric(usrTag, "business.total", 1)
            self.filelogger.info("calc business.total, count: %d " % ret)
        res.list = [resd]
        return res

    def wrapperFini(cls) -> int:
        return 0

    def wrapperError(cls, ret: int) -> str:
        if ret == 100:
            return "no result.."
        return ""

    """
        此函数保留测试用，不可删除
    """

    def wrapperTestFunc(cls, data: [], respData: []):
        pass

    def testLoad(self, patch_id):
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
        # import pdb
        # pdb.set_trace()

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
            params["atp_patch_id"] = "0"
            response = self.wrapperOnceExec(params, req)
            params["atp_patch_id"] = "1111"
            response = self.wrapperOnceExec(params, req)
            params["atp_patch_id"] = "0"
            response = self.wrapperOnceExec(params, req)
            if self.check_resp(response):
                log.info("wrapper.py has been verified... Congratulations ...!")
            else:
                log.error("Sorry, Please Check The Log Output Above ...")
        except Exception as e:
            # 4. 模拟检查 wrapperOnceExec返回
            log.error(e)
            self.wrapperError(-1)


if __name__ == "__main__":
    m = Wrapper()
    m.run()
