#!/usr/bin/env python
# coding:utf-8
"""
@license: Apache License2
@Author: xiaohan4
@time: 2023/02/27
@project: ailab
"""
import json
import os.path
import threading
from aiges.core.types import *
import torch

try:
    from aiges_embed import ResponseData, Response, DataListNode, DataListCls  # c++
except:
    from aiges.dto import Response, ResponseData, DataListNode, DataListCls

from aiges.sdk import WrapperBase, \
    JsonBodyField, StringBodyField, ImageBodyField, \
    StringParamField
from aiges.utils.log import log, getFileLogger

import io
# from ifly_atp_sdk.huggingface.pipelines import pipeline
from transformers import pipeline
from PIL import Image

task = "image-classification-pipeline"


# 定义模型的超参数和输入参数
class UserRequest(object):
    input1 = ImageBodyField(key="image", path='./img.png')
    input2 = StringParamField(key="task", value=task)


# 定义模型的输出参数
class UserResponse(object):
    accept1 = JsonBodyField(key="result")


# 定义服务推理逻辑
class Wrapper(WrapperBase):
    serviceId = task
    version = "v1"
    requestCls = UserRequest()
    responseCls = UserResponse()
    model = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filelogger = None
        self.lock = threading.Lock()

    def wrapperInit(self, config: {}) -> int:
        self.filelogger = getFileLogger()
        full_model_path = os.environ.get("FULL_MODEL_PATH")
        if not full_model_path:
            self.filelogger.error("should have environ(FULL_MODEL_PATH")
            return -1

        def load_model_and_imageprocessor(model_path):
            from transformers import AutoImageProcessor, AutoModelForImageClassification
            model = AutoModelForImageClassification.from_pretrained(model_path)
            image_processor = AutoImageProcessor.from_pretrained(model_path)
            return model,image_processor

        self.full_model, self.full_image_processor = load_model_and_imageprocessor(full_model_path)
        return 0

    def _model_inference(self, model, image_processor, reqData: DataListCls) -> str:
        imagebytes = reqData.get("image").data
        image = Image.open(io.BytesIO(imagebytes))
        inputs = image_processor(image, return_tensors="pt")
        with torch.no_grad():
            logits = model(**inputs).logits
        predicted_label = logits.argmax(-1).item()
        predicted_name = model.config.id2label[predicted_label]

        return predicted_name

    def wrapperOnceExec(self, params: {}, reqData: DataListCls, usrTag:str="",persId: int = 0) -> Response:
        patch_id = params.get("atp_patch_id", 0)
        self.filelogger.info("got reqdata , %s" % reqData.list)
        self.lock.acquire()
        result = self._model_inference(self.full_model, self.full_image_processor, reqData)
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
        print("###")
        self.filelogger.info("###")
        self.filelogger.info(result)
        print(result)
        res.list = [resd]

        return res

    def wrapperFini(cls) -> int:
        return 0

    def wrapperError(cls, ret: int) -> str:
        if ret == 100:
            return "user error defined here"
        return ""

    '''
        此函数保留测试用，不可删除
    '''

    def wrapperTestFunc(cls, data: [], respData: []):
        pass


if __name__ == '__main__':
    m = Wrapper()
    m.run()
