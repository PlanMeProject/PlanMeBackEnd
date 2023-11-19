"""A module for the TTSViewSet class of the nlp app."""
import torch
from django.db import transaction
from rest_framework import status, viewsets
from rest_framework.response import Response

from planmebackend.app.models import SubTask
from planmebackend.app.serializers import SubTaskSerializer
from planmebackend.nlp.apps import NlpConfig


class TTSViewSet(viewsets.ViewSet):
    """ViewSet to process text and update SubTask entries in the database."""

    def create(self, request, *args, **kwargs):
        """Create new SubTask entries based on the input text."""
        input_text = request.data.get("text")
        task_id = request.data.get("task_id")
        generated_text = self.perform_inference(input_text)
        generated_subtasks = generated_text.split(",")
        subtask_data_list = []

        for subtask_title in generated_subtasks:
            subtask_title = subtask_title.strip()
            if subtask_title:
                subtask_data_list.append(
                    SubTask(
                        title=subtask_title, task_id=task_id, status="Todo"
                    )
                )

        with transaction.atomic():
            SubTask.objects.filter(task_id=task_id).delete()

            new_subtasks_instances = SubTask.objects.bulk_create(
                subtask_data_list
            )

        new_subtasks_data = SubTaskSerializer(
            new_subtasks_instances, many=True
        ).data

        return Response(new_subtasks_data, status=status.HTTP_201_CREATED)

    @staticmethod
    def perform_inference(input_text):
        """Perform inference on the input text."""
        model = NlpConfig.tts_model
        tokenizer = NlpConfig.tokenizer
        model.eval()
        input_tensor = tokenizer.encode(input_text, return_tensors="pt").to(
            "cpu"
        )

        with torch.no_grad():
            output = model.generate(input_tensor, max_length=1024)

        decoded_output = tokenizer.decode(output[0], skip_special_tokens=True)
        decoded_output = decoded_output.replace(" and ", ", ").strip()
        return decoded_output
