import argparse, subprocess, torch, os
import json
from ailab.log import logger
from ailab.atp_finetuner.constant import Model

try:
    import jsonlines
except ImportError:
    print("jsonlines not install.please use 'pip install jsonlines'")

def read_input_file(input_file_path:str):
    lines = []

    def load_txt_file(txt_file):
        txt_lines = []
        try:
            with open(txt_file, "r", encoding="utf-8") as file:
                for line in file:
                    # 去除行尾的换行符并添加到数组中
                    if len(line) > 1:
                        txt_lines.append(line.strip())
        except FileNotFoundError:
            logger.error(f"file '{txt_file}' not found.")
        return txt_lines
    
    if os.path.isfile(input_file_path):
        lines = load_txt_file(input_file_path)
    elif os.path.isdir(input_file_path):
        for root, _, files in os.walk(input_file_path):
            for filename in files:
                file_path = os.path.join(root, filename)
                if file_path.endswith('txt'):
                    lines.extend(load_txt_file(file_path))
    return lines

def write_output_file(output_file_path:str, querys:[], answers:[]):
    with jsonlines.open(output_file_path, 'w') as jsonl_file:
        for query, answer in zip(querys, answers):
            json_object = {"input": query, "output": answer}
            jsonl_file.write(json_object)

def common_base_model_pipeline(model, tokenizer, args):
    output_file_path = args.base_result_path
    input_file_path = args.test_dataset_path

    querys = read_input_file(input_file_path)
    answers = []
    prompt_model = [Model.atom_7b]
    if args.pretrained_model_name in prompt_model:
        from ailab.utils.template import Template
        template_dict = {
            Model.atom_7b: "atom",
        }
        prompt_template = Template(template_dict.get(args.pretrained_model_name))

    for input_text in querys:
        logger.info("base Instruction:", input_text)
        if args.pretrained_model_name in prompt_model:
            history = []
            input_text = prompt_template.get_prompt(input_text, history, "")
        inputs = tokenizer(input_text, return_tensors='pt')
        gen_kwargs = {
                "max_new_tokens": 512,
                "repetition_penalty": 1.1,
            }
        input_text_skip_st = tokenizer.decode(inputs.input_ids[0], skip_special_tokens=True)
        inputs = inputs.input_ids
        inputs = inputs.to(model.device)
        output = model.generate(inputs, **gen_kwargs)
        output = tokenizer.decode(output[0], skip_special_tokens=True)
        if output.startswith(input_text_skip_st):
            output = output[len(input_text_skip_st):]
        output = output.strip()
        logger.info("base output:", output)
        answers.append(output)
    write_output_file(output_file_path, querys, answers)

def llama_base_model_inference(model, tokenizer, input_file_path, output_file_path):
    querys = read_input_file(input_file_path)
    answers = []
    for input_text in querys:
        inputs = tokenizer(input_text, return_tensors='pt')
        inputs = inputs.to(model.device)
        from transformers import TextIteratorStreamer
        streamer = TextIteratorStreamer(tokenizer, timeout=60.0, skip_prompt=True, skip_special_tokens=True)
        gen_kwargs = {
                "streamer" : streamer,
                "temperature": 0.1,
                "top_p": 0.75,
                "top_k": 40,
                "num_beams": 1,
                "max_new_tokens": 128,
            }
        input_text_skip_st = tokenizer.decode(inputs.input_ids[0], skip_special_tokens=True)
        output = model.generate(**inputs, **gen_kwargs)
        output = tokenizer.decode(output[0].tolist(), skip_special_tokens=True)
        if output.startswith(input_text_skip_st):
            output = output[len(input_text_skip_st):]
        # output = output.lstrip(input_text).strip()
        output = output.strip()
        logger.info(f'instruction: {input_text}')
        logger.info(f'response: {output}')
        answers.append(output)
    write_output_file(output_file_path, querys, answers)


def alpaca_model_inference(model, tokenizer, input_file_path, output_file_path):
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
        max_new_tokens=256,
        stream_output=False,
        **kwargs,
    ):
        prompt = prompter.generate_prompt(instruction, input)
        inputs = tokenizer(prompt, return_tensors="pt")
        input_ids = inputs["input_ids"].to(model.device)
        from transformers import GenerationConfig
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

    querys = read_input_file(input_file_path)
    answers = []
    for input_text in querys:
        result = evaluate(input_text)
        logger.info(f'instruction: {input_text}')
        logger.info(f'response: {result}')
        answers.append(result)
    write_output_file(output_file_path, querys, answers)

def chatglm_base_model_pipeline(model, tokenizer, args):
    output_file_path = args.base_result_path
    input_file_path = args.test_dataset_path
    querys = read_input_file(input_file_path)
    answers = []

    for input_text in querys:
        response, history = model.chat(tokenizer, input_text, history=[])
        answers.append(response)
    write_output_file(output_file_path, querys, answers)


def load_chatglm_model_tokenizer(model_path,tokenizer_path,is_qlora=False):
    from transformers import AutoTokenizer,AutoConfig,AutoModel,BitsAndBytesConfig
    tokenizer = AutoTokenizer.from_pretrained(
        tokenizer_path,
        use_fast=False,
        padding_side="left",
        trust_remote_code=True
    )

    config = AutoConfig.from_pretrained(model_path,trust_remote_code=True)
    if is_qlora:
        model = AutoModel.from_pretrained(
            model_path,
            config=config,
            torch_dtype=torch.float16,
            low_cpu_mem_usage=True,
            load_in_4bit=True,
            trust_remote_code=True, 
            device_map="auto",
            quantization_config= BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_compute_dtype=torch.float16,
                bnb_4bit_use_double_quant=True,
                bnb_4bit_quant_type='nf4'))
    else:
        model = AutoModel.from_pretrained(model_path, config=config, 
                                        trust_remote_code=True, device_map="auto", torch_dtype=torch.float16)
    assert tokenizer.eos_token_id is not None, "Please update the *.json and *.py files of ChatGLM-6B from HuggingFace."
    model.requires_grad_(False) # fix all model params
    model = model.cuda()
    model.eval()
    return model,tokenizer

#chatglm1 and chatglm2
def chatglm_pipeline(args):
    os.environ["CUDA_VISIBLE_DEVICES"] = "0"

    base_model,base_tokenizer = load_chatglm_model_tokenizer(args.pretrained_model_path, args.tokenizer_path)
    chatglm_base_model_pipeline(base_model,base_tokenizer,args)

    if args.finetune_type == 'full':
        model,tokenizer = load_chatglm_model_tokenizer(args.fintuned_weights,args.fintuned_weights)

    from peft import PeftModel
    if args.finetune_type == 'lora':
        tokenizer = base_tokenizer
        model = PeftModel.from_pretrained(base_model, args.fintuned_weights)

    if args.finetune_type == 'qlora':
        model,tokenizer = load_chatglm_model_tokenizer(args.pretrained_model_path, args.tokenizer_path, True)
        model = PeftModel.from_pretrained(model, args.fintuned_weights)

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

    querys = read_input_file(args.test_dataset_path)
    answers = []

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

    for instruction in querys:
        response = evalute(instruction)
        logger.info(f'instruction {instruction}')
        logger.info(f'response {response}')
        answers.append(response)
    write_output_file(args.finetuned_result_path, querys, answers)

def chinese_alpaca_inference(model, tokenizer, input_file_path, output_file_path):
    model.eval()

    device = torch.device(0)
    def evaluate(instruction: str) -> str:
        generation_config = dict(
            temperature=0.2,
            top_k=40,
            top_p=0.9,
            do_sample=True,
            num_beams=1,
            repetition_penalty=1.1,
            max_new_tokens=512,
            )

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
            input_ids = inputs["input_ids"].to(device)
            attention_mask = inputs['attention_mask'].to(device)
            generation_output = model.generate(
                input_ids = input_ids, 
                attention_mask = attention_mask,
                eos_token_id=tokenizer.eos_token_id,
                pad_token_id=tokenizer.pad_token_id,
                **generation_config
            )
        s = generation_output[0]
        output = tokenizer.decode(s,skip_special_tokens=True)
        if (len(tokenizer)) == 49954:
            response = output.split("### Response:")[1].strip()
        else:
            response = output.split("[/INST]")[-1].strip()
        return response

    querys = read_input_file(input_file_path)
    answers = []
    
    for instruction in querys:
        logger.info("Instruction:", instruction)
        response = evaluate(instruction)
        logger.info("Response:", response)
        answers.append(response)
    write_output_file(output_file_path, querys, answers)

def load_alpaca_model_tokenizer(model_path, tokenizer_path, load_in_8bit=False,is_qlora=False):
    from transformers import LlamaForCausalLM,LlamaTokenizer,AutoConfig,BitsAndBytesConfig
    tokenizer = LlamaTokenizer.from_pretrained(tokenizer_path) #, legacy=False
    if (len(tokenizer)) == 55296: #v2 49954:v1
        from ailab.utils.attn_and_long_ctx_patches import apply_attention_patch, apply_ntk_scaling_patch
        apply_attention_patch(use_memory_efficient_attention=True)
        apply_ntk_scaling_patch("1.0")

    if is_qlora:
        config = AutoConfig.from_pretrained(model_path)
        model = LlamaForCausalLM.from_pretrained(
            model_path,
            config=config,
            torch_dtype=torch.float16,
            low_cpu_mem_usage=True,
            load_in_4bit=True,
            trust_remote_code=True, 
            device_map="auto",
            quantization_config= BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_compute_dtype=torch.float16,
                bnb_4bit_use_double_quant=True,
                bnb_4bit_quant_type='nf4'))
    else:
        model = LlamaForCausalLM.from_pretrained(
            model_path, 
            torch_dtype=torch.float16,
            load_in_8bit=load_in_8bit,
            low_cpu_mem_usage=True,
            device_map='auto',
            )
    
    # unify tokenizer and embedding size
    model_vocab_size = model.get_input_embeddings().weight.size(0)
    tokenzier_vocab_size = len(tokenizer)
    logger.info(f"Vocab of the base model: {model_vocab_size}")
    logger.info(f"Vocab of the tokenizer: {tokenzier_vocab_size}")
    if model_vocab_size!=tokenzier_vocab_size:
        assert tokenzier_vocab_size > model_vocab_size
        logger.info("Resize model embeddings to fit tokenizer")
        model.resize_token_embeddings(tokenzier_vocab_size)

    return model, tokenizer
    

def chinese_llama_alpaca_pipeline(args):
    base_model, base_tokenizer = load_alpaca_model_tokenizer(args.pretrained_model_path,args.tokenizer_path, True)
    if args.pretrained_model_name == Model.chinese_alpaca:
        llama_base_model_inference(base_model, base_tokenizer, args.test_dataset_path, args.base_result_path)
    else:
        chinese_alpaca_inference(base_model, base_tokenizer, args.test_dataset_path, args.base_result_path)

    if args.finetune_type == 'full':
        model, tokenizer = load_alpaca_model_tokenizer(args.fintuned_weights,args.fintuned_weights)
        
    from peft import PeftModel
    if args.finetune_type == 'lora':
        model = PeftModel.from_pretrained(base_model, 
                                    args.fintuned_weights,
                                    torch_dtype=torch.float16,
                                    device_map='auto',)
        tokenizer = base_tokenizer

    if args.finetune_type == 'qlora':
        model, tokenizer = load_alpaca_model_tokenizer(args.pretrained_model_path,args.tokenizer_path, True)
        model = PeftModel.from_pretrained(model, 
                                    args.fintuned_weights,
                                    torch_dtype=torch.float16,
                                    device_map='auto',)
        
    chinese_alpaca_inference(model, tokenizer, args.test_dataset_path, args.finetuned_result_path)

def llama_alpaca_pipeline(args):
    base_model, base_tokenizer = load_alpaca_model_tokenizer(args.pretrained_model_path,args.tokenizer_path)
    base_tokenizer.pad_token_id = 0
    
    llama_base_model_inference(base_model, base_tokenizer, args.test_dataset_path, args.base_result_path)
    if args.finetune_type == 'full':
        model, tokenizer = load_alpaca_model_tokenizer(args.fintuned_weights,args.fintuned_weights)
    if args.finetune_type == 'lora':
        from peft import PeftModel
        model = PeftModel.from_pretrained(base_model, args.fintuned_weights, torch_dtype=torch.float16, device_map='auto',)
        model.config.pad_token_id = 0  # unk
        model.config.bos_token_id = 1
        model.config.eos_token_id = 2
        model.eval()
        tokenizer = base_tokenizer
    alpaca_model_inference(model, tokenizer, args.test_dataset_path, args.finetuned_result_path)

def load_efficient_model_tokenizer(model_path, tokenizer_path,is_qlora=False):
    from transformers import AutoTokenizer,AutoModelForCausalLM,AutoConfig,BitsAndBytesConfig
    tokenizer = AutoTokenizer.from_pretrained(tokenizer_path, trust_remote_code=True)
    if is_qlora:
        config = AutoConfig.from_pretrained(model_path,trust_remote_code=True)
        model = AutoModelForCausalLM.from_pretrained(
            model_path,
            config=config,
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
        model = AutoModelForCausalLM.from_pretrained(model_path, device_map="auto", trust_remote_code=True)
    return model, tokenizer

def LLaMA_Efficient_Tuning_pipeline(args):
    from transformers import TextIteratorStreamer
    from threading import Thread

    base_model,tokenizer = load_efficient_model_tokenizer(args.pretrained_model_path,args.tokenizer_path)
    common_base_model_pipeline(base_model,tokenizer,args)

    if args.finetune_type == 'full':
        model,tokenizer = load_efficient_model_tokenizer(args.fintuned_weights,args.fintuned_weights)

    from peft import PeftModel
    if args.finetune_type == 'lora':
        model = PeftModel.from_pretrained(base_model, args.fintuned_weights)

    if args.finetune_type == 'qlora':
        model,tokenizer = load_efficient_model_tokenizer(args.pretrained_model_path,args.tokenizer_path,True)
        model = PeftModel.from_pretrained(model, args.fintuned_weights)

    from ailab.utils.template import get_template_and_fix_tokenizer
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
        Model.bloomz_1b1 : "default",
        Model.bloomz_3b : "default",
        Model.codellama_7b_instruction : "default",
        Model.codellama_13b_instruction : "default",
        Model.atom_7b: "atom",
        Model.chatglm3_6b: "chatglm3",
    }
    prompt_template = get_template_and_fix_tokenizer(template_dict.get(args.pretrained_model_name),tokenizer)

    def predict_and_print(query) -> list:
        history = []
        prompt, _ = prompt_template.encode_oneturn(
            tokenizer=tokenizer, query=query, resp="", history=history, system=None
        )
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
        for new_text in streamer:
            response += new_text

        return response
    
    querys = read_input_file(args.test_dataset_path)
    answers = []
    for instruction in querys:
        logger.info("Instruction:", instruction)
        response = predict_and_print(instruction)
        logger.info("Response:", response)
        answers.append(response)
    write_output_file(args.finetuned_result_path, querys, answers)

def ziya_pipeline(args):
    import torch
    from peft import PeftModel
    from transformers import LlamaForCausalLM, AutoTokenizer, AutoConfig, AutoModelForCausalLM, BitsAndBytesConfig
    from typing import List
    import torch.nn.functional as F

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

    queries = read_input_file(args.test_dataset_path)
    tokenizer_path = args.tokenizer_path
    llama_tokenizer = AutoTokenizer.from_pretrained(tokenizer_path)
    generate_kwargs = {
        "do_sample": True,
        "top_p": 1.0,
        "top_k": 0,
        "max_length": 2048,
        "repetition_penalty": 1.0,
        "temperature": 0.8,
        "pad_token_id": llama_tokenizer.eos_token_id,
        "eos_token_id": llama_tokenizer.eos_token_id,
    }
    def merge_lora_to_base_model(args):
        model_name_or_path = args.pretrained_model_path
        adapter_name_or_path = args.fintuned_weights
        model1 = AutoModelForCausalLM.from_pretrained(
            model_name_or_path,
            trust_remote_code=True,
            low_cpu_mem_usage=True,
            torch_dtype=torch.float16,
            device_map="auto",
        )
        if adapter_name_or_path is not None:
            model2 = PeftModel.from_pretrained(
                model1,
                adapter_name_or_path,
                device_map="auto",
            )
            # model = model.merge_and_unload()
        return model1, model2
    model1,model2 = merge_lora_to_base_model(args)
    ans1 = generate(queries=queries, tokenizer=llama_tokenizer, model=model1, device=0, **generate_kwargs)
    q1=[]
    a1=[]
    for i in ans1 :
        temp=i.split("<bot> :")
        q1.append(temp[0].strip("<human> :"))
        a1.append(temp[1])
    write_output_file(args.base_result_path, q1, a1)    
    ans2 = generate(queries=queries, tokenizer=llama_tokenizer, model=model2, device=0, **generate_kwargs)
    q2=[]
    a2=[]
    for i in ans2 :
        temp=i.split("<bot> :")
        q2.append(temp[0].strip("<human> :"))
        a2.append(temp[1])
    write_output_file(args.finetuned_result_path, q2, a2)

def image_classification_inference(model, image_processor, image_dir, result_path):
    if not os.path.isdir(image_dir):
        logger.error("input is not a valid directory , %s" % image_dir)
    querys = []
    answers = []
    for filename in os.listdir(image_dir):
        image_path = os.path.join(image_dir, filename)
        if not os.path.isfile(image_path):
            logger.error("input is not a valid file , %s" % image_path)
            continue
        if not image_path.endswith(('.jpg', '.jpeg', '.png', '.gif')):
            logger.error("input is not a picture (should jpg jpeg png gif), %s" % image_path)
            continue

        from PIL import Image
        # 打开图像文件
        image = Image.open(image_path)
        inputs = image_processor(image, return_tensors="pt")
        with torch.no_grad():
            logits = model(**inputs).logits

        predicted_label = logits.argmax(-1).item()
        predicted_name = model.config.id2label[predicted_label]
        querys.append(image_path)
        answers.append(predicted_name)
    write_output_file(result_path, querys, answers)

def image_classification_pipeline(args):
    base_model_path = args.pretrained_model_path
    full_model_path = args.fintuned_weights

    def load_model_and_imageprocessor(model_path):
        from transformers import AutoImageProcessor, AutoModelForImageClassification
        model = AutoModelForImageClassification.from_pretrained(model_path)
        image_processor = AutoImageProcessor.from_pretrained(model_path)
        return model,image_processor

    base_model, base_image_processor = load_model_and_imageprocessor(base_model_path)
    full_model, full_image_processor = load_model_and_imageprocessor(full_model_path)
    image_classification_inference(base_model, base_image_processor, args.test_dataset_path, args.base_result_path)
    image_classification_inference(full_model, full_image_processor, args.test_dataset_path, args.finetuned_result_path)

def object_detection_inference(model, image_processor, image_dir, result_path, save_pic=None):
    if not os.path.isdir(image_dir):
        logger.error("input is not a valid directory , %s" % image_dir)
    querys = []
    answers = []
    from PIL import Image, ImageDraw
    for filename in os.listdir(image_dir):
        file_path = os.path.join(image_dir, filename)
        if not os.path.isfile(file_path):
            continue
        # 检查文件类型是否为图像
        if not file_path.endswith(('.jpg', '.jpeg', '.png', '.gif')):
            continue
        # 打开图像文件
        image = Image.open(file_path)
        if image.mode != "RGB":
            image = image.convert("RGB")
        inputs = image_processor(image, return_tensors="pt")
        with torch.no_grad():
            outputs = model(**inputs)
            target_sizes = torch.tensor([image.size[::-1]])
            results = image_processor.post_process_object_detection(outputs, threshold=0.7, target_sizes=target_sizes)[0]

        if save_pic is not None:
            draw = ImageDraw.Draw(image)
        out_objects = []
        for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
            box = [round(i, 2) for i in box.tolist()]
            label_name = model.config.id2label[label.item()]
            confidence = round(score.item(), 3)
            logger.info(
                f"Detected {label_name} with confidence {confidence} at location {box}"
            )
            out_objects.append({
                'object': label_name,
                'confidence': confidence,
                'bbox': box,
            })
            if save_pic is not None:
                x, y, x2, y2 = tuple(box)
                draw.rectangle((x, y, x2, y2), outline="red", width=1)
                draw.text((x, y), f"{model.config.id2label[label.item()]} {round(score.item(), 3)}" + " ", fill="blue")

        if save_pic is not None:
            save_path = os.path.join(os.path.dirname(result_path), save_pic)
            if not os.path.exists(save_path):
                os.mkdir(save_path)
            save_file = os.path.join(save_path, filename)
            image.save(save_file)

        querys.append(file_path)
        answers.append(json.dumps(out_objects))
    write_output_file(result_path, querys, answers)

def object_detection_pipeline(args):
    base_model_path = args.pretrained_model_path
    full_model_path = args.fintuned_weights

    def load_model_and_imageprocessor(model_path):
        from transformers import AutoImageProcessor, AutoModelForObjectDetection
        model = AutoModelForObjectDetection.from_pretrained(model_path)
        image_processor = AutoImageProcessor.from_pretrained(model_path)
        return model,image_processor

    base_model, base_image_processor = load_model_and_imageprocessor(base_model_path)
    full_model, full_image_processor = load_model_and_imageprocessor(full_model_path)
    object_detection_inference(base_model, base_image_processor, args.test_dataset_path, args.base_result_path)
    object_detection_inference(full_model, full_image_processor, args.test_dataset_path, args.finetuned_result_path, save_pic="new")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="An example script with command-line arguments.")
    parser.add_argument("--finetune_type", type=str, default=None, choices=['lora', 'full', 'qlora'])
    parser.add_argument("--pretrained_model_name", type=str, default=None)
    parser.add_argument("--pretrained_model_path", type=str, default=None)
    parser.add_argument("--tokenizer_path", type=str, default=None)
    parser.add_argument("--fintuned_weights", type=str, default=None)
    parser.add_argument("--test_dataset_path", type=str, default=None)
    parser.add_argument("--base_result_path", type=str, default=None)
    parser.add_argument("--finetuned_result_path", type=str, default=None)
    args = parser.parse_args()

    logger.info(args)

    args_dict = vars(args)  # 将 argparse 命名空间转换为字典
    for arg_name, arg_value in args_dict.items():
        if arg_value is None:
            raise SystemExit(f'{arg_name} is None')
        
    if not os.path.exists(args.pretrained_model_path) :
        raise SystemExit(f'args.pretrained_model_path {args.pretrained_model_path} not exist')
    elif not os.path.exists(args.tokenizer_path):
        raise SystemExit(f'args.tokenizer_path {args.tokenizer_path} not exist')
    elif not os.path.exists(args.test_dataset_path):
        raise SystemExit(f'args.test_dataset_path {args.test_dataset_path} not exist')
    elif args.fintuned_weights is not None and not os.path.exists(args.fintuned_weights):
        raise SystemExit(f'args.fintuned_weights {args.fintuned_weights} not exist')
    
    if not args.base_result_path.endswith('jsonl') or not args.finetuned_result_path.endswith('jsonl'):
        raise SystemExit('output file should be jsonl')

    efficent_model = [Model.baichuan_7b,Model.baichuan_13b,Model.bloomz_7b1_mt,Model.falcon_7b,Model.falcon_7b_instruct,
                      Model.moss_moon_003_base,Model.llama2_7b,Model.llama2_7b_chat_hf,Model.llama2_13b_chat_hf,
                      Model.internlm_7b,Model.belle_7b_2m,
                      Model.xverse_13b,Model.lawgpt_llama,Model.bloomz_3b,Model.bloomz_1b1,
                      Model.codellama_7b_instruction,Model.codellama_13b_instruction,Model.atom_7b,
                      Model.chatglm3_6b]
    glm_model = [Model.chatglm_6b,Model.chatglm2_6b,Model.code_geex_2]
    chinese_alpaca_model = [Model.chinese_alpaca,Model.chinese_alpaca_2,Model.chinese_alpaca_2_13b,
                            Model.chinese_alpaca_2_7b_16k,Model.chinese_alpaca_2_13b_16k,Model.chinese_alpaca_2_1b3]
    alpaca_model = [Model.alpaca,Model.vicuna,Model.bencao_llama]
    ziya_model = [Model.ziya_llama_13b]
    image_classification_model = [Model.vit_patch16_224_in21k]
    object_detection_model = [Model.yolos_base, Model.yolos_small]

    if args.pretrained_model_name in efficent_model:
        LLaMA_Efficient_Tuning_pipeline(args)
    elif args.pretrained_model_name in glm_model:
        chatglm_pipeline(args)
    elif args.pretrained_model_name in chinese_alpaca_model:
        chinese_llama_alpaca_pipeline(args)
    elif args.pretrained_model_name in alpaca_model:
        llama_alpaca_pipeline(args)
    elif args.pretrained_model_name in ziya_model:
        ziya_pipeline(args)
    elif args.pretrained_model_name in image_classification_model:
        image_classification_pipeline(args)
    elif args.pretrained_model_name in object_detection_model:
        object_detection_pipeline(args)
    else:
        raise SystemExit(f'model_name {args.pretrained_model_name} not support yeat')

    exit(0)
    