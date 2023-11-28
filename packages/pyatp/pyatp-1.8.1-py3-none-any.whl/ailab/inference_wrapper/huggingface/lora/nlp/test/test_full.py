from aiges.dto import Response, ResponseData, DataListNode, DataListCls

"""personal param"""
model_name = 'baichuan_7b'
base_model_path = '/home/sdk_models/baichuan_7b'
token_path = '/home/sdk_models/baichuan_7b'
full_path = '/opt/ailab_sdk/src/test/ailabmodel/my_baichuan_model_full/checkpoint-500'
stream = 1
module_name = 'efficient'
finetune_type = 'lora'
infer_type = 'base'
""""""

import sys
print(sys.path)

import importlib
module_path = f'ailab.inference_wrapper.huggingface.lora.nlp.{module_name}.wrapper.wrapper_full'
wrapper_module = importlib.import_module(module_path)
Wrapper = getattr(wrapper_module, 'Wrapper')
wrapper = Wrapper()

def Init():
    import os
    os.environ['PRETRAINED_MODEL_NAME'] = model_name
    os.environ['TOKENIZER_PATH'] = token_path
    os.environ['FULL_MODEL_PATH'] = full_path
    os.environ['INFER_TYPE'] = infer_type

    config = {}
    if stream:
        config['common.lic'] = 1
    wrapper.wrapperInit(config)

def Once(key, text):
    http_node = DataListNode()
    http_node.key = 'text'
    text_data = text
    text_data = text_data.encode('utf-8')
    http_node.data = text_data 
    http_data = DataListCls()
    http_data.list.append(http_node)

    import os
    os.environ['PetrainedModel'] = model_name
    wrapper.wrapperOnceExec({"atp_patch_id":key}, http_data, key)

def StreamCreate():
    s = wrapper.wrapperCreate({}, 'sid','presid')
    return s.handle

def StreamWrite(handle,text):
    http_node = DataListNode()
    http_node.key = 'text'
    text_data = text
    text_data = text_data.encode('utf-8')
    http_node.data = text_data 
    http_data = DataListCls()
    http_data.list.append(http_node)

    wrapper.wrapperWrite(handle,http_data,'sessionid')

def StreamDestroy(handle):
    wrapper.wrapperDestroy(handle)


if __name__ == '__main__' :
    Init()
    if stream:
        handle_0 = StreamCreate()
        StreamWrite(handle_0,'what is NLP')
    else:
        Once(0, '自然语言处理是什么')
        Once(1, '自然语言处理是什么')


