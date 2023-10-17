from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    token = models.CharField(max_length=255, blank=True)

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateField()
    status = models.CharField(max_length=255)

class SubTask(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    summarized_text = models.TextField(blank=True)
    bullet_text = models.TextField(blank=True)
    due_date = models.DateField()
    status = models.CharField(max_length=255)

class Dashboard(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class DataVisualization(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=255)
