import transformers
from transformers import AutoTokenizer, AutoConfig
from ailab.atp_dataset.dataset import AILabDataset
from ailab.atp_finetuner.build import PreProcessorRg
from ailab.atp_finetuner.constant import Task, Model
from ailab.atp_finetuner.preprossor import AILabPreprocessor

@PreProcessorRg.register((Task.question_answering, Model.baichuan_7b))
@PreProcessorRg.register((Task.question_answering, Model.baichuan_13b))
@PreProcessorRg.register((Task.question_answering, Model.bloomz_7b1_mt))
@PreProcessorRg.register((Task.question_answering, Model.bloomz_3b))
@PreProcessorRg.register((Task.question_answering, Model.bloomz_1b1))
@PreProcessorRg.register((Task.question_answering, Model.falcon_7b))
@PreProcessorRg.register((Task.question_answering, Model.falcon_7b_instruct))
@PreProcessorRg.register((Task.question_answering, Model.moss_moon_003_base))
@PreProcessorRg.register((Task.question_answering, Model.llama2_7b))
@PreProcessorRg.register((Task.question_answering, Model.llama2_7b_chat_hf))
@PreProcessorRg.register((Task.question_answering, Model.llama2_13b_chat_hf))
@PreProcessorRg.register((Task.question_answering, Model.internlm_7b))
@PreProcessorRg.register((Task.question_answering, Model.belle_7b_2m))
@PreProcessorRg.register((Task.question_answering, Model.xverse_13b))
@PreProcessorRg.register((Task.question_answering, Model.lawgpt_llama))
@PreProcessorRg.register((Task.question_answering, Model.educhat))
@PreProcessorRg.register((Task.question_answering, Model.codellama_7b_instruction))
@PreProcessorRg.register((Task.question_answering, Model.codellama_13b_instruction))
@PreProcessorRg.register((Task.question_answering, Model.atom_7b))
@PreProcessorRg.register((Task.question_answering, Model.chatglm3_6b))
class BaichuanPreProcessor(AILabPreprocessor):
    def __init__(self, dataset, preprocessor):
        self.model_name = None
        super().__init__(dataset, preprocessor)

    @classmethod
    def build_preprocessor(cls, model_name:str, dataset: AILabDataset, pc_dir:str, **kwargs):
        pc_name_dir = model_name if pc_dir is None else pc_dir
        max_source_lenghth = kwargs['model_args'].get('max_source_length', 4096)

        padding_right_models = [Model.baichuan_13b,Model.falcon_7b_instruct]
        padding_side = 'right' if model_name in padding_right_models else 'left'
        tokenizer  = AutoTokenizer.from_pretrained(pc_name_dir,use_fast=False,
                                                   padding_side=padding_side,
                                                   trust_remote_code=True)
        if tokenizer.pad_token_id is None or tokenizer.pad_token_id == 64000: # 64000 for baichuan model (older version)
            tokenizer.pad_token_id = 0 # set as the <unk> token
        if "AutoTokenizer" in tokenizer.init_kwargs.get("auto_map", {}):
            tokenizer.__class__.register_for_auto_class()
        tokenizer_cls =  cls(dataset, tokenizer)
        tokenizer_cls.model_name = model_name
        tokenizer_cls._max_source_length = max_source_lenghth
        return tokenizer_cls

    def process_data(self) ->AILabDataset:
        tokenizer = self._preprocessor
        datasets = self._dataset.to_hf_dataset()

        for key,dataset in datasets.items():
            dummy_data = [None] * len(dataset)
            for column_name, target_name in [
                ("instruction", "prompt"),
                ("input", "query"),
                ("output", "response"),
                ("history", "history")
            ]: # every dataset will have 4 columns same as each other
                if column_name in dataset.column_names:
                    dataset = dataset.rename_column(column_name, target_name)
                    datasets[key] = dataset
                else:
                    dataset = dataset.add_column(target_name, dummy_data)
                    datasets[key] = dataset

        template_dict = {
            Model.baichuan_7b : "default",
            Model.baichuan_13b : "default",
            Model.bloomz_7b1_mt : "default",
            Model.bloomz_3b : "default",
            Model.bloomz_1b1 : "default",
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
            Model.educhat : "edu",
            Model.codellama_7b_instruction : "default",
            Model.codellama_13b_instruction : "default",
            Model.atom_7b : "atom",
            Model.chatglm3_6b : "chatglm3",
        }

        from ailab.utils.template import get_template_and_fix_tokenizer
        from typing import Dict,List,Generator,Any
        prompt_template = template_dict.get(self.model_name)
        template = get_template_and_fix_tokenizer(prompt_template, tokenizer)

        def construct_example(examples: Dict[str, List[Any]]) -> Generator[Any, None, None]:
            for i in range(len(examples["prompt"])):
                query, response = examples["prompt"][i], examples["response"][i]
                query = query + "\n" + examples["query"][i] if "query" in examples and examples["query"][i] else query
                history = examples["history"][i] if "history" in examples else None
                system = examples["system"][i] if "system" in examples else None
                yield query, response, history, system
        
        IGNORE_INDEX = -100
        max_source_length = self._max_source_length
        def preprocess_supervised_dataset(examples: Dict[str, List[Any]]) -> Dict[str, Any]:
            # build inputs with format `<bos> X Y <eos>` and labels with format `<ignore> ... <ignore> Y <eos>`
            # for multiturn examples, we only mask the prompt part in each prompt-response pair.
            model_inputs = {"input_ids": [], "attention_mask": [], "labels": []}

            for query, response, history, system in construct_example(examples):
                if not (isinstance(query, str) and isinstance(response, str) and query != "" and response != ""):
                    continue

                input_ids, labels = [], []
                for turn_idx, (source_ids, target_ids) in enumerate(template.encode_multiturn(
                    tokenizer, query, response, history, system
                )):
                    total_len = len(source_ids) + len(target_ids)
                    max_source_len = int(max_source_length * (len(source_ids) / total_len))
                    max_target_len = int(max_source_length * (len(target_ids) / total_len))

                    if len(source_ids) > max_source_len:
                        source_ids = source_ids[:max_source_len]
                    if len(target_ids) > max_target_len:
                        target_ids = target_ids[:max_target_len]

                    if turn_idx != 0 and template.efficient_eos:
                        source_mask = [tokenizer.eos_token_id] + [IGNORE_INDEX] * (len(source_ids) - 1)
                    else:
                        source_mask = [IGNORE_INDEX] * len(source_ids)

                    input_ids += source_ids + target_ids
                    labels += source_mask + target_ids

                if template.efficient_eos:
                    input_ids += [tokenizer.eos_token_id]
                    labels += [tokenizer.eos_token_id]

                if len(input_ids) > max_source_length:
                    input_ids = input_ids[:max_source_length]
                    labels = labels[:max_source_length]

                model_inputs["input_ids"].append(input_ids)
                model_inputs["attention_mask"].append([1] * len(input_ids))
                model_inputs["labels"].append(labels)

            return model_inputs
    
        tokenized_dataset = datasets.map(preprocess_supervised_dataset,
                                        batched=True,
                                        remove_columns=['prompt', 'query', 'response', 'history'],)
        return AILabDataset(tokenized_dataset)