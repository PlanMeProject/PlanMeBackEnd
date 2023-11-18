"""The module for the SubTask serializer."""
from rest_framework import serializers

from planmebackend.app.models import SubTask


class SubTaskSerializer(serializers.ModelSerializer):
    """Serializer definition for SubTask."""

    class Meta:
        """Meta definition for SubTask."""

        model = SubTask
        fields = "__all__"
