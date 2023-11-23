"""A module that defines the UserViewSet class."""
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status, viewsets
from rest_framework.response import Response

from planmebackend.app.models import User
from planmebackend.app.serializers import UserSerializer


class UserViewSet(viewsets.ViewSet):
    """ViewSet for handling User-related operations."""

    def retrieve(self, request, pk=None):
        """
        Retrieve a User object by ID.

        :param request: The incoming HTTP request.
        :param pk: The primary key of the user to be retrieved.
        :return: HTTP Response with user data or an error message.
        """
        try:
            user = User.objects.get(id=pk)
        except ObjectDoesNotExist:
            return Response(
                {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        """
        Create a new User object.

        :param request: The incoming HTTP request containing the new User data.
        :return: HTTP Response with the created User object or
        an error message.
        """
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        """
        Update an existing User object by ID.

        :param request: The incoming HTTP request with updated User data.
        :param pk: The primary key of the user to be updated.
        :return: HTTP Response with updated user data or an error message.
        """
        try:
            user = User.objects.get(id=pk)
        except ObjectDoesNotExist:
            return Response(
                {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        """
        Delete a User object by ID.

        :param request: The incoming HTTP request.
        :param pk: The primary key of the user to be deleted.
        :return: HTTP Response indicating successful deletion or
        an error message.
        """
        try:
            user = User.objects.get(id=pk)
        except ObjectDoesNotExist:
            return Response(
                {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
