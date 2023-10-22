from django.contrib import admin

from .models import SubTask, Task, User

admin.site.register(User)
admin.site.register(Task)
admin.site.register(SubTask)
