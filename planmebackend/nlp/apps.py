from django.apps import AppConfig
from transformers import T5ForConditionalGeneration, T5Tokenizer, pipeline


class NlpConfig(AppConfig):
    name = "planmebackend.nlp"
    tts_model = None
    tokenizer = None
    summarizer = None

    def get_tts_model(self):
        if not self.tts_model:
            self.tts_model = T5ForConditionalGeneration.from_pretrained("Jwizzed/TaskToSubtask").to("cpu")
        return self.tts_model

    def get_tokenizer(self):
        if not self.tokenizer:
            self.tokenizer = T5Tokenizer.from_pretrained("t5-small")
        return self.tokenizer

    def get_summarizer(self):
        if not self.summarizer:
            self.summarizer = pipeline("summarization", model="t5-small")
        return self.summarizer
