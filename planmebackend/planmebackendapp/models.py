from django.db import models


class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    token = models.CharField(max_length=255)


class Task(models.Model):
    task_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    summarized_text = models.TextField()
    bullet_text = models.TextField()
    due_date = models.DateField()
    status = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks")


class SubTask(models.Model):
    subtask_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="subtasks")
