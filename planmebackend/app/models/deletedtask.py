"""The module defines the DeletedTask model."""
from django.db import models

from planmebackend.utils.model_abstracts import AbstractModel


class DeletedTask(AbstractModel):
    """
    Represents a task that has been marked as deleted in the system.

    This model inherits from the AbstractModel and adds specific fields
    for a deleted task.

    :param title: The title of the deleted task.
    :type title: models.CharField
    :param course: The course associated with the deleted task, can be null.
    :type course: models.CharField
    :param user: The user who deleted the task.
    :type user: models.ForeignKey
    """

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
