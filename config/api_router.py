from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from planmebackend.app.api.views import UserViewSet, TaskViewSet, \
    SubTaskViewSet, DashboardViewSet, DataVisualizationViewSet


if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register(r'users', UserViewSet, basename='user')
router.register(r'tasks', TaskViewSet, basename='task')
router.register(r'subtasks', SubTaskViewSet, basename='subtask')
router.register(r'dashboards', DashboardViewSet, basename='dashboard')
router.register(r'data-visualizations', DataVisualizationViewSet,
                basename='data-visualization')


app_name = "api"
urlpatterns = router.urls
