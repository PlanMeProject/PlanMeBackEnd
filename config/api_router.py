from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter
from rest_framework_nested import routers

from planmebackend.app.api.views import (
    DashboardViewSet,
    DataVisualizationViewSet,
    SubTaskViewSet,
    TaskViewSet,
    UserViewSet,
)

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet, basename="user")

users_router = routers.NestedSimpleRouter(router, "users", lookup="user")
users_router.register("tasks", TaskViewSet, basename="user-tasks")  # Tasks nested inside users
users_router.register("dashboard", DashboardViewSet, basename="user-dashboard")

tasks_router = routers.NestedSimpleRouter(users_router, "tasks", lookup="task")
tasks_router.register("subtasks", SubTaskViewSet, basename="task-subtask")
tasks_router.register("visualization", DataVisualizationViewSet, basename="task-visualization")

app_name = "api"
urlpatterns = router.urls + users_router.urls + tasks_router.urls
