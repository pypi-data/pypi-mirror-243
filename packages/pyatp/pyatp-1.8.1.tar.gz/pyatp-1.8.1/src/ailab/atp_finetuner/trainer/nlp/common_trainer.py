from typing import Dict, Optional
import os,torch
from transformers.trainer import TRAINING_ARGS_NAME, WEIGHTS_NAME
from transformers.modeling_utils import unwrap_model,PreTrainedModel
from transformers import Seq2SeqTrainer
from ailab.utils.other import get_state_dict,load_trainable_params,load_valuehead_params,VALUE_HEAD_FILE_NAME
from ailab.log import logger
from trl import PreTrainedModelWrapper

class PeftTrainer(Seq2SeqTrainer):
    r"""
    Inherits Seq2SeqTrainer to support parameter-efficient checkpoints.
    """
    def __init__(self, finetune_type, **kwargs):
        self.finetune_type = finetune_type
        super().__init__(**kwargs)

    def _save(self, output_dir: Optional[str] = None, state_dict: Optional[Dict[str, torch.Tensor]] = None) -> None:
        r"""
        Saves trainable parameters as model checkpoint.

        This function will only be executed at the process zero.

        Subclass and override to inject custom behavior. It should not be directly used by external scripts.
        """

        output_dir = output_dir if output_dir is not None else self.args.output_dir
        os.makedirs(output_dir, exist_ok=True)
        logger.info(f"Saving model checkpoint to {output_dir}")
        model = unwrap_model(self.model)

        if isinstance(model, PreTrainedModelWrapper):
            # Custom state dict: https://github.com/lvwerra/trl/blob/v0.4.7/trl/models/modeling_value_head.py#L200
            model_state_dict = state_dict or model.state_dict()
            v_head_state_dict = {
                name.replace("v_head.", ""): model_state_dict[name].cpu().clone().detach()
                for name in model_state_dict.keys() if name.startswith("v_head.")
            }

            torch.save(v_head_state_dict, os.path.join(output_dir, VALUE_HEAD_FILE_NAME))
            model = model.pretrained_model

        state_dict = state_dict or get_state_dict(model)
        from peft import PeftModel
        if isinstance(model, (PeftModel, PreTrainedModel)):
            model.config.use_cache = True
            model.save_pretrained(output_dir, state_dict=state_dict, safe_serialization=self.args.save_safetensors)
            model.config.use_cache = False
        else:
            torch.save(state_dict, os.path.join(output_dir, WEIGHTS_NAME))

        if self.finetune_type == "full" and self.tokenizer is not None:
            try:
                self.tokenizer.save_pretrained(output_dir)
            except:
                logger.warning("Cannot save tokenizer, copy the files manually.")

        with open(os.path.join(output_dir, TRAINING_ARGS_NAME), "w", encoding="utf-8") as f:
            f.write(self.args.to_json_string() + "\n")

    def _load_best_model(self):
        r"""
        Loads trainable parameters from model checkpoint.

        Subclass and override to inject custom behavior. It should not be directly used by external scripts.
        """
        logger.info(f"Loading best model from {self.state.best_model_checkpoint} (score: {self.state.best_metric}).")
        model = unwrap_model(self.model)
        if hasattr(model, "peft_config"): # peft methods
            model.load_adapter(self.state.best_model_checkpoint, getattr(model, "active_adapter"))
        else:
            load_trainable_params(model, self.state.best_model_checkpoint)

        if hasattr(model, "v_head"):
            load_valuehead_params(model, self.state.best_model_checkpoint)