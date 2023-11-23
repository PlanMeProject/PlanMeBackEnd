"""The module for the SubTask serializer."""
from rest_framework import serializers

from planmebackend.app.models import SubTask


class SubTaskSerializer(serializers.ModelSerializer):
    """
    Serializer for the SubTask model.

    Facilitates the serialization and deserialization of SubTask model
    instances, enabling their easy conversion to JSON and back for
    API interactions.
    """

    class Meta:
        """Meta definition for SubTask."""

        model = SubTask
        fields = "__all__"
