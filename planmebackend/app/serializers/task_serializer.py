"""The module defines the serializer for the Task model."""
from rest_framework import serializers

from planmebackend.app.models import Task


class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer for the Task model.

    Handles the conversion of Task model instances to JSON format and
    vice versa, simplifying the process of transmitting Task data over APIs.
    """

    class Meta:
        """Meta definition for Task."""

        model = Task
        fields = "__all__"
