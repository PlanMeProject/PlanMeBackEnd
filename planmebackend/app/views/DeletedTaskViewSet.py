"""A module that defines the DeleteViewSet class."""
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status, viewsets
from rest_framework.response import Response

from planmebackend.app.models import DeletedTask
from planmebackend.app.serializers import DeletedTaskSerializer


class DeletedTaskViewSet(viewsets.ViewSet):
    """ViewSet for handling Deleted-Task-related operations."""

    def list(self, request, user_pk=None):
        """List all Deleted Task objects for the user and courses."""
        user_pk = request.query_params.get("user_id", None)

        if not user_pk:
            return Response(
                {"error": "User ID is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        queryset = DeletedTask.objects.filter(user_id=user_pk)
        serializer = DeletedTaskSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, user_pk=None):
        """Create a new Deleted Task object for a specific user."""
        data = request.data
        data["user"] = user_pk
        serializer = DeletedTaskSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None, **kwargs):
        """Delete a Deleted Task object by ID."""
        try:
            task = DeletedTask.objects.get(id=pk)
        except ObjectDoesNotExist:
            return Response(
                {"error": "Deleted Task not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
