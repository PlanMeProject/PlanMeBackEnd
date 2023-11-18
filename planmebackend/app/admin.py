"""Admin module for the app."""
from django.contrib import admin

from .models import DeletedTask, SubTask, Task, User

admin.site.register(User)
admin.site.register(Task)
admin.site.register(SubTask)
admin.site.register(DeletedTask)
