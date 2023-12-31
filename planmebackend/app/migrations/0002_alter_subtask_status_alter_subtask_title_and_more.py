# Generated by Django 4.2.7 on 2023-11-16 02:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subtask',
            name='status',
            field=models.CharField(blank=True, default='Todo', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='subtask',
            name='title',
            field=models.CharField(blank=True, default='No title', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='description',
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='due_date',
            field=models.DateField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='summarized_text',
            field=models.TextField(blank=True, default=None, null=True),
        ),
    ]
