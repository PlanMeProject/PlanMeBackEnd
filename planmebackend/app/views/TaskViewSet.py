"""A module that defines the TaskViewSet class."""
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status, viewsets
from rest_framework.response import Response

from planmebackend.app.models import Task
from planmebackend.app.serializers import TaskSerializer


class TaskViewSet(viewsets.ViewSet):
    """
    ViewSet for handling Task-related operations.
    """

    def list(self, request, user_pk=None):
        """List all Task objects for a specific user."""
        queryset = Task.objects.filter(user_id=user_pk)
        serializer = TaskSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, user_pk=None):
        """Create a new Task object for a specific user."""
        data = request.data
        data["user"] = user_pk
        serializer = TaskSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None, **kwargs):
        """Retrieve a Task object by ID."""
        try:
            task = Task.objects.get(id=pk)
        except ObjectDoesNotExist:
            return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = TaskSerializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None, user_pk=None, **kwargs):
        """Update an existing Task object by ID."""
        try:
            task = Task.objects.get(id=pk)
        except ObjectDoesNotExist:
            return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)
        data = request.data
        data["user"] = user_pk

        serializer = TaskSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None, **kwargs):
        """Delete a Task object by ID."""
        try:
            task = Task.objects.get(id=pk)
        except ObjectDoesNotExist:
            return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
