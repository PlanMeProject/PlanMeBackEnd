import logging
from datetime import datetime

import requests
from decouple import config
from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.response import Response

from planmebackend.app.models import Task, User


class GoogleClassroomViewSet(viewsets.ViewSet):
    @staticmethod
    def exchange_code_for_token(authorization_code):
        token_url = config("TOKEN_URL")
        client_id = config("GOOGLE_CLIENT_ID")
        client_secret = config("GOOGLE_CLIENT_SECRET")
        redirect_uri = config("REDIRECT_URI")

        data = {
            "code": authorization_code,
            "client_id": client_id,
            "client_secret": client_secret,
            "redirect_uri": redirect_uri,
            "grant_type": "authorization_code",
        }

        response = requests.post(token_url, data=data)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception("Failed to retrieve tokens")

    @staticmethod
    def get_classroom_courses(access_token):
        url = "https://classroom.googleapis.com/v1/courses"
        headers = {"Authorization": f"Bearer {access_token}"}

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception("Failed to retrieve classroom data")

    @staticmethod
    def parse_due_date(due_date_dict):
        if due_date_dict:
            return datetime(due_date_dict["year"], due_date_dict["month"], due_date_dict["day"]).date()
        return timezone.now().date()

    def create_tasks_for_user(self, user, classroom_data):
        for course in classroom_data.get("courses", []):
            for assignment in course.get("courseWork", []):
                task_data = {
                    "title": assignment["title"],
                    "description": assignment.get("description", ""),
                    "summarized_text": "",  # Placeholder
                    "due_date": self.parse_due_date(assignment.get("dueDate")),
                    "status": "Pending",
                    "user": user,
                }
                Task.objects.create(**task_data)

    def create(self, request, *args, **kwargs):
        authorization_code = request.data.get("authorization_code")

        if not authorization_code:
            return Response({"error": "Authorization code not provided"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            tokens = self.exchange_code_for_token(authorization_code)
            classroom_data = self.get_classroom_courses(tokens["access_token"])

            user_email = classroom_data["userEmail"]  # Extract user email from classroom data
            user, created = User.objects.get_or_create(
                username=user_email, defaults={"email": user_email, "token": tokens["access_token"]}
            )

            self.create_tasks_for_user(user, classroom_data)

            return Response({"user_id": user.id}, status=status.HTTP_201_CREATED)

        except Exception as e:
            logging.error(e)
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
