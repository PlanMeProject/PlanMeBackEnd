"""The module defines the User model."""
from django.contrib.auth.models import AbstractUser
from django.db import models

from planmebackend.utils.model_abstracts import AbstractModel


class User(AbstractUser, AbstractModel):
    """
    Represents a user in the system.

    This model extends Django's AbstractUser and AbstractModel,
    providing additional fields specific to the system's requirements
    for user management.

    :param token: A unique token associated with the user for
    authentication or other purposes.
    :type token: models.CharField
    :param username: The username of the user. Note that in this model,
    usernames are not unique.
    :type username: models.CharField
    :param email: The email address of the user, which is unique
    across the system.
    :type email: models.EmailField
    """

    class Meta:
        """Meta definition for User."""

        app_label = "app"
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ["id"]

    token = models.CharField(max_length=255)
    username = models.CharField(max_length=150, unique=False)
    email = models.EmailField(max_length=254, unique=True)
