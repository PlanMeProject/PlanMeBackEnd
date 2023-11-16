"""
The models module defines the data models used in the project.

- User: Represents an authenticated user with a unique ID and token.
- Task: Represents a task object associated with a user.
- SubTask: Represents a sub-task under a main task.
"""
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
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks")

    def __str__(self):
        """Unicode's representation of Task."""
        return self.title


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
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="subtasks")

    def __str__(self):
        """Unicode's representation of SubTask."""
        return self.title
