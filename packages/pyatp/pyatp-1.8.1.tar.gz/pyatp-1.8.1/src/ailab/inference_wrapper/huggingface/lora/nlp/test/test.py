from aiges.dto import Response, ResponseData, DataListNode, DataListCls

"""personal param"""
model_name = 'baichuan_7b'
pretrain_model_name = '/home/sdk_models/baichuan_7b'
token_path = '/home/sdk_models/baichuan_7b'
zip_path = '/home/finetuned_models/my_baichuan_model/adapter.zip'
stream = 1
finetune_type = 'lora'
infer_type = 'base'
""""""

import sys
print(sys.path)

import importlib
module_path = f'ailab.inference_wrapper.huggingface.lora.nlp.wrapper'
wrapper_module = importlib.import_module(module_path)
Wrapper = getattr(wrapper_module, 'Wrapper')
wrapper = Wrapper()

def get_messages(text):
    message = {
        "messages": [ {
        "content": text, "role": 'user'
        } ]
    }
    import json
    return json.dumps(message)

def Init():
    import os
    os.environ['PRETRAINED_MODEL_NAME'] = model_name
    os.environ['FULL_MODEL_PATH'] = pretrain_model_name
    os.environ['TOKENIZER_PATH'] = token_path
    os.environ['FINETUNE_TYPE'] = finetune_type
    os.environ['INFER_TYPE'] = infer_type
    config = {}
    if stream:
        config['common.lic'] = 1
    wrapper.wrapperInit(config)

def LoadRes(key):
    zip_file_path = zip_path
    with open(zip_file_path, 'rb') as zip_file:
        # 读取压缩包的二进制数据
        zip_data = zip_file.read()
        # 计算数据长度
        zip_data_length = len(zip_data)

    list_node = DataListNode()
    list_node.key = str(key)
    list_node.data = zip_data
    list_node.len = zip_data_length

    req_data = DataListCls()
    req_data.list.append(list_node)
    wrapper.wrapperLoadRes(req_data, key)

def Once(key, text):
    http_node = DataListNode()
    http_node.key = 'messages'
    text_data = get_messages(text).encode('utf-8')
    http_node.data = text_data 
    http_data = DataListCls()
    http_data.list.append(http_node)
    wrapper.wrapperOnceExec({"res_id":key}, http_data, key)

def UnloadRes(key):
    wrapper.wrapperUnloadRes(key)

def StreamCreate(patch_id):
    s = wrapper.wrapperCreate({}, 'presid',patch_id)
    return s.handle

def StreamWrite(handle,text):
    http_node = DataListNode()
    http_node.key = 'messages'
    text_data = get_messages(text).encode('utf-8')
    http_node.data = text_data 
    http_data = DataListCls()
    http_data.list.append(http_node)

    wrapper.wrapperWrite(handle,http_data,'sessionid')

def StreamDestroy(handle):
    wrapper.wrapperDestroy(handle)

if __name__ == '__main__' :
    Init()
    LoadRes('1')
    if stream:
        handle_0 = StreamCreate('1')
        StreamWrite(handle_0,'什么是自然语言处理')
    else:
        Once('0', '什么是自然语言处理')
        Once('1', '什么是自然语言处理')
    #UnloadRes('1')


