import logging

import requests
from rest_framework import status, viewsets
from rest_framework.response import Response


class CoursesViewSet(viewsets.ViewSet):
    @staticmethod
    def get_classroom_courses(access_token):
        url = "https://classroom.googleapis.com/v1/courses"
        headers = {"Authorization": f"Bearer {access_token}"}

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception("Failed to retrieve classroom data")

    def create(self, request, *args, **kwargs):
        access_token = request.data.get("access_token")
        if not access_token:
            return Response({"error": "Access token not found in session"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            classroom_data = self.get_classroom_courses(access_token)
            courses = [{"title": course} for course in classroom_data.get("courses", [])]

            return Response(courses, status=status.HTTP_200_OK)

        except Exception as e:
            logging.error(e)
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
