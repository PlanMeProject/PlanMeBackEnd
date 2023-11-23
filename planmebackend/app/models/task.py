"""The module defines the Task model."""
from django.db import models

from planmebackend.utils.model_abstracts import AbstractModel


class Task(AbstractModel):
    """
    Represents a task in the system.

    This model inherits from the AbstractModel and includes fields for
    task details such as title, description, due date, status, and more.

    :param title: The title of the task.
    :type title: models.CharField
    :param description: A detailed description of the task, can be null.
    :type description: models.TextField
    :param summarized_text: A summarized version of the task, can be null.
    :type summarized_text: models.TextField
    :param due_date: The due date of the task, can be null.
    :type due_date: models.DateField
    :param status: The current status of the task.
    """

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
