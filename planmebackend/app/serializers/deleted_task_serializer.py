"""The module tests the DeletedTask model."""
from rest_framework import serializers

from planmebackend.app.models import DeletedTask


class DeletedTaskSerializer(serializers.ModelSerializer):
    """
    Serializer for the DeletedTask model.

    This serializer provides a mechanism for querying and saving instances of
    the DeletedTask model, converting them to and from JSON format.
    """

    class Meta:
        """Meta definition for Deleted Task."""

        model = DeletedTask
        fields = "__all__"
