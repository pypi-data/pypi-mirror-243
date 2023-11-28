from transformers import Seq2SeqTrainingArguments,HfArgumentParser,TrainingArguments
from dataclasses import dataclass,field
from typing import Optional,Dict,Tuple

@dataclass
class MyArguments:
    end_to_zip: Optional[bool] = field(
        default=False,
        metadata={"help": "end to zip"}
    ),
    cpu_offload: Optional[bool] = field(
        default=False,
        metadata={"help": "deepspeed use offload"}
    )

def get_train_args(args:Dict) -> Tuple[MyArguments, Seq2SeqTrainingArguments]:
    parser = HfArgumentParser((MyArguments,Seq2SeqTrainingArguments))
    my_args, train_args = parser.parse_dict(args)
    print(f'my_args {my_args}, train_args {train_args}')
    return my_args, train_args

def get_base_train_args(args:Dict) -> Tuple[MyArguments, TrainingArguments]:
    parser = HfArgumentParser((MyArguments, TrainingArguments))
    my_args, train_args = parser.parse_dict(args)
    print(f'base my_args {my_args}, train_args {train_args}')
    return my_args, train_args