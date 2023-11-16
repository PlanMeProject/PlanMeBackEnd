from datetime import date

from planmebackend.utils.request_handler import HTTPRequestHandler

GOOGLE_CLASSROOM_API_BASE = "https://classroom.googleapis.com/v1"
COURSE_WORK_ENDPOINT = "/courses/{course_id}/courseWork"
STUDENT_SUBMISSIONS_ENDPOINT = "/courses/{course_id}/courseWork/{course_work_id}/studentSubmissions"


class GoogleClassroomAPI:
    @classmethod
    def get_course_work(cls, access_token, course_id):
        url = f"{GOOGLE_CLASSROOM_API_BASE}{COURSE_WORK_ENDPOINT.format(course_id=course_id)}"
        headers = {"Authorization": f"Bearer {access_token}"}
        return HTTPRequestHandler.make_request("GET", url, headers=headers).get("courseWork", [])

    @classmethod
    def get_student_submissions(cls, access_token, course_id, course_work_id):
        url = (
            f"{GOOGLE_CLASSROOM_API_BASE}"
            f"{STUDENT_SUBMISSIONS_ENDPOINT.format(course_id=course_id, course_work_id=course_work_id)}"
        )
        headers = {"Authorization": f"Bearer {access_token}"}
        return HTTPRequestHandler.make_request("GET", url, headers=headers).get("studentSubmissions", [])

    @classmethod
    def should_skip_assignment(cls, access_token, course_id, assignment):
        student_submissions = cls.get_student_submissions(access_token, course_id, assignment.get("id"))
        return not student_submissions or student_submissions[0].get("state") in ["TURNED_IN", "RETURNED"]

    @staticmethod
    def parse_due_date(due_date_data):
        return date(
            year=due_date_data.get("year"),
            month=due_date_data.get("month"),
            day=due_date_data.get("day"),
        )
