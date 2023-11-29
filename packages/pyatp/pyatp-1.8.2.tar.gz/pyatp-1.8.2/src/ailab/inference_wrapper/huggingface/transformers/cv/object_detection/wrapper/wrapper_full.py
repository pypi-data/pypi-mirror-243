#!/usr/bin/env python
# coding:utf-8
"""
@license: Apache License2
@Author: xiaohan4
@time: 2023/03/18
@project: ailab
"""
import base64
import json
import io
import os
import torch
# from ifly_atp_sdk.huggingface.pipelines import pipeline
from transformers import pipeline
from PIL import Image

from aiges.core.types import *

try:
    from aiges_embed import ResponseData, Response, DataListNode, DataListCls  # c++
except:
    from aiges.dto import Response, ResponseData, DataListNode, DataListCls
from aiges.sdk import WrapperBase, \
    JsonBodyField, StringBodyField, ImageBodyField, \
    StringParamField
from aiges.utils.log import log, getFileLogger

# 使用的模型
task = "object-detection"

# 定义模型的超参数和输入参数
class UserRequest(object):
    input1 = ImageBodyField(key="image", path='./cat.jpg')


# 定义模型的输出参数
class UserResponse(object):
    accept1 = StringBodyField(key="result")


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

    def wrapperInit(self, config: {}) -> int:
        self.filelogger = getFileLogger()
        full_model_path = os.environ.get("FULL_MODEL_PATH")
        if not full_model_path:
            self.filelogger.error("should have environ(FULL_MODEL_PATH")
            return -1

        def load_model_and_imageprocessor(model_path):
            from transformers import AutoImageProcessor, AutoModelForObjectDetection
            model = AutoModelForObjectDetection.from_pretrained(model_path)
            image_processor = AutoImageProcessor.from_pretrained(model_path)
            return model,image_processor

        self.full_model, self.full_image_processor = load_model_and_imageprocessor(full_model_path)
        return 0

    def _model_inference(self, model, image_processor, reqData: DataListCls):
        imagebytes = reqData.get("image").data
        image = Image.open(io.BytesIO(imagebytes))
        if image.mode != "RGB":
            image = image.convert("RGB")
        inputs = image_processor(image, return_tensors="pt")
        out_objects = []
        with torch.no_grad():
            outputs = model(**inputs)
            target_sizes = torch.tensor([image.size[::-1]])
            results = image_processor.post_process_object_detection(outputs, threshold=0.7, target_sizes=target_sizes)[0]

        for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
            box = [round(i, 2) for i in box.tolist()]
            label_name = model.config.id2label[label.item()]
            confidence = round(score.item(), 3)
            out_objects.append({
                'object': label_name,
                'confidence': confidence,
                'bbox': box,
            })
        return out_objects

    def wrapperOnceExec(self, params: {}, reqData: DataListCls, usrTag:str="",persId: int = 0) -> Response:
        patch_id = params.get("atp_patch_id", 0)
        self.filelogger.info("got reqdata , %s" % reqData.list)
        result = self._model_inference(self.full_model, self.full_image_processor, reqData)
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
        resd.setData(json.dumps(result).encode("utf-8"))
        # self.filelogger.info("###")
        # self.filelogger.info(result)
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
