from typing import List
import torch
from transformers import AutoModelForCausalLM,AutoConfig, BitsAndBytesConfig
from peft import TaskType,LoraConfig,get_peft_model,PeftModel
from ailab.atp_finetuner.model.model import AILabModel
from ailab.atp_finetuner.build import ModelRg
from ailab.atp_finetuner.constant import Task, Model
from ailab.log import logger

@ModelRg.register((Task.question_answering, Model.baichuan_7b))
@ModelRg.register((Task.question_answering, Model.baichuan_13b))
@ModelRg.register((Task.question_answering, Model.bloomz_7b1_mt))
@ModelRg.register((Task.question_answering, Model.bloomz_3b))
@ModelRg.register((Task.question_answering, Model.bloomz_1b1))
@ModelRg.register((Task.question_answering, Model.falcon_7b))
@ModelRg.register((Task.question_answering, Model.falcon_7b_instruct))
@ModelRg.register((Task.question_answering, Model.moss_moon_003_base))
@ModelRg.register((Task.question_answering, Model.llama2_7b))
@ModelRg.register((Task.question_answering, Model.llama2_7b_chat_hf))
@ModelRg.register((Task.question_answering, Model.llama2_13b_chat_hf))
@ModelRg.register((Task.question_answering, Model.internlm_7b))
@ModelRg.register((Task.question_answering, Model.belle_7b_2m))
@ModelRg.register((Task.question_answering, Model.xverse_13b))
@ModelRg.register((Task.question_answering, Model.lawgpt_llama))
@ModelRg.register((Task.question_answering, Model.educhat))
@ModelRg.register((Task.question_answering, Model.codellama_7b_instruction))
@ModelRg.register((Task.question_answering, Model.codellama_13b_instruction))
@ModelRg.register((Task.question_answering, Model.atom_7b))
@ModelRg.register((Task.question_answering, Model.chatglm3_6b))
class BaichuanModel(AILabModel):
    def __init__(self, model: any) -> None:
        self.model_name = None
        super().__init__(model)

    def forward(self,**kwargs):
        model = self.model_ins
        finetune_type = kwargs['model_args'].get('finetune_type','lora')

        output_embedding_layer_name = "lm_head"
        layer_norm_names = ["norm", "ln_f", "ln_attn", "ln_mlp"]
        for name, param in model.named_parameters():
            if param.ndim == 1 and any(layer_norm_name in name for layer_norm_name in layer_norm_names):
                param.data = param.data.to(torch.float32)

        neft_alpha = kwargs['model_args'].get('neft_alpha', 0)
        if neft_alpha > 1e-6:
            input_embed = model.get_input_embeddings()
            if isinstance(input_embed, torch.nn.Embedding):
                def noisy_forward(self: torch.nn.Embedding, x: torch.Tensor) -> torch.Tensor:
                    embeddings = input_embed.__class__.forward(self, x)
                    if self.training:
                        dims = self.num_embeddings * self.embedding_dim
                        mag_norm = neft_alpha / (dims ** 0.5)
                        embeddings += torch.zeros_like(embeddings).uniform_(-mag_norm, mag_norm)
                    return embeddings
                
                from types import MethodType
                input_embed.forward = MethodType(noisy_forward, input_embed)
                logger.info("Using noisy embedding with alpha={:.2f}".format(neft_alpha))
            else:
                logger.warning("Input embeddings are not normal nn.Embedding, cannot transform into noisy embedding.")

        if hasattr(model, "enable_input_require_grads"):
            model.enable_input_require_grads()
        else:
            def make_inputs_require_grad(module, input, output):
                output.requires_grad_(True)
            model.get_input_embeddings().register_forward_hook(make_inputs_require_grad)

        model.gradient_checkpointing_enable()
        model.config.use_cache = False # turn off when gradient checkpointing is enabled

        if finetune_type != "full" and hasattr(model, output_embedding_layer_name):
            output_embedding_layer: torch.nn.Linear = getattr(model, output_embedding_layer_name)
            input_dtype = output_embedding_layer.weight.dtype

            class CastOutputToFloat(torch.nn.Sequential):
                def forward(self, x: torch.Tensor) -> torch.Tensor:
                    return super().forward(x.to(input_dtype)).to(torch.float32)

            setattr(model, output_embedding_layer_name, CastOutputToFloat(output_embedding_layer))

        if finetune_type == "full":
            model = model.float()

        if finetune_type == "lora" or finetune_type == "qlora":
            #for dpo
            checkpoints_dir = kwargs['model_args'].get('checkpoint_dir', None)
            if checkpoints_dir is not None:
                checkpoints_dir = checkpoints_dir.split(',')
                for checkpoint in checkpoints_dir:
                    model = PeftModel.from_pretrained(model, checkpoint)
                    model = model.merge_and_unload()

            #resume_from_latest_checkpoint
            resume_from_checkpoint = kwargs['train_args'].get('resume_from_checkpoint', False)
            if resume_from_checkpoint :
                output_dir = kwargs['train_args'].get('output_dir')
                from transformers.trainer_utils import get_last_checkpoint
                latest_checkpoint = get_last_checkpoint(output_dir)
                if latest_checkpoint:
                    logger.info(f"resume train from checkpoint:{latest_checkpoint}")
                    model = PeftModel.from_pretrained(model, latest_checkpoint)
                    model = model.merge_and_unload()

            if self.model_name in [Model.baichuan_7b,Model.baichuan_13b,]:
                lora_targets = ['W_pack']
            elif self.model_name in [Model.bloomz_7b1_mt,Model.bloomz_3b,Model.bloomz_1b1,Model.falcon_7b,Model.falcon_7b_instruct,
                                     Model.belle_7b_2m,Model.chatglm3_6b]:
                lora_targets = ['query_key_value']
            else:
                lora_targets = ['q_proj','v_proj']
            
            lora_config = LoraConfig(
                    task_type=TaskType.CAUSAL_LM,
                    inference_mode=False,
                    r=8,
                    lora_alpha=32.0,
                    lora_dropout=0.1,
                    target_modules=lora_targets,
                )
            model = get_peft_model(model, lora_config)

        from ailab.utils.other import print_trainable_params
        print_trainable_params(model)
        self._model = model
    
    @classmethod
    def build_model(cls, device_name:str, model_name:str, model_dir:str, **kwargs):
        # quantization args
        quantization_bit = kwargs.get('quantization_bit', None)
        quantization_type = kwargs.get('quantization_type', 'nf4')
        double_quantization = kwargs.get("double_quantization", True)
        compute_dtype = kwargs.get('compute_dtype', torch.float16)
        torch_dtype = kwargs.get('torch_dtype', torch.float16)
        
        #qlora 的配置参数
        config_kwargs = {"trust_remote_code": True} 

        model_name_or_dir = model_name if model_dir is None else model_dir
        config = AutoConfig.from_pretrained(model_name_or_dir, trust_remote_code=True)
        # Quantization configurations (using bitsandbytes library).
        if quantization_bit is not None:
            if quantization_bit == 8:
                config_kwargs["load_in_8bit"] = True
                config_kwargs["quantization_config"] = BitsAndBytesConfig(
                    load_in_8bit=True,
                )

            elif quantization_bit == 4:
                config_kwargs["load_in_4bit"] = True
                config_kwargs["quantization_config"] = BitsAndBytesConfig(
                    load_in_4bit=True,
                    bnb_4bit_compute_dtype=compute_dtype,
                    bnb_4bit_use_double_quant=double_quantization,
                    bnb_4bit_quant_type=quantization_type
                )

            logger.info("Quantizing model to {} bit.".format(quantization_bit))
            
        model = AutoModelForCausalLM.from_pretrained(
            model_name_or_dir,
            config=config,
            torch_dtype=torch_dtype,#QLoRA
            low_cpu_mem_usage=True,
            **config_kwargs,
        )

        if hasattr(config, "auto_map") and "AutoConfig" in config.auto_map:
            config.__class__.register_for_auto_class()
        if hasattr(config, "auto_map") and "AutoModelForCausalLM" in config.auto_map:
            model.__class__.register_for_auto_class()
        cls_model =  cls(model)
        cls_model.model_name = model_name
        return cls_model
    
    def get_inside_models(self, model_type:str):
        pass
