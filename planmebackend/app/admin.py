from django.contrib import admin
from .models import User, Task, SubTask


class UserAdmin(admin.ModelAdmin):
    list_display = 'username'
    search_fields = 'username'


admin.site.register(User, UserAdmin)
admin.site.register(Task)
admin.site.register(SubTask)
