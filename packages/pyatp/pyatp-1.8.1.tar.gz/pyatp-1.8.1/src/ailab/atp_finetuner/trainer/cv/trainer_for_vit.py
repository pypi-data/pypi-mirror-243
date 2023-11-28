from typing import Callable
from ailab.atp_dataset.dataset import AILabDataset
from ailab.atp_finetuner.trainer import AILabTrainer 
from ailab.atp_finetuner.model import AILabModel
from ailab.atp_finetuner.datacollator import AILabDataCollator
from ailab.atp_finetuner.metric import AILabMetric
from ailab.atp_finetuner.preprossor import AILabPreprocessor
from ailab.atp_finetuner.build import TrainerRg
from ailab.atp_finetuner.constant import Task, Model
from ailab.log import logger
from transformers import Trainer
from ailab.utils.other import plot_loss

@TrainerRg.register((Task.image_classification, Model.vit_patch16_224_in21k))
class ViTTrainer(AILabTrainer):
    def __init__(self):
        super().__init__()

    def preprocess(self, dataset:AILabDataset, model:AILabModel, preprocessor: AILabPreprocessor, \
                      data_collator:AILabDataCollator, metric:AILabMetric, train_progress:Callable, **kwargs):
        train_args = kwargs['train_args']
        train_args['ddp_find_unused_parameters'] = False
        train_args['ddp_timeout'] = 30000
        from ailab.utils.parse_args import get_base_train_args
        _, training_args = get_base_train_args(train_args)

        logger.info(f'training_args {training_args}') 

        trainer = Trainer(
            model=model.model_ins,
            args=training_args,
            data_collator=data_collator.datacollator_ins,
            train_dataset=dataset.to_hf_dataset()['train'],
            eval_dataset=dataset.to_hf_dataset()['test'],
            tokenizer=preprocessor.preprocessor_ins,
            compute_metrics=metric.evalute,
        )
        self.trainer = trainer
        self.train_args = train_args

    def train(self):
        trainer = self.trainer
        output_dir = self.train_args.get('output_dir', 'my_model')

        train_result = trainer.train()
        trainer.log_metrics("train", train_result.metrics)
        trainer.save_metrics("train", train_result.metrics)
        trainer.save_state()
        trainer.save_model()

        if trainer.is_world_process_zero():
            plot_loss(output_dir, keys=["loss", "eval_loss", "eval_accuracy"])
            end_to_zip = self.train_args.get('end_to_zip', False)
            if end_to_zip:
                from ailab.utils.other import create_zip_and_delete_folder
                zip_file_path = output_dir+"/adapter.zip"
                create_zip_and_delete_folder(output_dir,zip_file_path)

    def postprocess(self):
        trainer = self.trainer
        metrics = trainer.evaluate()
        trainer.log_metrics("eval", metrics)
        trainer.save_metrics("eval", metrics)