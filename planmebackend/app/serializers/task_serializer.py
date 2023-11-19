"""The module defines the serializer for the Task model."""
from rest_framework import serializers

from planmebackend.app.models import Task


class TaskSerializer(serializers.ModelSerializer):
    """Serializer definition for Task."""

    class Meta:
        """Meta definition for Task."""

        model = Task
        fields = "__all__"
