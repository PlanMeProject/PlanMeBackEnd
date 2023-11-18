"""The module defines the ClassroomConfig class."""
from django.apps import AppConfig


class ClassroomConfig(AppConfig):
    """Class definition for ClassroomConfig."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "classroom"
