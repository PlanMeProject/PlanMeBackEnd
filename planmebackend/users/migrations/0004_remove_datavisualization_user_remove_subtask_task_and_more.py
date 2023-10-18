# Generated by Django 4.2.6 on 2023-10-18 12:12

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0003_remove_user_first_name_remove_user_last_name_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="datavisualization",
            name="user",
        ),
        migrations.RemoveField(
            model_name="subtask",
            name="task",
        ),
        migrations.RemoveField(
            model_name="subtask",
            name="user",
        ),
        migrations.RemoveField(
            model_name="task",
            name="user",
        ),
        migrations.RemoveField(
            model_name="user",
            name="token",
        ),
        migrations.DeleteModel(
            name="Dashboard",
        ),
        migrations.DeleteModel(
            name="DataVisualization",
        ),
        migrations.DeleteModel(
            name="SubTask",
        ),
        migrations.DeleteModel(
            name="Task",
        ),
    ]
