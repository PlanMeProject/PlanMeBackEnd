"""
The models module defines the data models used in the project.

- User: Represents an authenticated user with a unique ID and token.
- Task: Represents a task object associated with a user.
- SubTask: Represents a sub-task under a main task.
- Dashboard: Represents a dashboard associated with a user.
- DataVisualization: Represents data visualizations associated with tasks.
"""
from django.db import models
from utils.model_abstracts import Model


class User(Model):
    """Model definition for User."""
    class Meta:
        """Meta definition for User."""
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ['id']

    token = models.CharField(max_length=255)

    def __str__(self):
        """Unicode's representation of User."""
        return self.id


class Task(Model):
    """Model definition for Task."""
    class Meta:
        """Meta definition for Task."""
        verbose_name = "Task"
        verbose_name_plural = "Tasks"
        ordering = ['due_date']

    title = models.CharField(max_length=255)
    description = models.TextField()
    summarized_text = models.TextField()
    bullet_text = models.TextField()
    due_date = models.DateField()
    status = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name="tasks")

    def __str__(self):
        """Unicode's representation of Task."""
        return self.title


class SubTask(Model):
    """Model definition for SubTask."""
    class Meta:
        """Meta definition for SubTask."""
        verbose_name = "SubTask"
        verbose_name_plural = "SubTasks"
        ordering = ['id']

    title = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    task = models.ForeignKey(Task, on_delete=models.CASCADE,
                             related_name="subtasks")

    def __str__(self):
        """Unicode's representation of SubTask."""
        return self.title


class Dashboard(Model):
    """Model definition for Dashboard."""
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name="dashboard")


class DataVisualization(Model):
    """Model definition for DataVisualization."""
    task = models.ForeignKey(Task, on_delete=models.CASCADE,
                             related_name="data_visualization")
