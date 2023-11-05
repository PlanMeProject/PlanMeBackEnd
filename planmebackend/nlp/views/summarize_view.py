import logging

from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.response import Response

from planmebackend.app.models import Task
from planmebackend.app.serializers import TaskSerializer
from planmebackend.nlp.apps import NlpConfig


class SummarizeViewSet(viewsets.ViewSet):
    def update(self, request, *args, **kwargs):
        input_text = request.data.get("text")
        task_id = request.data.get("task_id")

        if not input_text:
            return Response({"error": "No text provided"}, status=status.HTTP_400_BAD_REQUEST)

        task = get_object_or_404(Task, id=task_id)

        try:
            generated_text = self.perform_summary(input_text)
            task_data = {"summarized_text": generated_text}
            task_serializer = TaskSerializer(task, data=task_data, partial=True)

            if not task_serializer.is_valid():
                return Response(task_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            task_serializer.save()
            return Response(task_serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    def perform_summary(input_text):
        try:
            return NlpConfig.summarizer(input_text)[0]["summary_text"]
        except Exception as error:
            logging.error(error)
