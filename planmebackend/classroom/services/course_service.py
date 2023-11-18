"""The module defines the CoursesService class."""
from planmebackend.utils.request_handler import HTTPRequestHandler


class CoursesService:
    """Class definition for CoursesService."""

    @staticmethod
    def get_classroom_courses(access_token):
        """Get courses from Google Classroom."""
        url = "https://classroom.googleapis.com/v1/courses"
        headers = {"Authorization": f"Bearer {access_token}"}
        return HTTPRequestHandler.make_request("GET", url, headers=headers)
