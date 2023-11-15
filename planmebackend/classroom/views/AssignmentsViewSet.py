import logging

import requests

# from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.response import Response

# from datetime import datetime


# from planmebackend.classroom.views.CoursesViewSet import CoursesViewSet


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
            # raise Exception("Failed to retrieve course assignments", response.text)

    @staticmethod
    def get_student_submissions(access_token, course_id, course_work_id):
        url = f"https://classroom.googleapis.com/v1/courses/{course_id}/courseWork/{course_work_id}/studentSubmissions"
        headers = {"Authorization": f"Bearer {access_token}"}

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json().get("studentSubmissions", [])
        else:
            raise Exception("Failed to retrieve student submissions")

    def create(self, request, *args, **kwargs):
        courses = request.data.get("all_courses").get("data", [])
        access_token = request.data.get("access_token")

        if not access_token:
            return Response({"error": "Access token not found"}, status=status.HTTP_400_BAD_REQUEST)

        if not courses:
            return Response({"error": "All courses not provided"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            unsubmitted_assignments = []

            for course in courses:
                course_id = course.get("title", {}).get("id", "")
                assignments = self.get_course_work(access_token, course_id)
                for assignment in assignments:
                    student_submissions = self.get_student_submissions(access_token, course_id, assignment["id"])
                    unsubmitted_assignments.append(student_submissions)
                #     if student_submissions and student_submissions[0].get("state") not in ["TURNED_IN", "RETURNED"]:
                #     unsubmitted_assignments.append(assignment)
                # unsubmitted_assignments.append(assignments)

            return Response({"unsubmitted_assignments": unsubmitted_assignments}, status=status.HTTP_201_CREATED)

        except Exception as e:
            logging.error(e)
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
