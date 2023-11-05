import torch
from django.apps import apps
from rest_framework import status, viewsets
from rest_framework.response import Response

from planmebackend.app.models import SubTask
from planmebackend.app.serializers import SubTaskSerializer


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

        for subtask_title in generated_subtasks:
            subtask_title = subtask_title.strip()

            if not subtask_title:
                continue

            data = {"title": subtask_title, "task": task_id, "status": "Todo"}

            subtask_serializer = SubTaskSerializer(data=data)

            if subtask_serializer.is_valid():
                subtask_instance = subtask_serializer.save()
                subtask_data = {
                    "type": "SubTaskViewSet",
                    "id": str(subtask_instance.id),
                    "attributes": {"title": subtask_instance.title, "status": subtask_instance.status},
                    "relationships": {"task": {"data": {"type": "Task", "id": str(subtask_instance.task.id)}}},
                }
                new_subtasks.append(subtask_data)
            else:
                return Response(subtask_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(new_subtasks, status=status.HTTP_201_CREATED)

    @staticmethod
    def perform_inference(input_text):
        nlp_config = apps.get_app_config("nlp")
        model = nlp_config.get_tts_model()
        tokenizer = nlp_config.get_tokenizer()
        model.eval()
        input_tensor = tokenizer.encode(input_text, return_tensors="pt").to("cpu")

        with torch.no_grad():
            output = model.generate(input_tensor, max_length=1024)

        decoded_output = tokenizer.decode(output[0], skip_special_tokens=True)
        decoded_output = decoded_output.replace(" and ", ", ").strip()
        return decoded_output
