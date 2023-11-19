"""The module defines the serializer for the User model."""
from rest_framework import serializers

from planmebackend.app.models import User


class UserSerializer(serializers.ModelSerializer):
    """Serializer definition for User."""

    class Meta:
        """Meta definition for User."""

        model = User
        fields = "__all__"
