from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status, viewsets
from rest_framework.response import Response

from ..models import Dashboard, DataVisualization, SubTask, Task, User
from .serializers import (
    DashboardSerializer,
    DataVisualizationSerializer,
    SubTaskSerializer,
    TaskSerializer,
    UserSerializer,
)


class UserViewSet(viewsets.ViewSet):
    """
    ViewSet for handling User-related operations.
    """

    def list(self, request):
        """List all User objects."""
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        """Retrieve a User object by ID."""
        try:
            user = User.objects.get(id=pk)
        except ObjectDoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        """Create a new User object."""
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        """Update an existing User object by ID."""
        try:
            user = User.objects.get(id=pk)
        except ObjectDoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        """Delete a User object by ID."""
        try:
            user = User.objects.get(id=pk)
        except ObjectDoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


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


class SubTaskViewSet(viewsets.ViewSet):
    """
    ViewSet for handling SubTask-related operations.
    """

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
            return Response({"error": "SubTask not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = SubTaskSerializer(subtask)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None, **kwargs):
        """Update an existing SubTask object by ID."""
        try:
            subtask = SubTask.objects.get(id=pk)
        except ObjectDoesNotExist:
            return Response({"error": "SubTask not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = SubTaskSerializer(subtask, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None, *args, **kwargs):
        """Delete a SubTask object by ID."""
        try:
            subtask = SubTask.objects.get(id=pk)

        except ObjectDoesNotExist:
            return Response({"error": "SubTask not found"}, status=status.HTTP_404_NOT_FOUND)

        subtask.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DashboardViewSet(viewsets.ViewSet):
    """
    ViewSet for handling Dashboard-related operations.
    """

    def create(self, request):
        """Create a new Dashboard object."""
        serializer = DashboardSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Retrieve a Dashboard object by ID."""
        try:
            dashboard = Dashboard.objects.get(id=pk)
        except ObjectDoesNotExist:
            return Response({"error": "Dashboard not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = DashboardSerializer(dashboard)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        """Update an existing Dashboard object by ID."""
        try:
            dashboard = Dashboard.objects.get(id=pk)
        except ObjectDoesNotExist:
            return Response({"error": "Dashboard not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = DashboardSerializer(dashboard, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        """Delete a Dashboard object by ID."""
        try:
            dashboard = Dashboard.objects.get(id=pk)
        except ObjectDoesNotExist:
            return Response({"error": "Dashboard not found"}, status=status.HTTP_404_NOT_FOUND)
        dashboard.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DataVisualizationViewSet(viewsets.ViewSet):
    """
    ViewSet for handling DataVisualization-related operations.
    """

    def list(self, request):
        """List all DataVisualization objects."""
        queryset = DataVisualization.objects.all()
        serializer = DataVisualizationSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        """Create a new DataVisualization object."""
        serializer = DataVisualizationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Retrieve a DataVisualization object by ID."""
        try:
            visualization = DataVisualization.objects.get(id=pk)

        except ObjectDoesNotExist:
            return Response({"error": "DataVisualization not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = DataVisualizationSerializer(visualization)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        """Update an existing DataVisualization object by ID."""
        try:
            visualization = DataVisualization.objects.get(id=pk)

        except ObjectDoesNotExist:
            return Response({"error": "DataVisualization not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = DataVisualizationSerializer(visualization, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        """Delete a DataVisualization object by ID."""
        try:
            visualization = DataVisualization.objects.get(id=pk)
        except ObjectDoesNotExist:
            return Response({"error": "DataVisualization not found"}, status=status.HTTP_404_NOT_FOUND)
        visualization.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
