from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


class GoogleClassroomAPI:
    """A class to interact with Google Classroom API."""

    def __init__(self):
        """
        Initializes the GoogleClassroomAPI object with a service connection to Google Classroom.
        """
        self.service = self.initialize_api()

    def initialize_api(self):
        """
        Initialize a connection to the Google Classroom API.

        Returns:
            service: A Resource object with methods for interacting with the service.
        """
        scopes = [
            "https://www.googleapis.com/auth/classroom.courses.readonly",
            "https://www.googleapis.com/auth/classroom.rosters.readonly",
            "https://www.googleapis.com/auth/classroom.course-work.readonly",
            "https://www.googleapis.com/auth/classroom.student-submissions.me.readonly",
        ]

        flow = InstalledAppFlow.from_client_secrets_file("credentials.json", scopes)
        credentials = flow.run_local_server(port=0)
        service = build("classroom", "v1", credentials=credentials)

        return service

    def get_courses(self):
        """
        Retrieves a list of courses where the student is enrolled.

        Returns:
            List[Dict]: A list of course dictionaries.
        """
        results = self.service.courses().list(studentId="me").execute()
        return results.get("courses", [])

    def get_students(self, course_id):
        """
        Retrieves a list of students enrolled in the specified course.

        Parameters:
            course_id (str): The ID of the course.

        Returns:
            List[Dict]: A list of student dictionaries.
        """
        students_results = self.service.courses().students().list(courseId=course_id).execute()
        return students_results.get("students", [])

    def get_works(self, course_id):
        """
        Retrieves coursework for the specified course.

        Parameters:
            course_id (str): The ID of the course.

        Returns:
            Dict: A dictionary containing course works.
        """
        coursework_results = self.service.courses().courseWork().list(courseId=course_id).execute()
        return coursework_results

    def student_information(self, students):
        """
        Formats student information.

        Parameters:
            students (List[Dict]): A list of student dictionaries.

        Returns:
            List[Dict]: A list of formatted student dictionaries.
        """
        student_info = []
        for student in students:
            info = {
                "course_id": student["courseId"],
                "user_id": student["userId"],
                "name": student["profile"]["name"]["givenName"],
                "family_name": student["profile"]["name"]["familyName"],
                "full_name": student["profile"]["name"]["fullName"],
            }
            student_info.append(info)
        return student_info

    def course_information(self, course):
        """
        Retrieves and formats course and assignment information for the specified course.

        Parameters:
            course (Dict): A dictionary containing course details.

        Returns:
            Tuple[Dict, List[Dict]]: A tuple containing a dictionary of course details
            and a list of dictionaries of assignment details.
        """
        # Course Data
        course_data = {
            "course_id": course["id"],
            "course_name": course["name"],
            "course_section": course.get("section"),
            "course_description": course.get("description"),
            "course_status": course.get("courseState"),
        }

        # Assignments Information
        assignments = self.get_works(course_data["course_id"]).get("courseWork", [])
        assignments_info = []

        for assignment in assignments:
            submissions_results = (
                self.service.courses()
                .courseWork()
                .studentSubmissions()
                .list(courseId=course_data["course_id"], courseWorkId=assignment["id"], userId="me")
                .execute()
            )
            submissions = submissions_results.get("studentSubmissions", [])

            if not any(submission.get("state") in ["TURNED_IN", "RETURNED"] for submission in submissions):
                info = {
                    "course_id": course_data["course_id"],
                    "title": assignment.get("title"),
                    "description": assignment.get("description"),
                    "due_date": "{}-{}-{}".format(
                        assignment.get("dueDate", {}).get("year"),
                        assignment.get("dueDate", {}).get("month"),
                        assignment.get("dueDate", {}).get("day"),
                    ),
                    "status": assignment.get("state"),
                    "max_points": assignment.get("maxPoints"),
                }
                assignments_info.append(info)

        return course_data, assignments_info


if __name__ == "__main__":
    api = GoogleClassroomAPI()
    courses = api.get_courses()
    for course in courses:
        course_info, assignments_info = api.course_information(course)
        print("Course Information:", course_info)
        print("Assignments Information:", assignments_info)
        print()
