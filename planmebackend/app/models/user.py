"""The module defines the User model."""
from django.contrib.auth.models import AbstractUser
from django.db import models

from planmebackend.utils.model_abstracts import AbstractModel


class User(AbstractUser, AbstractModel):
    """Model definition for User."""

    class Meta:
        """Meta definition for User."""

        app_label = "app"
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ["id"]

    token = models.CharField(max_length=255)
    username = models.CharField(max_length=150, unique=False)
    email = models.EmailField(max_length=254, unique=True)
