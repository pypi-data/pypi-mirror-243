from ailab.atp_dataset.dataset import AILabDataset
from ailab.atp_finetuner.preprossor import AILabPreprocessor
from ailab.atp_finetuner.build import PreProcessorRg
from ailab.atp_finetuner.constant import Task, Model
from transformers import AutoImageProcessor
from torchvision.transforms import RandomResizedCrop, Compose, Normalize, ToTensor

@PreProcessorRg.register((Task.image_classification, Model.vit_patch16_224_in21k))
class ViTPreProcessor(AILabPreprocessor):
    def __init__(self, dataset, preprocessor):
        super().__init__(dataset, preprocessor)

    @classmethod
    def build_preprocessor(cls, model_name:str, dataset: AILabDataset,pc_dir:str,**kwargs):
        pc_name_dir = model_name if pc_dir is None else pc_dir
        image_processor = AutoImageProcessor.from_pretrained(pc_name_dir)
        labels = dataset.to_hf_dataset()["train"].features["label"].names
        kwargs["model_args"]["labels"] = labels
        return cls(dataset, image_processor)

    def process_data(self) ->AILabDataset:
        image_processor = self._preprocessor
        normalize = Normalize(mean=image_processor.image_mean, std=image_processor.image_std)
        size = (
            image_processor.size["shortest_edge"]
            if "shortest_edge" in image_processor.size
            else (image_processor.size["height"], image_processor.size["width"])
        )
        _transforms = Compose([RandomResizedCrop(size), ToTensor(), normalize])

        def transforms(examples):
            examples["pixel_values"] = [_transforms(img.convert("RGB")) for img in examples["image"]]
            del examples["image"]
            return examples

        datasets = self._dataset.to_hf_dataset()
        transformed_datasets = datasets.with_transform(transforms)
        return AILabDataset(transformed_datasets)