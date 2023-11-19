"""The module tests the DeletedTask model."""
from rest_framework import serializers

from planmebackend.app.models import DeletedTask


class DeletedTaskSerializer(serializers.ModelSerializer):
    """Serializer definition for Deleted Task."""

    class Meta:
        """Meta definition for Deleted Task."""

        model = DeletedTask
        fields = "__all__"
