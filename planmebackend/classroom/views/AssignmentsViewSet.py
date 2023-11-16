import logging
from datetime import date

import requests
from django.contrib.auth import get_user_model
from rest_framework import status, viewsets
from rest_framework.response import Response

from planmebackend.app.models import Task
from planmebackend.app.serializers import TaskSerializer


class AssignmentsViewSet(viewsets.ViewSet):
    @staticmethod
    def get_course_work(access_token, course_id):
        url = f"https://classroom.googleapis.com/v1/courses/{course_id}/courseWork"
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return response.json().get("courseWork", [])
        else:
            raise Exception(f"Error fetching course work for course ID {course_id}: {response.text}")

    @staticmethod
    def get_student_submissions(access_token, course_id, course_work_id):
        url = f"https://classroom.googleapis.com/v1/courses/{course_id}/courseWork/{course_work_id}/studentSubmissions"
        headers = {"Authorization": f"Bearer {access_token}"}

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json().get("studentSubmissions", [])
        else:
            raise Exception("Failed to retrieve student submissions", response.text)

    def create(self, request, *args, **kwargs):
        courses = request.data.get("all_courses").get("data", [])
        access_token = request.data.get("access_token")
        check_status = request.data.get("check_status", "")
        user_id = request.data.get("user_id", None)

        if not access_token:
            return Response({"error": "Access token not found"}, status=status.HTTP_400_BAD_REQUEST)

        if not courses:
            return Response({"error": "All courses not provided"}, status=status.HTTP_400_BAD_REQUEST)

        if not user_id:
            return Response({"error": "User ID not provided"}, status=status.HTTP_400_BAD_REQUEST)

        User = get_user_model()
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        new_tasks = []

        try:
            for course in courses:
                course_id = course.get("title", {}).get("id", "")
                assignments = self.get_course_work(access_token, course_id)

                for assignment in assignments:
                    assignment_title = assignment.get("title")
                    due_date_data = assignment.get("dueDate", None)

                    if Task.objects.filter(title=assignment_title, user=user).exists():
                        continue

                    if due_date_data:
                        assignment_due_date = date(
                            year=due_date_data.get("year"),
                            month=due_date_data.get("month"),
                            day=due_date_data.get("day"),
                        )
                    else:
                        assignment_due_date = None

                    if check_status:
                        student_submissions = self.get_student_submissions(
                            access_token, course_id, assignment.get("id", None)
                        )
                        if not student_submissions or student_submissions[0].get("state") in ["TURNED_IN", "RETURNED"]:
                            continue

                    new_tasks.append(
                        Task(
                            title=assignment.get("title", ""),
                            description=assignment.get("description", ""),
                            summarized_text=assignment.get("description", ""),
                            due_date=assignment_due_date,
                            status="Todo",
                            user=user,
                        )
                    )

            Task.objects.bulk_create(new_tasks)

            all_tasks = Task.objects.filter(user=user)
            serializer = TaskSerializer(all_tasks, many=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            logging.error(e)
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
