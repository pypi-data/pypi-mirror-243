from typing import Dict,List,Any
from transformers import DataCollatorWithPadding
from ailab.atp_finetuner.datacollator import AILabDataCollator
from ailab.atp_finetuner import constant
from ailab.atp_finetuner.preprossor import AILabPreprocessor
from ailab.atp_finetuner.model import AILabModel
from ailab.atp_finetuner.build import DataCollatorRg
from ailab.atp_finetuner.constant import Task, Model

class DataCollatorForYolos(DataCollatorWithPadding):
    def __init__(self, preprocessor):
        self._preprocessor = preprocessor

    def __call__(self, features: List[Dict[str, Any]]) -> Dict[str, Any]:
        pixel_values = [item["pixel_values"] for item in features]
        encoding = self._preprocessor.pad(pixel_values, return_pixel_mask=False, return_tensors="pt")
        labels = [item["labels"] for item in features]
        batch = {}
        batch["pixel_values"] = encoding["pixel_values"]
        #batch["pixel_mask"] = encoding["pixel_mask"]
        batch["labels"] = labels
        return batch

@DataCollatorRg.register((Task.object_detection, Model.yolos_base))
@DataCollatorRg.register((Task.object_detection, Model.yolos_small))
class YolosDataCollator(AILabDataCollator) :
    def __init__(self, datacollator, preprocessor):
        super().__init__(datacollator, preprocessor)
    
    def forward(self, **kwargs):
        pass

    @classmethod
    def build_datacollator(cls, framework:constant.Framework, preprocessor:AILabPreprocessor,model:AILabModel) :
        datacollator = DataCollatorForYolos(preprocessor.preprocessor_ins)
        return cls(datacollator, preprocessor)