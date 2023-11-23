"""The module defines the SubTask model."""
from django.db import models

from planmebackend.utils.model_abstracts import AbstractModel


class SubTask(AbstractModel):
    """
    Represents a subtask of a main task in the system.

    This model inherits from the AbstractModel and contains details
    about a subtask like its title, status, and associated main task.

    :param title: The title of the subtask, defaults to 'No title'.
    :type title: models.CharField
    :param status: The current status of the subtask, defaults to 'Todo'.
    :type status: models.CharField
    :param task: The main task to which this subtask is linked.
    :type task: models.ForeignKey

    :return: A string representation of the subtask's title.
    :rtype: str
    """

    class Meta:
        """Meta definition for SubTask."""

        app_label = "app"
        verbose_name = "SubTask"
        verbose_name_plural = "SubTasks"
        ordering = ["id"]

    title = models.CharField(
        max_length=255, null=True, blank=True, default="No title"
    )
    status = models.CharField(
        max_length=255, null=True, blank=True, default="Todo"
    )
    task = models.ForeignKey(
        "Task", on_delete=models.CASCADE, related_name="subtasks"
    )

    def __str__(self):
        """Unicode's representation of SubTask."""
        return self.title
