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
import json
import threading
import torch
from threading import Thread
from aiges.core.types import *
try:
    from aiges_embed import ResponseData, Response, DataListNode, DataListCls, SessionCreateResponse, callback  # c++
except:
    from aiges.dto import Response, ResponseData, DataListNode, DataListCls, SessionCreateResponse, callback

from aiges.dto import init_rq
from aiges.sdk import WrapperBase, \
    ImageBodyField, \
    StringBodyField, StringParamField
from aiges.utils.log import log, getFileLogger
from transformers import TextIteratorStreamer

try:
    from aiges_embed import callback_metric
except:
    callback_metric=None

TEST=1

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

def get_payload_messages(reqData: DataListCls):
    messages = json.loads(reqData.get('messages').data.decode('utf-8'))
    message = messages['messages'][0]['content']
    role = messages['messages'][0]['role']
    return message

def resp_content(status, index, text):
    resp_json = {"choices":[{"content":text,"index":index,"role":"assistant"}],"question_type":"math"}
    resd = ResponseData()
    resd.key = "content"
    resd.setDataType(DataText)
    resd.status = status
    resd.setData(json.dumps(resp_json).encode("utf-8"))
    return resd

def resp_usage(status, prompt_token, completion_token):
    resp_json = {"completion_tokens":completion_token,"prompt_tokens":prompt_token,"question_tokens":4,"total_tokens":prompt_token+completion_token}
    resd = ResponseData()
    resd.key = "usage"
    resd.setDataType(DataText)
    resd.status = status
    resd.setData(json.dumps(resp_json).encode("utf-8"))
    return resd

# 定义模型的超参数和输入参数
class UserRequest(object):
    input1 = StringBodyField(key="text", value=b"I have a problem with my iphone that needs to be resolved asap!!")


# 定义模型的输出参数
class UserResponse(object):
    accept1 = StringBodyField(key="result")

class WrapperFactory():
    def __init__(self,pretrained_name,base_model_path,tokenizer_path,finetune_type,infer_type):
        self.pretrained_name = pretrained_name
        self.base_model_path = base_model_path
        self.tokenizer_path = tokenizer_path
        self.finetune_type = finetune_type
        self.infer_type = infer_type
        self.model = None
        self.tokenizer = None
        self.first_load_peft = True

    def load_peft_model(self,lora_weight_path,patch_id):
        from peft import PeftModel
        if self.first_load_peft == True:
            self.model = PeftModel.from_pretrained(self.model, lora_weight_path, adapter_name=patch_id)
            self.first_load_peft = False
        else:
            self.model.load_adapter(lora_weight_path, patch_id)
        self.model.eval()

    def load_model_tokenizer(self):
        pass

    def once_infer(self, params, reqData: DataListCls, lora_weight,stream_handle_cls):
        log.info(f'once_infer finetune_type {self.finetune_type}')
        if self.finetune_type == 'lora' or self.finetune_type == 'qlora':
            patch_id = params.get("patch_id", 0)
            if patch_id == 0 or patch_id == "0":
                input, result = self.base_predict(reqData,stream_handle_cls)
            else:
                input,result = self.trained_predict(reqData, lora_weight, patch_id, stream_handle_cls)
        elif self.finetune_type == 'full':
            if self.infer_type == 'base':
                input, result = self.base_predict(reqData,stream_handle_cls)
            else:
                input, result = self.trained_predict(reqData, None, None, stream_handle_cls)
        return input, result

    def base_predict(self, reqData: DataListCls, stream_cls):
        tokenizer = self.tokenizer
        model = self.model

        input_text = get_payload_messages(reqData)
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
            index = 0
            for new_text in streamer:
                if stream_cls:
                    cur_state = transform_stream_state(cur_state, streamer.print_len, new_text)
                    stream_cls.on_stream_infer(new_text,cur_state,index,0,0)
                response += new_text
                index = index+1 if new_text and cur_state != DataNone else index
            if stream_cls and cur_state == DataContinue:
                stream_cls.on_stream_infer('.',DataEnd,index,self.get_tokens(input_text),self.get_tokens(response))
            return response

        if hasattr(model, 'disable_adapter'):
            with model.disable_adapter():
                inputs = inputs.to(model.device)
                output = predict(model, inputs.input_ids)
                log.info("got result , %s" % output)
                return input_text,output
        else:
            inputs = inputs.to(model.device)
            output = predict(model, inputs.input_ids)
            log.info("got result , %s" % output)
            return input_text,output

    def trained_predict(self, reqData: DataListCls, lora_weight, patch_id, stream_cls):
        pass

    def get_tokens(self, input):
        return len(self.tokenizer.tokenize(input))

    @classmethod
    def create_wrapper_cls(cls, pretrain_name,base_model_path,tokenizer_path,finetune_type,infer_type):
        from ailab.atp_finetuner.constant import Model
        efficent_model = [Model.baichuan_7b,Model.baichuan_13b,Model.bloomz_7b1_mt,Model.falcon_7b,Model.falcon_7b_instruct,
                        Model.moss_moon_003_base,Model.llama2_7b,Model.internlm_7b,Model.belle_7b_2m,
                        Model.xverse_13b,Model.lawgpt_llama,Model.bloomz_3b,Model.bloomz_1b1,
                        Model.codellama_7b_instruction,Model.codellama_13b_instruction,Model.atom_7b,
                        Model.chatglm3_6b,Model.llama2_7b_chat_hf,Model.llama2_13b_chat_hf]
        glm_model = [Model.chatglm_6b,Model.chatglm2_6b,Model.code_geex_2]
        chinese_alpaca_model = [Model.chinese_alpaca,Model.chinese_alpaca_2,Model.chinese_alpaca_2_13b,
                                Model.chinese_alpaca_2_7b_16k,Model.chinese_alpaca_2_13b_16k,Model.chinese_alpaca_2_1b3]
        alpaca_model = [Model.alpaca,Model.vicuna,Model.bencao_llama]
        ziya_model = [Model.ziya_llama_13b]

        if pretrain_name in alpaca_model:
            return AlpacaWrapper(pretrain_name,base_model_path,tokenizer_path,finetune_type,infer_type)
        elif pretrain_name in efficent_model:
            return EfficientWrapper(pretrain_name,base_model_path,tokenizer_path,finetune_type,infer_type)
        elif pretrain_name in chinese_alpaca_model:
            return ChineseAlpacaWrapper(pretrain_name,base_model_path,tokenizer_path,finetune_type,infer_type)
        elif pretrain_name in glm_model:
            return ChatGlmWrapper(pretrain_name,base_model_path,tokenizer_path,finetune_type,infer_type)
        
class AlpacaWrapper(WrapperFactory):
    def __init__(self, pretrained_name,base_model_path,tokenizer_path,finetune_type,infer_type) -> None:
        super().__init__(pretrained_name,base_model_path,tokenizer_path,finetune_type,infer_type)

    def load_model_tokenizer(self):
        from transformers import LlamaForCausalLM, LlamaTokenizer
        tokenizer = LlamaTokenizer.from_pretrained(self.tokenizer_path)
        tokenizer.pad_token_id = 0
        model = LlamaForCausalLM.from_pretrained(self.base_model_path,load_in_8bit=True,torch_dtype=torch.float16,device_map="auto",)
        self.model = model
        self.tokenizer = tokenizer

    def load_peft_model(self,lora_weight_path,patch_id):
        from peft import PeftModel
        if self.first_load_peft == True:
            self.model = PeftModel.from_pretrained(self.model, lora_weight_path, adapter_name=patch_id)
            self.first_load_peft = False
        else:
            self.model.load_adapter(lora_weight_path, patch_id)
        self.model.config.pad_token_id = 0  # unk
        self.model.config.bos_token_id = 1
        self.model.config.eos_token_id = 2
        self.model.eval()
        self.model = torch.compile(self.model)

    def trained_predict(self, reqData: DataListCls, lora_weight, patch_id, stream_cls):
        tokenizer = self.tokenizer
        model = self.model

        if self.finetune_type == 'lora' or self.finetune_type == 'qlora':
            model.load_adapter(lora_weight,patch_id)
            model.set_adapter(str(patch_id))

        from transformers import GenerationConfig
        prompt_template: str = "alpaca"  # The prompt template to use, will default to alpaca.
        from ailab.utils.prompter import Prompter
        prompter = Prompter(prompt_template)

        def evaluate(
            instruction,
            input=None,
            temperature=0.1,
            top_p=0.75,
            top_k=40,
            num_beams=4,
            max_new_tokens=128,
            stream_output=False,
            **kwargs,
        ):
            prompt = prompter.generate_prompt(instruction, input)
            inputs = tokenizer(prompt, return_tensors="pt")
            input_ids = inputs["input_ids"].to('cuda')
            generation_config = GenerationConfig(
                temperature=temperature,
                top_p=top_p,
                top_k=top_k,
                num_beams=num_beams,
                **kwargs,
            )

            # Without streaming
            with torch.no_grad():
                generation_output = model.generate(
                    input_ids=input_ids,
                    generation_config=generation_config,
                    return_dict_in_generate=True,
                    output_scores=True,
                    max_new_tokens=max_new_tokens,
                )
            s = generation_output.sequences[0]
            output = tokenizer.decode(s)
            response =  prompter.get_response(output)
            return response.split("### Instruction:")[0].strip()

        input_text = get_payload_messages(reqData)
        log.info("got input_text , %s" % input_text)
        result = evaluate(input_text)
        return input_text, result

class ChatGlmWrapper(WrapperFactory):
    def __init__(self, pretrained_name,base_model_path,tokenizer_path,finetune_type,infer_type) -> None:
        super().__init__(pretrained_name,base_model_path,tokenizer_path,finetune_type,infer_type)

    def load_model_tokenizer(self):
        from transformers import AutoTokenizer,AutoConfig,AutoModel,BitsAndBytesConfig
        tokenizer = AutoTokenizer.from_pretrained(
            self.base_model_path,
            use_fast=False,
            padding_side="left",
            trust_remote_code=True
        )

        model_config = AutoConfig.from_pretrained(self.base_model_path,trust_remote_code=True)
        if self.finetune_type == 'qlora':
            model = AutoModel.from_pretrained(
                self.base_model_path,
                config=model_config,
                torch_dtype=torch.float16,
                low_cpu_mem_usage=True,
                load_in_4bit=True,
                device_map={"": 0}, 
                trust_remote_code=True,
                quantization_config= BitsAndBytesConfig(
                    load_in_4bit=True,
                    bnb_4bit_compute_dtype=torch.float16,
                    bnb_4bit_use_double_quant=True,
                    bnb_4bit_quant_type='nf4'))
        else:
            model = AutoModel.from_pretrained(self.base_model_path, config=model_config, torch_dtype=torch.float16,
                                            trust_remote_code=True, device_map={"": 0})
        model.requires_grad_(False) # fix all model params
        model = model.cuda()
        model.eval()
        assert tokenizer.eos_token_id is not None, "Please update the *.json and *.py files of ChatGLM-6B from HuggingFace."

        self.model = model
        self.tokenizer = tokenizer

    def load_peft_model(self,lora_weight_path,patch_id):
        from peft import PeftModel
        if self.first_load_peft == True:
            self.model = PeftModel.from_pretrained(self.model, lora_weight_path, adapter_name=patch_id)
            self.first_load_peft = False
        else:
            self.model.load_adapter(lora_weight_path, patch_id)
        self.model.requires_grad_(False) # fix all model params
        self.model = self.model.half() # cast all params to float16 for inference
        self.model = self.model.cuda()
        self.model.eval()
    
    def trained_predict(self, reqData: DataListCls, lora_weight, patch_id, stream_cls):
        tokenizer = self.tokenizer
        model = self.model

        if self.finetune_type == 'lora' or self.finetune_type == 'qlora':
            model.load_adapter(lora_weight,patch_id)
            model.set_adapter(str(patch_id))

        instruction = get_payload_messages(reqData)

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
            cur_state = DataNone
            index = 0
            for new_text in streamer:
                if stream_cls:
                    cur_state = transform_stream_state(cur_state, streamer.print_len, new_text)
                    stream_cls.on_stream_infer(new_text,cur_state,index,0,0)
                response += new_text
                index = index+1 if new_text and cur_state != DataNone else index
            if stream_cls and cur_state == DataContinue:
                stream_cls.on_stream_infer('.',DataEnd,index,self.get_tokens(instruction),self.get_tokens(response))
            return response

        result = evalute(instruction)
        log.info(f'got result {result}')
        return instruction, result


class ChineseAlpacaWrapper(WrapperFactory):
    def __init__(self, pretrained_name,base_model_path,tokenizer_path,finetune_type,infer_type) -> None:
        super().__init__(pretrained_name,base_model_path,tokenizer_path,finetune_type,infer_type)

    def load_model_tokenizer(self):
        from transformers import LlamaTokenizer,AutoConfig,LlamaForCausalLM,BitsAndBytesConfig
        tokenizer = LlamaTokenizer.from_pretrained(self.tokenizer_path)

        if (len(tokenizer)) == 55296: #v2 49954:v1
            from ailab.utils.attn_and_long_ctx_patches import apply_attention_patch, apply_ntk_scaling_patch
            apply_attention_patch(use_memory_efficient_attention=True)
            apply_ntk_scaling_patch(1.0)
        if self.finetune_type == 'qlora':
            model_config = AutoConfig.from_pretrained(self.base_model_path,trust_remote_code=True)
            base_model = LlamaForCausalLM.from_pretrained(
                self.base_model_path,
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
            base_model = LlamaForCausalLM.from_pretrained(
                self.base_model_path,
                load_in_8bit=False,
                torch_dtype=torch.float16,
                low_cpu_mem_usage=True,
                device_map='auto',
                )

        model_vocab_size = base_model.get_input_embeddings().weight.size(0)
        tokenzier_vocab_size = len(tokenizer)
        log.info(f"Vocab of the base model: {model_vocab_size}")
        log.info(f"Vocab of the tokenizer: {tokenzier_vocab_size}")
        if model_vocab_size!=tokenzier_vocab_size:
            assert tokenzier_vocab_size > model_vocab_size
            log.info("Resize model embeddings to fit tokenizer")
            base_model.resize_token_embeddings(tokenzier_vocab_size)

        self.model = base_model
        self.tokenizer = tokenizer

    def evaluate(self, instruction: str, model , tokenizer, stream_cls) -> str:
        # The prompt template below is taken from llama.cpp
        # and is slightly different from the one used in training.
        # But we find it gives better results
        if (len(tokenizer)) == 49954:
            prompt_input = (
                "Below is an instruction that describes a task. "
                "Write a response that appropriately completes the request.\n\n"
                "### Instruction:\n\n{instruction}\n\n### Response:\n\n"
            )
            def generate_prompt(instruction, input=None):
                if input:
                    instruction = instruction + '\n' + input
                return prompt_input.format_map({'instruction': instruction})
        elif (len(tokenizer)) == 55296:
            prompt_input = (
                "[INST] <<SYS>>\n"
                "{system_prompt}\n"
                "<</SYS>>\n\n"
                "{instruction} [/INST]"
            )
            DEFAULT_SYSTEM_PROMPT = """You are a helpful assistant. 你是一个乐于助人的助手。"""
            def generate_prompt(instruction, system_prompt=DEFAULT_SYSTEM_PROMPT):
                return prompt_input.format_map({'instruction': instruction,'system_prompt': system_prompt})

        with torch.no_grad():
            input_text = generate_prompt(instruction=instruction)
            inputs = tokenizer(input_text,return_tensors="pt")  #add_special_tokens=False ?
            input_ids = inputs["input_ids"].to(model.device)
            attention_mask = inputs['attention_mask'].to(model.device)

            from transformers import TextIteratorStreamer
            streamer = TextIteratorStreamer(tokenizer, timeout=60.0, skip_prompt=True, skip_special_tokens=True)
            gen_kwargs = {
                "input_ids": input_ids,
                "streamer": streamer,
                "attention_mask":attention_mask,
                "eos_token_id":tokenizer.eos_token_id,
                "pad_token_id":tokenizer.pad_token_id,
                "temperature" :0.2,
                "top_k":40,
                "top_p":0.9,
                "do_sample":True,
                "num_beams":1,
                "repetition_penalty":1.3,
                "max_new_tokens":400,
            }

            thread = Thread(target=model.generate, kwargs=gen_kwargs)
            thread.start()

            response = ""
            cur_state = DataNone
            index = 0
            for new_text in streamer:
                if stream_cls:
                    cur_state = transform_stream_state(cur_state, streamer.print_len, new_text)
                    stream_cls.on_stream_infer(new_text,cur_state,index,0,0)
                response += new_text
                index = index+1 if new_text and cur_state != DataNone else index
            if stream_cls and cur_state == DataContinue:
                stream_cls.on_stream_infer('.',DataEnd,index,self.get_tokens(input_text),self.get_tokens(response))
            log.info(f'got result {response}')
            return response

    def base_predict(self, reqData: DataListCls, stream_cls):
        tokenizer = self.tokenizer
        model = self.model

        if hasattr(model, 'disable_adapter'):
            with model.disable_adapter():
                input_text = get_payload_messages(reqData)
                log.info("got input_text , %s" % input_text)
                return input_text, self.evaluate(input_text,model,tokenizer, stream_cls)
        else:
            input_text = get_payload_messages(reqData)
            log.info("got input_text , %s" % input_text)
            return input_text, self.evaluate(input_text,model,tokenizer, stream_cls)

    def trained_predict(self, reqData: DataListCls, lora_weight, patch_id, stream_cls):
        tokenizer = self.tokenizer
        model = self.model

        if self.finetune_type == 'lora' or self.finetune_type == 'qlora':
            model.load_adapter(lora_weight,patch_id)
            model.set_adapter(str(patch_id))

        instruction = get_payload_messages(reqData)
        return instruction, self.evaluate(instruction,self.model,tokenizer, stream_cls)

class EfficientWrapper(WrapperFactory):
    def __init__(self, pretrained_name,base_model_path,tokenizer_path,finetune_type,infer_type) -> None:
        super().__init__(pretrained_name,base_model_path,tokenizer_path,finetune_type,infer_type)

    def load_model_tokenizer(self):
        from transformers import AutoTokenizer,AutoConfig,AutoModelForCausalLM,BitsAndBytesConfig
        tokenizer = AutoTokenizer.from_pretrained(self.tokenizer_path, trust_remote_code=True)
        if self.finetune_type == 'qlora':
            import torch
            model_config = AutoConfig.from_pretrained(self.base_model_path,trust_remote_code=True)
            model = AutoModelForCausalLM.from_pretrained(
                self.base_model_path,
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
            model = AutoModelForCausalLM.from_pretrained(self.base_model_path, device_map="auto", trust_remote_code=True)
        self.model = model
        self.tokenizer = tokenizer

    def trained_predict(self, reqData: DataListCls, lora_weight, patch_id, stream_cls):
        model_name = self.pretrained_name
        tokenizer = self.tokenizer
        model = self.model
        if self.finetune_type == 'lora' or self.finetune_type == 'qlora':
            model.load_adapter(lora_weight,patch_id)
            model.set_adapter(str(patch_id))

        input_text = get_payload_messages(reqData)
        log.info("got input_text , %s" % input_text)

        from transformers import TextIteratorStreamer
        from ailab.utils.template import get_template_and_fix_tokenizer
        from ailab.atp_finetuner.constant import Model
        import torch

        template_dict = {
            Model.baichuan_7b : "default",
            Model.baichuan_13b : "default",
            Model.bloomz_7b1_mt : "default",
            Model.falcon_7b : "default",
            Model.falcon_7b_instruct : "falcon",
            Model.moss_moon_003_base : "moss",
            Model.llama2_7b : "llama2",
            Model.llama2_7b_chat_hf : "llama2",
            Model.llama2_13b_chat_hf : "llama2",
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
            index = 0
            for new_text in streamer:
                if stream_cls:
                    cur_state = transform_stream_state(cur_state, streamer.print_len, new_text)
                    stream_cls.on_stream_infer(new_text,cur_state,index,0,0)
                response += new_text
                index = index+1 if new_text and cur_state != DataNone else index
            if stream_cls and cur_state == DataContinue:
                stream_cls.on_stream_infer('.',DataEnd,index,self.get_tokens(input_text),self.get_tokens(response))
            return response

        result = predict_and_print(input_text)
        log.info("got result , %s" % result)
        return input_text, result

    
# 定义服务推理逻辑
class Wrapper(WrapperBase):
    serviceId = "atp"
    version = "v1"
    requestCls = UserRequest()
    responseCls = UserResponse()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filelogger = None
        self.patch_id = {}
        self.wrapper_cls = None
        self.lock = threading.Lock()

    def wrapperInit(self, config: {}) -> int:
        self.pretrained_name = os.environ.get("PRETRAINED_MODEL_NAME")
        tokenizer_path = os.environ.get("TOKENIZER_PATH")
        base_model_path = os.environ.get("FULL_MODEL_PATH")
        finetune_type = os.environ.get("FINETUNE_TYPE",'lora')
        infer_type = os.environ.get("INFER_TYPE")

        if not os.path.isdir(base_model_path):
            log.error(f"not find the base_model in {base_model_path}")
            return -1
        if not base_model_path or not tokenizer_path:
            log.error("should have environ")
            return -1
        self.wrapper_cls = WrapperFactory.create_wrapper_cls(self.pretrained_name,base_model_path,tokenizer_path,finetune_type,infer_type)
        self.wrapper_cls.load_model_tokenizer()
        self.finetune_type = finetune_type
        self.filelogger = getFileLogger()
        session_total = int(config.get("common.lic", 0))
        if session_total > 0:
            init_rq()
            self.session.init_wrapper_config(config)
            self.session.init_handle_pool("thread", 1, MyReqDataThread)
        return 0
    
    def checkValidLora(self, pretrained_name, lora_path):
        confjson = "adapter_config.json"
        files = os.listdir(lora_path)
        if not os.path.isdir(lora_path):
            msg = "not find  %s"%lora_path
            log.error(msg)
            return False, msg
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
        
    def wrapperLoadRes(self, reqData: DataListCls, patch_id) -> int:
        if patch_id in self.patch_id:
            log.warn("patch_id has exist.Please first to UnloadRes")
            return 0
        lora_weight_path = "/home/.atp/lora_weight/"
        lora_weight_path = os.path.join(lora_weight_path, str(patch_id))
        #if os.path.exists(lora_weight_path):
        #    log.error("zip file has exist.Please first to UnloadRes")
        #    return -1

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
        self.wrapper_cls.load_peft_model(lora_weight_path,patch_id)
        self.patch_id[patch_id] = lora_weight_path
        self.lock.release()
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
    
    def wrapperOnceExec(self, params: {}, reqData: DataListCls, usrTag:str="",persId: int = 0) -> Response:
        self.filelogger.info("got reqdata , %s" % reqData.list)
        self.lock.acquire()
        atp_patch_id = params.get('patch_id', 0)
        if atp_patch_id == 0 or atp_patch_id == '0':
            lora_weight = None
        else:
            lora_weight = self.patch_id[atp_patch_id]
        input, result = self.wrapper_cls.once_infer(params,reqData,lora_weight,None)
        self.lock.release()
        res= Response()
        if not result:
            self.filelogger.info("no result")
            return res.response_err(100)

        # 使用Response封装result
        content = resp_content(Once,0,result)
        usage = resp_usage(Once,self.wrapper_cls.get_tokens(input),self.wrapper_cls.get_tokens(result))
        if callback_metric:
            ret = callback_metric(usrTag, "business.total", 1)
            self.filelogger.info("calc business.total, count: %d " %ret)
        res.list = [content, usage]
        return res

    def wrapperOnceExecAsync(self, params: {}, reqData: DataListCls, sid: str, persId: int = 0):
        self.filelogger.info("got reqdata , %s" % reqData.list)
        self.lock.acquire()
        atp_patch_id = params.get('patch_id', 0)
        if atp_patch_id == 0 or atp_patch_id == '0':
            lora_weight = None
        else:
            lora_weight = self.patch_id[atp_patch_id]
        input, result = self.wrapper_cls.once_infer(params,reqData,lora_weight,None)
        self.lock.release()
        if not result:
            self.filelogger.info("no result")
            return -1
        res= Response()
        content = resp_content(Once,0,result)
        usage = resp_usage(Once,self.wrapper_cls.get_tokens(input),self.wrapper_cls.get_tokens(result))
        res.list = [content, usage]
        callback(res, sid)
        return 0

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
            s.error_code = -1
            s.handle = ""
            return s
        params['wrapper'] = self.wrapper_cls
        if self.finetune_type == 'lora' or self.finetune_type == 'qlora':
            params['patch_id'] = persId
            if persId == 0 or persId == '0':
                params['lora_weight'] = None
            else:
                params['lora_weight'] = self.patch_id[persId]
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

    def on_stream_infer(self, text, state, index, prompt_token, completion_token):
        if text and state != DataNone:
            res= Response()
            # 使用Response封装result
            content = resp_content(state,index,text)
            if state != DataEnd:
                res.list = [content]
                self.session_thread.callback_fn(res, self.session_thread.sid)
            else:
                usage = resp_usage(state,prompt_token,completion_token)
                res.list = [content,usage]
                self.session_thread.callback_fn(res, self.session_thread.sid)
                self.session_thread.reset()

    def infer(self, reqData: DataListCls):
        params = self.session_thread.params
        wrapper_cls = params['wrapper']
        lora_weight = params.get('lora_weight',None)
        wrapper_cls.once_infer(params,reqData,lora_weight,self)

    def run(self):
        while not self.is_stopping:
            try:
                req = self.in_q.get(timeout=5)
                self.infer(req)
            except queue.Empty as e:
                pass


        
    