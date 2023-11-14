# import logging
# from datetime import datetime
#
# import requests
# from decouple import config
# from django.utils import timezone
# from rest_framework import status, viewsets
# from rest_framework.response import Response
#
# from planmebackend.app.models import Task, User
#
#
# class ClassroomDataViewSet(viewsets.ViewSet):
#     @staticmethod
#     def exchange_code_for_token(authorization_code):
#         token_url = config("TOKEN_URL")
#         client_id = config("GOOGLE_CLIENT_ID")
#         client_secret = config("GOOGLE_CLIENT_SECRET")
#         redirect_uri = config("REDIRECT_URI")
#
#         data = {
#             "code": authorization_code,
#             "client_id": client_id,
#             "client_secret": client_secret,
#             "redirect_uri": redirect_uri,
#             "grant_type": "authorization_code",
#         }
#
#         response = requests.post(token_url, data=data)
#         if response.status_code == 200:
#             return response.json()
#         else:
#             print(response.text)
#             raise Exception("Failed to retrieve tokens")
#
#     @staticmethod
#     def get_classroom_courses(access_token):
#         url = "https://classroom.googleapis.com/v1/courses"
#         headers = {"Authorization": f"Bearer {access_token}"}
#
#         response = requests.get(url, headers=headers)
#         if response.status_code == 200:
#             return response.json()
#         else:
#             raise Exception("Failed to retrieve classroom data")
#
#     @staticmethod
#     def get_user_profile(access_token):
#         url = "https://www.googleapis.com/oauth2/v2/userinfo"
#         headers = {"Authorization": f"Bearer {access_token}"}
#
#         response = requests.get(url, headers=headers)
#         if response.status_code == 200:
#             return response.json()
#         else:
#             print(f"Error fetching user profile: Status Code: {response.status_code}, Response: {response.text}")
#             raise Exception("Failed to retrieve user profile data")
#
#     @staticmethod
#     def get_course_assignments(access_token, course_id):
#         url = f"https://classroom.googleapis.com/v1/courses/{course_id}/courseWork"
#         headers = {"Authorization": f"Bearer {access_token}"}
#
#         response = requests.get(url, headers=headers)
#         if response.status_code == 200:
#             return response.json().get("courseWork", [])
#         else:
#             raise Exception("Failed to retrieve course assignments")
#
#     def create_tasks_for_user(self, user, classroom_data, access_token):
#         for course in classroom_data.get("courses", []):
#             course_id = course.get("id")
#             assignments = self.get_course_assignments(access_token, course_id)
#
#             for assignment in assignments:
#                 if assignment.get("state") != "TURNED_IN":
#                     task, created = Task.objects.get_or_create(
#                         user=user,
#                         title=assignment.get("title", ""),
#                         defaults={
#                             "title": assignment.get("title", ""),
#                             "description": assignment.get("description", ""),
#                             "summarized_text": "",
#                             "due_date": self.parse_due_date(assignment.get("dueDate")),
#                             "status": "Todo",
#                         },
#                     )
#
#     @staticmethod
#     def parse_due_date(due_date_dict):
#         if due_date_dict:
#             return datetime(due_date_dict["year"], due_date_dict["month"], due_date_dict["day"]).date()
#         return timezone.now().date()
#
#     def create(self, request, *args, **kwargs):
#         authorization_code = request.session.get("authorization_code")
#         if not authorization_code:
#             return Response({"error": "Authorization code not found in session"}, status=status.HTTP_400_BAD_REQUEST)
#
#         try:
#             tokens = self.exchange_code_for_token(authorization_code)
#             user_profile = self.get_user_profile(tokens["access_token"])
#             user_email = user_profile.get("email")
#
#             user, created = User.objects.update_or_create(
#                 username=user_email, defaults={"email": user_email, "token": tokens["access_token"]}
#             )
#
#             classroom_data = self.get_classroom_courses(tokens["access_token"])
#             self.create_tasks_for_user(user, classroom_data, tokens["access_token"])
#
#             del request.session["authorization_code"]
#
#             return Response({"user_id": user.id}, status=status.HTTP_201_CREATED)
#
#         except Exception as e:
#             logging.error(e)
#             return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
