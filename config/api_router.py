from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter
from rest_framework_nested import routers

from planmebackend.app.views import SubTaskViewSet, TaskViewSet, UserViewSet
from planmebackend.classroom.views import AssignmentsViewSet, AuthorizationViewSet, CoursesViewSet
from planmebackend.nlp.views import SummarizeViewSet, TTSViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet, basename="user")
router.register("authorize", AuthorizationViewSet, basename="authorize")
router.register("courses", CoursesViewSet, basename="courses")
router.register("assignments", AssignmentsViewSet, basename="assignments")
router.register("tts", TTSViewSet, basename="tts")
router.register("summarize", SummarizeViewSet, basename="summarize")

users_router = routers.NestedSimpleRouter(router, "users", lookup="user")
users_router.register("tasks", TaskViewSet, basename="user-tasks")

tasks_router = routers.NestedSimpleRouter(users_router, "tasks", lookup="task")
tasks_router.register("subtasks", SubTaskViewSet, basename="task-subtask")


app_name = "api"
urlpatterns = router.urls + users_router.urls + tasks_router.urls
