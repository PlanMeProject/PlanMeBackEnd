"""A module that defines the SubTaskViewSet class."""
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status, viewsets
from rest_framework.response import Response

from planmebackend.app.models import SubTask
from planmebackend.app.serializers import SubTaskSerializer


class SubTaskViewSet(viewsets.ViewSet):
    """ViewSet for handling SubTask-related operations."""

    def list(self, request, task_pk=None, **kwargs):
        """
        List all SubTasks for a specific task.

        :param request: The HTTP request.
        :param task_pk: Task's primary key.
        :return: Response with subtasks or error message.
        """
        queryset = SubTask.objects.filter(task_id=task_pk)
        serializer = SubTaskSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, task_pk=None, **kwargs):
        """
        Create a SubTask for a specific task.

        :param request: The HTTP request with subtask data.
        :param task_pk: Task's primary key.
        :return: Response with created subtask or error.
        """
        data = request.data
        data["task"] = task_pk
        serializer = SubTaskSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None, *args, **kwargs):
        """
        Retrieve a SubTask object by ID.

        :param request: The HTTP request.
        :param pk: Primary key of the SubTask.
        :return: Response with subtask data or error message.
        """
        try:
            subtask = SubTask.objects.get(id=pk)
        except ObjectDoesNotExist:
            return Response(
                {"error": "SubTask not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = SubTaskSerializer(subtask)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None, **kwargs):
        """
        Update an existing SubTask object by ID.

        :param request: The HTTP request with updated data.
        :param pk: Primary key of the SubTask to update.
        :return: Response with updated subtask or error.
        """
        try:
            subtask = SubTask.objects.get(id=pk)
        except ObjectDoesNotExist:
            return Response(
                {"error": "SubTask not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = SubTaskSerializer(
            subtask, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None, *args, **kwargs):
        """
        Delete a SubTask object by ID.

        :param request: The HTTP request.
        :param pk: Primary key of the SubTask to delete.
        :return: Response indicating deletion status.
        """
        try:
            subtask = SubTask.objects.get(id=pk)

        except ObjectDoesNotExist:
            return Response(
                {"error": "SubTask not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        subtask.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
