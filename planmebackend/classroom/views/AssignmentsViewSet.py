import logging
from datetime import datetime

import requests
from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.response import Response


class AssignmentsViewSet(viewsets.ViewSet):
    @staticmethod
    def get_course_assignments(access_token, course_id):
        url = f"https://classroom.googleapis.com/v1/courses/{course_id}/courseWork"
        headers = {"Authorization": f"Bearer {access_token}"}

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json().get("courseWork", [])
        else:
            raise Exception("Failed to retrieve course assignments")

    @staticmethod
    def parse_due_date(due_date_dict):
        if due_date_dict:
            return datetime(due_date_dict["year"], due_date_dict["month"], due_date_dict["day"]).date()
        return timezone.now().date()

    def create(self, request, *args, **kwargs):
        course_id = request.data.get("course_id")
        if not course_id:
            return Response({"error": "Course ID not provided"}, status=status.HTTP_400_BAD_REQUEST)

        access_token = request.session.get("access_token")
        if not access_token:
            return Response({"error": "Access token not found in session"}, status=status.HTTP_400_BAD_REQUEST)
        #
        try:
            #     assignments_data = self.get_course_assignments(access_token, course_id)
            #
            #     # for assignment in assignments_data:
            #     #     # Logic to save assignments to the database
            #     #     # ...
            #
            return Response({"message": "Assignments saved"}, status=status.HTTP_201_CREATED)
        #
        except Exception as e:
            logging.error(e)
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
