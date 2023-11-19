"""The module defines the AssignmentsViewSet class."""
from rest_framework import status, viewsets
from rest_framework.response import Response

from planmebackend.app.models import Task
from planmebackend.app.serializers import TaskSerializer
from planmebackend.classroom.services import AssignmentsService


class AssignmentsViewSet(viewsets.ViewSet):
    """Class definition for AssignmentsViewSet."""

    def create(self, request, *args, **kwargs):
        """Create tasks from Google Classroom."""
        data = request.data
        access_token = data.get("access_token")
        courses = data.get("all_courses", {}).get("data", [])
        check_status = data.get("check_status", "")
        user_id = data.get("user_id")

        if not all([access_token, courses, user_id]):
            return Response({"error": "Missing required data"}, status=status.HTTP_400_BAD_REQUEST)

        service = AssignmentsService()
        user = service.get_user(user_id)
        new_tasks = service.process_courses(courses, access_token, check_status, user)

        Task.objects.bulk_create(new_tasks)
        serializer = TaskSerializer(new_tasks, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
