import os
from typing import (Dict, Optional,  Union)
from datasets import (load_dataset,load_from_disk)
from datasets import inspect, Image, Features, Sequence, ClassLabel, Value, Split
from datasets import Dataset, DatasetDict, IterableDataset, IterableDatasetDict

class HFDatasetAPI :
    def __init__(self) -> None:
        pass

    def load(dataset_name: str,) -> Union[DatasetDict, Dataset, IterableDatasetDict, IterableDataset]:
        hf_dataset = load_dataset(dataset_name)
        i = Image()
        return hf_dataset
        
    def load_disk(dataset:str, data_dir: Optional[str] = None)-> Union[DatasetDict, Dataset, IterableDatasetDict, IterableDataset]:
        supported_dataset_format = {"csv","json","text","jsonl","png","jpg"}
        def load_file(dataset:str):
            dataset_name_format_spit = dataset.split('.')
            dataset_name_format = dataset_name_format_spit[-1].strip()
            if dataset_name_format not in supported_dataset_format:
                raise TypeError('dataset format should be json or csv or text')
            if dataset_name_format == "jsonl":
                dataset_name_format = "json"
            hf_dataset = load_dataset(path=dataset_name_format, data_files=dataset)
            return hf_dataset

        if dataset == "imagefolder":
            return load_dataset(dataset, data_dir=data_dir)

        if os.path.isfile(dataset):
            return load_file(dataset)
        if os.path.isdir(dataset):
            files = os.listdir(dataset)
            dataset_files = set()
            for file in files:
                dataset_name_format_spit = file.split('.')
                dataset_name_format = dataset_name_format_spit[-1].strip()
                if dataset_name_format in supported_dataset_format:
                    dataset_files.add(file)
            if len(dataset_files) == 1:
                file_path = os.path.join(dataset, next(iter(dataset_files)))
                return load_file(file_path)
            else:
                return load_dataset(dataset)

    def load_image_with_annotations(image_dir: str, annPath: str)-> Union[DatasetDict, Dataset, IterableDatasetDict, IterableDataset]:
        from pycocotools.coco import COCO
        coco = COCO(annPath)
        # 获取所有分类名称
        category_names = []
        for _, cat_info in coco.cats.items():
            category_names.append(cat_info['name'])

        # 只保留基本信息，图像，分类，候选框
        features = Features({
            "image_id": Value("int64"),
            "image": Image(),
            "objects": Sequence(
                {
                    "id": Value("int64"),
                    "area": Value("float"),
                    "category": ClassLabel(names=category_names),
                    "bbox": Sequence(Value("float32"), length=4),
                }
            )
        })
        data_list = []
        image_ids = coco.getImgIds()
        for image_id in image_ids:
            image_info = coco.loadImgs(image_id)[0]
            data = {}
            data["image_id"] = image_info['id']
            data["image"] = {"path": os.path.join(image_dir, image_info['file_name'])}
            objects = []
            annotation_ids = coco.getAnnIds(imgIds=image_id)
            annotations = coco.loadAnns(annotation_ids)
            for item in annotations:
                objects.append({
                        "id": item['id'],
                        "area": item['area'],
                        "category": coco.cats[item['category_id']]['name'],
                        "bbox":item['bbox'],
                    })
            data["objects"] = objects
            data_list.append(data)

        hf_dataset = Dataset.from_list(data_list, features=features, split=Split.TRAIN)

        # 过滤bbox无效的选项
        def condition_met(item):
            image = item['image']
            objects = item['objects']
            for box in objects['bbox']:
                x, y, w, h = tuple(box)
                if x + w > image.width or y + h > image.height:
                    return False
            return True

        hf_dataset = hf_dataset.filter(lambda item: condition_met(item))

        return hf_dataset

    def list() -> str :
        dataset = inspect.list_datasets()
        return dataset
    
    def train_test_split(dataset : Dataset, test_size:float) :
        return dataset.train_test_split(test_size=test_size)

    def trasform_dataset(stage:str, datasets:DatasetDict):
        import json
        json_path = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(json_path,"data_info.json")
        with open(json_path, "r") as json_file:
            json_data = json.load(json_file)
            body = json_data[stage]
            for _,value in body.items():
                prompt = value['prompt']
                query = value['query']
                response = value['response']
                
                for key,dataset in datasets.items():
                    dummy_data = [None] * len(dataset)
                    if prompt and prompt in dataset.column_names and response and response in dataset.column_names:
                        if query and query in dataset.column_names:
                            dataset = dataset.rename_column(prompt, 'instruction')
                            dataset = dataset.rename_column(query, 'input')
                            dataset = dataset.rename_column(response, 'output')
                            datasets[key] = dataset
                        elif not query:
                            dataset = dataset.rename_column(prompt, 'instruction')
                            dataset = dataset.rename_column(response, 'output')
                            dataset = dataset.add_column('input', dummy_data)
                            datasets[key] = dataset
        return datasets
                

