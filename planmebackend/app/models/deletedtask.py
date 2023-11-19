"""The module defines the DeletedTask model."""
from django.db import models

from planmebackend.utils.model_abstracts import AbstractModel


class DeletedTask(AbstractModel):
    """Model definition for DeletedTask."""

    class Meta:
        """Meta definition for DeletedTask."""

        verbose_name = "DeletedTask"
        verbose_name_plural = "DeletedTasks"
        ordering = ["id"]

    title = models.CharField(max_length=255)
    course = models.CharField(
        max_length=255, null=True, blank=True, default=None
    )
    user = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="deleted_tasks"
    )
