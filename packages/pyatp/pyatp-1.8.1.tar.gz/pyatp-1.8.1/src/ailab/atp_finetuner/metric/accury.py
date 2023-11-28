import numpy as np
from ailab.atp_finetuner.metric import AILabMetric
from ailab.atp_finetuner.build import MetricRg
from ailab.atp_finetuner.constant import Task, Model
from sklearn.metrics import accuracy_score

@MetricRg.register((Task.text_classification, Model.distilbert_base_uncased))
@MetricRg.register((Task.image_classification, Model.vit_patch16_224_in21k))
class AccuryMetric(AILabMetric):
    def __init__(self) -> None:
        super().__init__()
    
    @staticmethod
    def evalute(eval_pred) :
        predictions, labels = eval_pred
        predictions = np.argmax(predictions, axis=1)
        return dict(accuracy=accuracy_score(predictions, labels))
    