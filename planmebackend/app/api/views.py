from rest_framework import serializers
from ..models import User, Task, SubTask, Dashboard, DataVisualization

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'token']

# Task Serializer
class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['task_id', 'title', 'description', 'summarized_text', 'bullet_text', 'due_date', 'status', 'user']

# SubTask Serializer
class SubTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields = ['subtask_id', 'title', 'status', 'task']

# Dashboard Serializer
class DashboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dashboard
        fields = ['dashboard_id', 'user']

# DataVisualization Serializer
class DataVisualizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataVisualization
        fields = ['visualization_id', 'task']
