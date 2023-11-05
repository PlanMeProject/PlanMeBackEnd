"""Serializers for the api app."""
from rest_framework import serializers

from planmebackend.app.models import SubTask, Task, User


class UserSerializer(serializers.ModelSerializer):
    """Serializer definition for User."""

    class Meta:
        """Meta definition for User."""

        model = User
        fields = "__all__"


class TaskSerializer(serializers.ModelSerializer):
    """Serializer definition for Task."""

    class Meta:
        """Meta definition for Task."""

        model = Task
        fields = "__all__"


class SubTaskSerializer(serializers.ModelSerializer):
    """Serializer definition for SubTask."""

    class Meta:
        """Meta definition for SubTask."""

        model = SubTask
        fields = "__all__"
