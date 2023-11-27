from abc import abstractmethod, ABC
from typing import Any

import torch
import transformers
from huggingface_hub import login
from transformers import AutoTokenizer

from ..abstract_model import AbstractModel


# pip install torch==2.0.1+cu118 -f https://download.pytorch.org/whl/torch_stable.html

class AbstractLLama2(AbstractModel, ABC):
    def __init__(self, model_name: str,
                 hugging_face_token: str | None,
                 force_cpu=False,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model_name = model_name
        login(token=hugging_face_token)
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = transformers.AutoModelForCausalLM.from_pretrained(
            self.model_name,
            load_in_8_bit=True,
            torch_dtype=torch.float16 if not force_cpu else torch.float32,
            device_map={"": 0} if not force_cpu else 'cpu',
            trust_remote_code=True,
        )
        # self.pipeline = transformers.pipeline(
        #     "text-generation",
        #     model=self.model_name,
        #     torch_dtype=torch.float16 if not force_cpu else torch.float32,
        #     tokenizer=self.tokenizer,
        #     device_map={"": 0} if not force_cpu else 'cpu',
        #     trust_remote_code=True,
        # ).enable_xformers_memory_efficient_attention()

    @property
    @abstractmethod
    def prompt(self):
        raise NotImplementedError

    def predict_input(self, model_input, table) -> list[Any]:
        final_prompt = self.prompt + model_input
        # sequences = self.pipeline(
        #     final_prompt,
        #     do_sample=False,
        #     num_return_sequences=1,
        #     eos_token_id=self.tokenizer.eos_token_id,
        #     max_new_tokens=2048,
        #     batch_size=1
        # )
        #text = sequences[0]['generated_text']

        model_inputs = self.tokenizer([final_prompt],
                                      return_tensors="pt",
                                      ).to("cuda")
        generated_ids = self.model.generate(**model_inputs)
        text = self.tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
        text = text.replace(final_prompt, '').strip()
        return self._normalize_output(text)

    @abstractmethod
    def _normalize_output(self, text):
        raise NotImplementedError
