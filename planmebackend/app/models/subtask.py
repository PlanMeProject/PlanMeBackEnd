from django.db import models

from planmebackend.utils.model_abstracts import AbstractModel


class SubTask(AbstractModel):
    """Model definition for SubTask."""

    class Meta:
        """Meta definition for SubTask."""

        app_label = "app"
        verbose_name = "SubTask"
        verbose_name_plural = "SubTasks"
        ordering = ["id"]

    title = models.CharField(max_length=255, null=True, blank=True, default="No title")
    status = models.CharField(max_length=255, null=True, blank=True, default="Todo")
    task = models.ForeignKey("Task", on_delete=models.CASCADE, related_name="subtasks")

    def __str__(self):
        """Unicode's representation of SubTask."""
        return self.title
