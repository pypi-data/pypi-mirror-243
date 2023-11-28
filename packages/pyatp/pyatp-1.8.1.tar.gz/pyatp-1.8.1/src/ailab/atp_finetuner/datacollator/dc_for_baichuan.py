from transformers import DataCollatorForSeq2Seq
from ailab.atp_finetuner.datacollator import AILabDataCollator
from ailab.atp_finetuner import constant
from ailab.atp_finetuner.preprossor import AILabPreprocessor
from ailab.atp_finetuner.model import AILabModel
from ailab.atp_finetuner.build import DataCollatorRg
from ailab.atp_finetuner.constant import Task, Model

@DataCollatorRg.register((Task.question_answering, Model.baichuan_7b))
@DataCollatorRg.register((Task.question_answering, Model.baichuan_13b))
@DataCollatorRg.register((Task.question_answering, Model.bloomz_7b1_mt))
@DataCollatorRg.register((Task.question_answering, Model.falcon_7b))
@DataCollatorRg.register((Task.question_answering, Model.falcon_7b_instruct))
@DataCollatorRg.register((Task.question_answering, Model.moss_moon_003_base))
@DataCollatorRg.register((Task.question_answering, Model.llama2_7b))
@DataCollatorRg.register((Task.question_answering, Model.llama2_7b_chat_hf))
@DataCollatorRg.register((Task.question_answering, Model.llama2_13b_chat_hf))
@DataCollatorRg.register((Task.question_answering, Model.internlm_7b))
@DataCollatorRg.register((Task.question_answering, Model.belle_7b_2m))
@DataCollatorRg.register((Task.question_answering, Model.xverse_13b))
@DataCollatorRg.register((Task.question_answering, Model.bloomz_3b))
@DataCollatorRg.register((Task.question_answering, Model.bloomz_1b1))
@DataCollatorRg.register((Task.question_answering, Model.lawgpt_llama))
@DataCollatorRg.register((Task.question_answering, Model.educhat))
@DataCollatorRg.register((Task.question_answering, Model.codellama_7b_instruction))
@DataCollatorRg.register((Task.question_answering, Model.codellama_13b_instruction))
@DataCollatorRg.register((Task.question_answering, Model.chatglm3_6b))
class BaichuanDataCollator(AILabDataCollator) :
    def __init__(self, datacollator, preprocessor):
        super().__init__(datacollator, preprocessor)
    
    def forward(self, **kwargs):
        pass

    @classmethod
    def build_datacollator(cls, framework:constant.Framework, preprocessor:AILabPreprocessor, model:AILabModel) :
        tokenizer=preprocessor.preprocessor_ins
        IGNORE_INDEX = -100
        datacollator = DataCollatorForSeq2Seq(
            tokenizer, label_pad_token_id=IGNORE_INDEX
        )
        return cls(datacollator, preprocessor)