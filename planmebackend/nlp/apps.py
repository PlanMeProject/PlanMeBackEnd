from django.apps import AppConfig
from transformers import T5ForConditionalGeneration, T5Tokenizer


class NlpConfig(AppConfig):
    name = "planmebackend.nlp"
    model = T5ForConditionalGeneration.from_pretrained("Jwizzed/TaskToSubtask").to("cpu")
    tokenizer = T5Tokenizer.from_pretrained("t5-small")
