import numpy as np
from ailab.atp_dataset.dataset import AILabDataset
from ailab.atp_finetuner.preprossor import AILabPreprocessor
from ailab.atp_finetuner.build import PreProcessorRg
from ailab.atp_finetuner.constant import Task, Model
from transformers import AutoImageProcessor


@PreProcessorRg.register((Task.object_detection, Model.yolos_base))
@PreProcessorRg.register((Task.object_detection, Model.yolos_small))
class YolosPreProcessor(AILabPreprocessor):
    def __init__(self, dataset, preprocessor):
        super().__init__(dataset, preprocessor)

    @classmethod
    def build_preprocessor(cls, model_name:str, dataset: AILabDataset, pc_dir:str, **kwargs):
        pc_name_dir = model_name if pc_dir is None else pc_dir
        image_processor = AutoImageProcessor.from_pretrained(pc_name_dir)
        labels = dataset.to_hf_dataset()["train"].features["objects"].feature["category"].names
        kwargs["model_args"]["labels"] = labels
        return cls(dataset, image_processor)

    def process_data(self) ->AILabDataset:
        image_processor = self._preprocessor
        import albumentations
        transform = albumentations.Compose(
            [
                albumentations.Resize(480, 480),
                albumentations.HorizontalFlip(p=1.0),
                albumentations.RandomBrightnessContrast(p=1.0),
            ],
            bbox_params=albumentations.BboxParams(format="coco", label_fields=["category"]),
        )

        def formatted_anns(image_id, category, area, bbox):
            annotations = []
            for i in range(0, len(category)):
                new_ann = {
                    "image_id": image_id,
                    "category_id": category[i],
                    "isCrowd": 0,
                    "area": area[i],
                    "bbox": list(bbox[i]),
                }
                annotations.append(new_ann)
            return annotations
        
        def transform_aug_ann(examples):
            image_ids = examples["image_id"]
            images, bboxes, area, categories = [], [], [], []
            for image, objects in zip(examples["image"], examples["objects"]):
                image = np.array(image.convert("RGB"))[:, :, ::-1]
                out = transform(image=image, bboxes=objects["bbox"], category=objects["category"])
                area.append(objects["area"])
                images.append(out["image"])
                bboxes.append(out["bboxes"])
                categories.append(out["category"])
            targets = [
                {"image_id": id_, "annotations": formatted_anns(id_, cat_, ar_, box_)}
                for id_, cat_, ar_, box_ in zip(image_ids, categories, area, bboxes)
            ]
            return image_processor(images=images, annotations=targets, return_tensors="pt")

        datasets = self._dataset.to_hf_dataset()
        transformed_datasets = datasets.with_transform(transform_aug_ann)
        return AILabDataset(transformed_datasets)