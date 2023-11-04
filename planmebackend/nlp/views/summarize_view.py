# from rest_framework import status, viewsets
# from rest_framework.response import Response
#
# from planmebackend.app.models import Task
# from planmebackend.app.serializers import SubTaskSerializer
# from planmebackend.nlp.apps import NlpConfig
#
#
# class SummarizeViewSet(viewsets.ViewSet):
#     def create(self, request, *args, **kwargs):
#         input_text = request.data.get("text")
#         task_id = request.data.get("task_id")
#         generated_text = self.perform_summary(input_text)
#         Task.objects.get(task_id=task_id).delete()
#         task_data = {"task": task_id, "summarized_text": generated_text}
#         task_serializer = SubTaskSerializer(data=generated_text)
#         if task_serializer.is_valid():
#             task_serializer.save()
#         else:
#             return Response(task_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         return Response(task_serializer, status=status.HTTP_201_CREATED)
#
#     @staticmethod
#     def perform_summary(input_text):
#         return NlpConfig.summarizer(input_text)[0]["summary_text"]
