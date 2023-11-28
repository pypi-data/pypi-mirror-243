#!/bin/bash

python -m ailab.inference \
    --finetune_type lora \
    --pretrained_model_name ziya_llama_13b \
    --pretrained_model_path /home/sdk_models/ziya_llama_13b \
    --tokenizer_path /home/sdk_models/ziya_llama_13b \
    --fintuned_weights /home/ailab_sdk/src/test/ailabmodel/my_ziya_model_10_27_lora/final \
    --test_dataset_path /home/ailab_sdk/src/ailab/inference/test/val.txt \
    --base_result_path /home/ailab_sdk/src/ailab/inference/test/base.jsonl \
    --finetuned_result_path /home/ailab_sdk/src/ailab/inference/test/finetune.jsonl 

# python -m ailab.inference \
#     --finetune_type full \
#     --pretrained_model_name vit_patch16_224_in21k \
#     --pretrained_model_path /home/sdk_models/vit_base_patch16_224_in21k \
#     --tokenizer_path /home/sdk_models/vit_base_patch16_224_in21k \
#     --fintuned_weights /data1/cgzhang6/ailab_sdk/src/test/ailabmodel/my_vit_patch16 \
#     --test_dataset_path /data1/cgzhang6/ailab_sdk/src/ailab/inference/test/images/classification \
#     --base_result_path /data1/cgzhang6/ailab_sdk/src/ailab/inference/test/base.jsonl \
#     --finetuned_result_path /data1/cgzhang6/ailab_sdk/src/ailab/inference/test/finetune.jsonl

# python -m ailab.inference \
#     --finetune_type full \
#     --pretrained_model_name yolos_small \
#     --pretrained_model_path /home/sdk_models/yolos_small \
#     --tokenizer_path /home/sdk_models/yolos_small \
#     --fintuned_weights /data1/cgzhang6/ailab_sdk/src/test/ailabmodel/my_yolos_small_80epoch_balloon \
#     --test_dataset_path /data1/cgzhang6/images/balloon/test \
#     --base_result_path /data1/cgzhang6/ailab_sdk/src/ailab/inference/test/base.jsonl \
#     --finetuned_result_path /data1/cgzhang6/ailab_sdk/src/ailab/inference/test/finetune.jsonl
