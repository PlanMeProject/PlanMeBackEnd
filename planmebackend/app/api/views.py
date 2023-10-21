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


class TaskViewSet(viewsets.ViewSet):
    """
    ViewSet for handling Task-related operations.
    """

    def list(self, request):
        """List all Task objects."""
        queryset = Task.objects.all()
        serializer = TaskSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        """Create a new Task object."""
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Retrieve a Task object by ID."""
        try:
            task = Task.objects.get(id=pk)
        except ObjectDoesNotExist:
            return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = TaskSerializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        """Update an existing Task object by ID."""
        try:
            task = Task.objects.get(id=pk)
        except ObjectDoesNotExist:
            return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = TaskSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
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

    def list(self, request, *args, **kwargs):
        """List all SubTask objects."""
        queryset = SubTask.objects.all()
        serializer = SubTaskSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        """Create a new SubTask object."""
        serializer = SubTaskSerializer(data=request.data)
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
        serializer = SubTaskSerializer(subtask, data=request.data)
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

    def list(self, request):
        """List all Dashboard objects."""
        queryset = Dashboard.objects.all()
        serializer = DashboardSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

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
        serializer = DashboardSerializer(dashboard, data=request.data)
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

        serializer = DataVisualizationSerializer(visualization, data=request.data)
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
