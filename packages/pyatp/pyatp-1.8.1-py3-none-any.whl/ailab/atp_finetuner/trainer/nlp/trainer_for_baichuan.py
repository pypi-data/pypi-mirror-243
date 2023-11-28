
from typing import Dict, Optional,Callable
import os
from ailab.utils.other import plot_loss
from ailab.atp_dataset.dataset import AILabDataset
from ailab.atp_finetuner.trainer import AILabTrainer 
from ailab.atp_finetuner.model import AILabModel
from ailab.atp_finetuner.datacollator import AILabDataCollator
from ailab.atp_finetuner.metric import AILabMetric
from ailab.atp_finetuner.preprossor import AILabPreprocessor
from ailab.atp_finetuner.build import TrainerRg
from ailab.atp_finetuner.constant import Task, Model
from ailab.utils.callbacks import TrainProgress
from ailab.log import logger

@TrainerRg.register((Task.question_answering, Model.baichuan_7b))
@TrainerRg.register((Task.question_answering, Model.baichuan_13b))
@TrainerRg.register((Task.question_answering, Model.bloomz_7b1_mt))
@TrainerRg.register((Task.question_answering, Model.bloomz_3b))
@TrainerRg.register((Task.question_answering, Model.bloomz_1b1))
@TrainerRg.register((Task.question_answering, Model.falcon_7b))
@TrainerRg.register((Task.question_answering, Model.falcon_7b_instruct))
@TrainerRg.register((Task.question_answering, Model.moss_moon_003_base))
@TrainerRg.register((Task.question_answering, Model.llama2_7b))
@TrainerRg.register((Task.question_answering, Model.llama2_7b_chat_hf))
@TrainerRg.register((Task.question_answering, Model.llama2_13b_chat_hf))
@TrainerRg.register((Task.question_answering, Model.internlm_7b))
@TrainerRg.register((Task.question_answering, Model.belle_7b_2m))
@TrainerRg.register((Task.question_answering, Model.xverse_13b))
@TrainerRg.register((Task.question_answering, Model.lawgpt_llama))
@TrainerRg.register((Task.question_answering, Model.educhat))
@TrainerRg.register((Task.question_answering, Model.codellama_7b_instruction))
@TrainerRg.register((Task.question_answering, Model.codellama_13b_instruction))
@TrainerRg.register((Task.question_answering, Model.atom_7b))
@TrainerRg.register((Task.question_answering, Model.chatglm3_6b))
class BaichuanTrainer(AILabTrainer):
    def __init__(self):
        super().__init__()

    def preprocess(self, dataset:AILabDataset, model:AILabModel, preprocessor: AILabPreprocessor, \
                      data_collator:AILabDataCollator, metric:AILabMetric, train_progress:Callable, **kwargs):
        train_args = kwargs['train_args']
        finetune_type = kwargs['model_args'].get('finetune_type', 'lora')

        offload = train_args.get('cpu_offload',False)
        deepspeed_dir = os.path.dirname(os.path.abspath(__file__))
        if offload:
            logger.info('use ds_zero2_cpu_offload')
            deepspeed_dir = os.path.join(deepspeed_dir,"ds_zero2_cpu_offload.json")
        else:
            logger.info('use ds_zero2_no_offload')
            deepspeed_dir = os.path.join(deepspeed_dir,"ds_zero2_no_offload.json")
        train_args['ddp_find_unused_parameters'] = False
        train_args['ddp_timeout'] = 30000
        train_args['deepspeed'] = deepspeed_dir

        from ailab.utils.parse_args import get_train_args
        _, training_args = get_train_args(train_args)

        logger.info(f'training_args {training_args}') 

        stage = kwargs['model_args'].get('stage', 'sft')
        from ailab.atp_finetuner.trainer.nlp.common_trainer import PeftTrainer
        if stage == 'sft':
            trainer = PeftTrainer(
                finetune_type=finetune_type,
                model=model.model_ins,
                train_dataset=dataset.to_hf_dataset()['train'],
                eval_dataset=dataset.to_hf_dataset()['test'],
                args=training_args,
                tokenizer=preprocessor.preprocessor_ins,
                data_collator=data_collator.datacollator_ins,
                callbacks=[TrainProgress(train_progress)],
            )
        elif stage == 'dpo':
            from trl import DPOTrainer
            training_args.remove_unused_columns = False
            trainer = DPOTrainer(
                model=model.model_ins,
                train_dataset=dataset.to_hf_dataset(),
                args=training_args,
                tokenizer=preprocessor.preprocessor_ins,
                max_length=512,
                max_prompt_length=128,
                callbacks=[TrainProgress(train_progress)],
            )

        self.trainer = trainer
        self.train_args = train_args
    
    def train(self):
        trainer = self.trainer
        output_dir = self.train_args.get('output_dir', 'my_model')
        resume_from_checkpoint = self.train_args.get('resume_from_checkpoint', False)
        end_to_zip = self.train_args.get('end_to_zip', False)

        if resume_from_checkpoint:
            from transformers.trainer_utils import get_last_checkpoint
            resume_from_checkpoint = get_last_checkpoint(output_dir)

        train_result = trainer.train(resume_from_checkpoint=resume_from_checkpoint)
        trainer.log_metrics("train", train_result.metrics)
        trainer.save_metrics("train", train_result.metrics)
        trainer.save_state()
        trainer.save_model()

        if trainer.is_world_process_zero():
            plot_loss(output_dir, keys=["loss", "eval_loss"])
            if end_to_zip:
                from ailab.utils.other import create_zip_and_delete_folder
                zip_file_path = output_dir+"/adapter.zip"
                create_zip_and_delete_folder(output_dir,zip_file_path)

    def postprocess(self):
        metrics = self.trainer.evaluate()
        self.trainer.log_metrics("eval", metrics)
        self.trainer.save_metrics("eval", metrics)



