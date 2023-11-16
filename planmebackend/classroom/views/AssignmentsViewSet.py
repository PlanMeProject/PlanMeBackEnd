import logging
from datetime import date

import requests
from django.contrib.auth import get_user_model
from rest_framework import status, viewsets
from rest_framework.response import Response

from planmebackend.app.models import Task
from planmebackend.app.serializers import TaskSerializer

GOOGLE_CLASSROOM_API_BASE = "https://classroom.googleapis.com/v1"
COURSE_WORK_ENDPOINT = "/courses/{course_id}/courseWork"
STUDENT_SUBMISSIONS_ENDPOINT = "/courses/{course_id}/courseWork/{course_work_id}/studentSubmissions"


class GoogleClassroomAPI:
    @staticmethod
    def _make_request(url, headers):
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            logging.error(f"Google Classroom API error: {response.text}")
            raise Exception(f"API Request failed: {response.text}")
        return response.json()

    @classmethod
    def get_course_work(cls, access_token, course_id):
        url = f"{GOOGLE_CLASSROOM_API_BASE}" f"{COURSE_WORK_ENDPOINT.format(course_id=course_id)}"
        headers = {"Authorization": f"Bearer {access_token}"}
        return cls._make_request(url, headers).get("courseWork", [])

    @classmethod
    def get_student_submissions(cls, access_token, course_id, course_work_id):
        url = (
            f"{GOOGLE_CLASSROOM_API_BASE}"
            f"{STUDENT_SUBMISSIONS_ENDPOINT.format(course_id=course_id, course_work_id=course_work_id)}"
        )
        headers = {"Authorization": f"Bearer {access_token}"}
        return cls._make_request(url, headers).get("studentSubmissions", [])


class AssignmentsViewSet(viewsets.ViewSet):
    def create(self, request, *args, **kwargs):
        data = request.data
        access_token = data.get("access_token")
        courses = data.get("all_courses", {}).get("data", [])
        check_status = data.get("check_status", "")
        user_id = data.get("user_id")

        if not all([access_token, courses, user_id]):
            return Response({"error": "Missing required data"}, status=status.HTTP_400_BAD_REQUEST)

        user = self._get_user(user_id)
        new_tasks = self._process_courses(courses, access_token, check_status, user)

        Task.objects.bulk_create(new_tasks)
        all_tasks = Task.objects.filter(user=user)
        serializer = TaskSerializer(all_tasks, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @staticmethod
    def _get_user(user_id):
        User = get_user_model()
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise Exception("User not found")

    def _process_courses(self, courses, access_token, check_status, user):
        new_tasks = []
        for course in courses:
            course_id = course.get("title", {}).get("id", "")
            assignments = GoogleClassroomAPI.get_course_work(access_token, course_id)
            new_tasks.extend(self._process_assignments(assignments, course_id, access_token, check_status, user))
        return new_tasks

    def _process_assignments(self, assignments, course_id, access_token, check_status, user):
        tasks = []
        for assignment in assignments:
            if Task.objects.filter(title=assignment.get("title"), user=user).exists():
                continue

            if check_status and self._should_skip_assignment(access_token, course_id, assignment):
                continue

            due_date_data = assignment.get("dueDate")
            due_date = self._parse_due_date(due_date_data) if due_date_data else None

            tasks.append(
                Task(
                    title=assignment.get("title", ""),
                    description=assignment.get("description", ""),
                    summarized_text=assignment.get("description", ""),
                    due_date=due_date,
                    status="Todo",
                    user=user,
                )
            )
        return tasks

    @staticmethod
    def _should_skip_assignment(access_token, course_id, assignment):
        student_submissions = GoogleClassroomAPI.get_student_submissions(access_token, course_id, assignment.get("id"))
        return not student_submissions or student_submissions[0].get("state") in ["TURNED_IN", "RETURNED"]

    @staticmethod
    def _parse_due_date(due_date_data):
        return date(
            year=due_date_data.get("year"),
            month=due_date_data.get("month"),
            day=due_date_data.get("day"),
        )
