"""The configuration class for the nlp app."""
from django.apps import AppConfig
from transformers import T5ForConditionalGeneration, T5Tokenizer, pipeline


class NlpConfig(AppConfig):
    """The configuration class for the nlp app."""

    name = "planmebackend.nlp"
    tts_model = T5ForConditionalGeneration.from_pretrained("Jwizzed/TaskToSubtask").to("cpu")
    tokenizer = T5Tokenizer.from_pretrained("t5-small")
    summarizer = pipeline("summarization", model="t5-small")
