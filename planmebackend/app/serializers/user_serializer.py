"""The module defines the serializer for the User model."""
from rest_framework import serializers

from planmebackend.app.models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.

    Provides serialization and deserialization functionality for the User
    model, allowing for efficient JSON format conversion for API responses
    and requests.
    """

    class Meta:
        """Meta definition for User."""

        model = User
        fields = "__all__"
