"""The module defines the GoogleClassroomAPI class."""
from datetime import date

from planmebackend.utils.request_handler import HTTPRequestHandler

GOOGLE_CLASSROOM_API_BASE = "https://classroom.googleapis.com/v1"
COURSE_WORK_ENDPOINT = "/courses/{course_id}/courseWork"
STUDENT_SUBMISSIONS_ENDPOINT = (
    "/courses/{course_id}/courseWork/" "{course_work_id}/studentSubmissions"
)


class GoogleClassroomAPI:
    """Class definition for GoogleClassroomAPI."""

    @classmethod
    def get_course_work(cls, access_token, course_id):
        """
        Retrieve course work from Google Classroom.

        :param access_token: Access token for API.
        :param course_id: ID of the course.
        :return: Course work data.
        """
        url = (
            f"{GOOGLE_CLASSROOM_API_BASE}"
            f"{COURSE_WORK_ENDPOINT.format(course_id=course_id)}"
        )
        headers = {"Authorization": f"Bearer {access_token}"}
        return HTTPRequestHandler.make_request(
            "GET", url, headers=headers
        ).get("courseWork", [])

    @classmethod
    def get_student_submissions(cls, access_token, course_id, course_work_id):
        """
        Get student submissions from Google Classroom.

        :param access_token: Access token for API.
        :param course_id: ID of the course.
        :param course_work_id: ID of the course work.
        :return: Student submissions data.
        """
        url = (
            f"{GOOGLE_CLASSROOM_API_BASE}"
            f"{STUDENT_SUBMISSIONS_ENDPOINT.format(course_id=course_id, course_work_id=course_work_id)}"  # noqa: E501
        )
        headers = {"Authorization": f"Bearer {access_token}"}
        return HTTPRequestHandler.make_request(
            "GET", url, headers=headers
        ).get("studentSubmissions", [])

    @classmethod
    def should_skip_assignment(cls, access_token, course_id, assignment):
        """
        Determine if an assignment should be skipped.

        :param access_token: Access token for API.
        :param course_id: ID of the course.
        :param assignment: Assignment data.
        :return: Boolean indicating if assignment should be skipped.
        """
        student_submissions = cls.get_student_submissions(
            access_token, course_id, assignment.get("id")
        )
        return not student_submissions or student_submissions[0].get(
            "state"
        ) in ["TURNED_IN", "RETURNED"]

    @staticmethod
    def parse_due_date(due_date_data):
        """
        Parse due date from provided data.

        :param due_date_data: Due date data.
        :return: Parsed due date or None.
        """
        if not due_date_data:
            return None
        return date(
            year=due_date_data.get("year", None),
            month=due_date_data.get("month", None),
            day=due_date_data.get("day", None),
        )
