import torch
from rest_framework import status, viewsets
from rest_framework.response import Response

from planmebackend.app.models import SubTask
from planmebackend.app.serializers import SubTaskSerializer
from planmebackend.nlp.apps import NlpConfig


class TTSViewSet(viewsets.ViewSet):
    """
    ViewSet to process text and update SubTask entries in the database.
    """

    def create(self, request, *args, **kwargs):
        input_text = request.data.get("text")
        task_id = request.data.get("task_id")
        generated_text = self.perform_inference(input_text)
        generated_subtasks = generated_text.split(",")
        SubTask.objects.filter(task_id=task_id).delete()
        new_subtasks = []

        for subtask_description in generated_subtasks:
            subtask_description = subtask_description.strip()

            if not subtask_description:
                continue

            subtask_data = {"task": task_id, "title": subtask_description, "status": "Todo"}
            subtask_serializer = SubTaskSerializer(data=subtask_data)

            if subtask_serializer.is_valid():
                subtask_serializer.save()
                new_subtasks.append(subtask_serializer.data)

            else:
                return Response(subtask_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(new_subtasks, status=status.HTTP_201_CREATED)

    @staticmethod
    def perform_inference(input_text):
        model = NlpConfig.tts_model
        tokenizer = NlpConfig.tokenizer
        model.eval()
        input_tensor = tokenizer.encode(input_text, return_tensors="pt").to("cpu")

        with torch.no_grad():
            output = model.generate(input_tensor, max_length=1024)

        decoded_output = tokenizer.decode(output[0], skip_special_tokens=True)
        decoded_output = decoded_output.replace(" and ", ", ").strip()
        return decoded_output
