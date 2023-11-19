"""A module that defines the SubTaskViewSet class."""
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status, viewsets
from rest_framework.response import Response

from planmebackend.app.models import SubTask
from planmebackend.app.serializers import SubTaskSerializer


class SubTaskViewSet(viewsets.ViewSet):
    """ViewSet for handling SubTask-related operations."""

    def list(self, request, task_pk=None, **kwargs):
        """List all SubTask objects for a specific task."""
        queryset = SubTask.objects.filter(task_id=task_pk)
        serializer = SubTaskSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, task_pk=None, **kwargs):
        """Create a new SubTask object for a specific task."""
        data = request.data
        data["task"] = task_pk
        serializer = SubTaskSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None, *args, **kwargs):
        """Retrieve a SubTask object by ID."""
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
        """Update an existing SubTask object by ID."""
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
        """Delete a SubTask object by ID."""
        try:
            subtask = SubTask.objects.get(id=pk)

        except ObjectDoesNotExist:
            return Response(
                {"error": "SubTask not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        subtask.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
