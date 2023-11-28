from ailab.atp_finetuner.model.model import AILabModel
from transformers import AutoModelForImageClassification
from ailab.atp_finetuner.build import ModelRg
from ailab.atp_finetuner.constant import Task, Model

@ModelRg.register((Task.image_classification, Model.vit_patch16_224_in21k))
class ViTModel(AILabModel):
    def __init__(self, model: any) -> None:
        super().__init__(model)

    def forward(self,**kwargs):
        pass
    
    @classmethod
    def build_model(cls, device_name:str, model_name:str, model_dir:str, **kwargs):
        model_name_or_dir = model_name if model_dir is None else model_dir
        keyLabels = "labels"
        if keyLabels not in kwargs:
            raise Exception('labels not exist for image classification')
        labels = kwargs[keyLabels]
        if not isinstance(labels, list) or len(labels) == 0:
            raise ValueError('labels should list type and not empty')
        label2id, id2label = dict(), dict()
        for i, label in enumerate(labels):
            label2id[label] = str(i)
            id2label[str(i)] = label

        model = AutoModelForImageClassification.from_pretrained(
            model_name_or_dir,
            num_labels=len(labels),
            id2label=id2label,
            label2id=label2id,
            ignore_mismatched_sizes=True
        )
        model = model.cuda()
        return cls(model)
    
    def get_inside_models(self, model_type:str):
        pass