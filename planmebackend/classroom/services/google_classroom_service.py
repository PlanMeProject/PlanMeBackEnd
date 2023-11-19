"""The module defines the GoogleClassroomAPI class."""
from datetime import date

from planmebackend.utils.request_handler import HTTPRequestHandler

GOOGLE_CLASSROOM_API_BASE = "https://classroom.googleapis.com/v1"
COURSE_WORK_ENDPOINT = "/courses/{course_id}/courseWork"
STUDENT_SUBMISSIONS_ENDPOINT = "/courses/{course_id}/courseWork/{course_work_id}/studentSubmissions"


class GoogleClassroomAPI:
    """Class definition for GoogleClassroomAPI."""

    @classmethod
    def get_course_work(cls, access_token, course_id):
        """Get course work from Google Classroom."""
        url = f"{GOOGLE_CLASSROOM_API_BASE}{COURSE_WORK_ENDPOINT.format(course_id=course_id)}"
        headers = {"Authorization": f"Bearer {access_token}"}
        return HTTPRequestHandler.make_request("GET", url, headers=headers).get("courseWork", [])

    @classmethod
    def get_student_submissions(cls, access_token, course_id, course_work_id):
        """Get student submissions from Google Classroom."""
        url = (
            f"{GOOGLE_CLASSROOM_API_BASE}"
            f"{STUDENT_SUBMISSIONS_ENDPOINT.format(course_id=course_id, course_work_id=course_work_id)}"
        )
        headers = {"Authorization": f"Bearer {access_token}"}
        return HTTPRequestHandler.make_request("GET", url, headers=headers).get("studentSubmissions", [])

    @classmethod
    def should_skip_assignment(cls, access_token, course_id, assignment):
        """Check if assignment should be skipped."""
        student_submissions = cls.get_student_submissions(access_token, course_id, assignment.get("id"))
        return not student_submissions or student_submissions[0].get("state") in ["TURNED_IN", "RETURNED"]

    @staticmethod
    def parse_due_date(due_date_data):
        """Parse due date from due date data."""
        if not due_date_data:
            return None
        return date(
            year=due_date_data.get("year", None),
            month=due_date_data.get("month", None),
            day=due_date_data.get("day", None),
        )
