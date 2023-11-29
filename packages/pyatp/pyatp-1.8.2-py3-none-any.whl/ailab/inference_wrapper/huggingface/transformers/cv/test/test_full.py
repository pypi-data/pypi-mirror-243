from aiges.dto import Response, ResponseData, DataListNode, DataListCls



"""personal param"""
model_name = 'vit_patch16_224_in21k'
full_path = '/data1/cgzhang6/ailab_sdk/src/test/ailabmodel/my_vit_patch16_50'
module_name = 'image_classification'
# model_name = 'yolos_small'
# full_path = '/data1/cgzhang6/ailab_sdk/src/test/ailabmodel/my_yolos_small_50epoch'
# module_name = 'object_detection'
""""""

import sys
print(sys.path)

import importlib
module_path = f'ailab.inference_wrapper.huggingface.transformers.cv.{module_name}.wrapper.wrapper_full'
wrapper_module = importlib.import_module(module_path)
Wrapper = getattr(wrapper_module, 'Wrapper')
wrapper = Wrapper()

def Init():
    import os
    os.environ['FULL_MODEL_PATH'] = full_path
    wrapper.wrapperInit({})

def Once(key, text):
    http_node = DataListNode()
    http_node.key = 'image'
    with open(text, 'rb') as file:
        # 读取文件内容
        image_data = file.read()
    http_node.data = image_data
    http_data = DataListCls()
    http_data.list.append(http_node)
    wrapper.wrapperOnceExec({"atp_patch_id":key}, http_data, key)

if __name__ == '__main__' :
    Init()

    # 图像分类
    if module_name == 'image_classification':
        pics = [
            '/data1/cgzhang6/images/test_pic/sunflower01.jpg',
            '/data1/cgzhang6/images/test_pic/peony04.jpg',
            '/data1/cgzhang6/images/test_pic/rose03.jpg',
            '/data1/cgzhang6/images/test_pic/lily05.jpg',
            '/data1/cgzhang6/images/test_pic/peony01.jpg',
            '/data1/cgzhang6/images/test_pic/sakura01.jpg',
        ]
    elif module_name == 'object_detection':
        pics = [
            '/data1/cgzhang6/ailab_sdk/src/ailab/inference/test/images/detection/1001.png',
            '/data1/cgzhang6/ailab_sdk/src/ailab/inference/test/images/detection/1002.png',
            '/data1/cgzhang6/ailab_sdk/src/ailab/inference/test/images/detection/1003.png',
            '/data1/cgzhang6/ailab_sdk/src/ailab/inference/test/images/detection/1004.png',
            '/data1/cgzhang6/ailab_sdk/src/ailab/inference/test/images/detection/1005.png',
            '/data1/cgzhang6/ailab_sdk/src/ailab/inference/test/images/detection/1006.png',
        ]
    def worker(pic_path):
        print(f"Thread '{pic_path}' started.")
        Once(1, pic_path)
        print(f"Thread '{pic_path}' finished.")

    threads = []
    import threading
    for i in range(len(pics)):
        thread = threading.Thread(target=worker, args=(pics[i],))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

