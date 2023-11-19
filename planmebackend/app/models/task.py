"""The module defines the Task model."""
from django.db import models

from planmebackend.utils.model_abstracts import AbstractModel


class Task(AbstractModel):
    """Model definition for Task."""

    class Meta:
        """Meta definition for Task."""

        verbose_name = "Task"
        verbose_name_plural = "Tasks"
        ordering = ["due_date"]

    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True, default=None)
    summarized_text = models.TextField(null=True, blank=True, default=None)
    due_date = models.DateField(null=True, blank=True, default=None)
    status = models.CharField(max_length=255)
    course = models.CharField(
        max_length=255, null=True, blank=True, default=None
    )
    user = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="tasks"
    )

    def __str__(self):
        """Unicode's representation of Task."""
        return self.title
