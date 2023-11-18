import logging

from rest_framework import status, viewsets
from rest_framework.response import Response

from planmebackend.classroom.services import CoursesService


class CoursesViewSet(viewsets.ViewSet):
    def create(self, request, *args, **kwargs):
        access_token = request.data.get("access_token")
        if not access_token:
            return Response({"error": "Access token not found in session"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            service = CoursesService()
            classroom_data = service.get_classroom_courses(access_token)
            courses = [{"title": course} for course in classroom_data.get("courses", [])]

            return Response(courses, status=status.HTTP_200_OK)

        except Exception as e:
            logging.error(e)
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
