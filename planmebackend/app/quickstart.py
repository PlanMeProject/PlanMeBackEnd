from datetime import datetime
import base64
from email.mime.text import MIMEText

from flow import InstalledAppFlow
from googleapiclient.discovery import build


class GoogleClassroomAPI:
    """
    A class to interact with Google Classroom API.

    This class provides methods to authenticate with Google Classroom,
    retrieve a list of courses, and fetch assignment details for specific courses.

    Attributes:
        service (Resource): A Google Classroom API service object.
    """

    def __init__(self):
        """
        Initializes the GoogleClassroomAPI object with a service connection to Google Classroom.
        """
        self.classroom_service, self.user_info_service = self.initialize_api()

    def initialize_api(self):
        """
        Initialize a connection to the Google Classroom API.

        Returns:
            service: A Resource object with methods for interacting with the service.
        """
        scopes = [
            "openid",
            "https://www.googleapis.com/auth/classroom.courses.readonly",
            "https://www.googleapis.com/auth/classroom.rosters.readonly",
            "https://www.googleapis.com/auth/classroom.course-work.readonly",
            "https://www.googleapis.com/auth/classroom.student-submissions.me.readonly",
            "https://www.googleapis.com/auth/userinfo.email",
            "https://www.googleapis.com/auth/gmail.send"
        ]

        flow = InstalledAppFlow.from_client_secrets_file("credentials.json", scopes)
        flow.redirect_uri = 'http://localhost:57747/'
        local_server, wsgi_app, auth_url = flow.run_local_server(port=0, open_browser=False)
        credentials = flow.get_credentials(wsgi_app, local_server)
        classroom_service = build("classroom", "v1", credentials=credentials)
        user_info_service = build("oauth2", "v2", credentials=credentials)
        gmail_service = build('gmail', 'v1', credentials=credentials)
        return classroom_service, user_info_service, gmail_service
    
    def get_user_email(self):
        """
        Retrieves the email address of the authenticated user.

        Returns:
            str: The user's email address.
        """
        user_info = self.user_info_service.userinfo().get().execute()
        return user_info.get('email')

    def get_courses(self):
        """
        Retrieves a list of courses where the student is enrolled.

        Returns:
            List[Dict]: A list of course dictionaries.
        """
        results = self.classroom_service.courses().list(studentId="me").execute()
        return results.get("courses", [])

    def get_works(self, course_id):
        """
        Retrieves coursework for the specified course.

        Parameters:
            course_id (str): The ID of the course.

        Returns:
            Dict: A dictionary containing course works.
        """
        coursework_results = self.classroom_service.courses().courseWork().list(courseId=course_id).execute()
        return coursework_results

    def get_student_submissions_batch(self, course_id, assignment_ids):
        """
        Fetch student submissions in batch for specific assignments.

        Parameters:
            course_id (str): The ID of the course.
            assignment_ids (List[str]): List of assignment IDs.

        Returns:
            Dict: A dictionary containing student submissions indexed by assignment IDs.
        """
        batch = self.classroom_service.new_batch_http_request()
        student_submissions = {}

        def callback(request_id, response, exception):
            if exception is None:
                student_submissions[request_id] = response

        for assignment_id in assignment_ids:
            req = (
                self.classroom_service.courses()
                .courseWork()
                .studentSubmissions()
                .list(courseId=course_id, courseWorkId=assignment_id, userId="me")
            )
            batch.add(req, callback=callback, request_id=assignment_id)

        batch.execute()
        return student_submissions

    def assignments_for_specific_course(self, course_identifier):
        """
        Retrieves and formats course and assignment information based on a course identifier.

        Parameters:
            course_identifier (str): Identifier (name or ID) of the course.

        Returns:
            Tuple[Dict, List[Dict]]: A tuple containing a dictionary of course details
            and a list of dictionaries of assignment details.
        """
        courses = self.get_courses()
        course = next(
            (
                course
                for course in courses
                if course.get("name") == course_identifier or course.get("id") == course_identifier
            ),
            None,
        )

        if not course:
            print(f"No course found with identifier {course_identifier}")
            return None, None

        return self.course_information(course)

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
        assignment_ids = [assignment["id"] for assignment in assignments]
        student_submissions = self.get_student_submissions_batch(course_data["course_id"], assignment_ids)

        assignments_info = []
        for assignment in assignments:
            submissions = student_submissions.get(assignment["id"], {}).get("studentSubmissions", [])

            not_done_submissions = [s for s in submissions if s.get("state") not in ["TURNED_IN", "RETURNED"]]

            if not not_done_submissions:
                continue

            due_date = assignment.get("dueDate")
            if due_date:
                date_obj = datetime(due_date["year"], due_date["month"], due_date["day"])
                due_date_str = date_obj.strftime("%Y-%m-%d")
            else:
                due_date_str = None

            info = {
                "course_id": course_data["course_id"],
                "title": assignment.get("title"),
                "description": assignment.get("description"),
                "due_date": due_date_str,
                "status": assignment.get("state"),
                "max_points": assignment.get("maxPoints"),
            }
            assignments_info.append(info)

        return course_data, assignments_info
    
    def send_email(self, recipient_email, subject, message_text):
        message = MIMEText(message_text)
        message['to'] = recipient_email
        message['subject'] = subject
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        message_body = {'raw': raw_message}
        try:
            send_message = self.gmail_service.users().messages().send(userId='me', body=message_body).execute()
            print(f"Message Id: {send_message['id']}")
        except Exception as e:
            print(f'An error occurred: {e}')


if __name__ == "__main__":
    api = GoogleClassroomAPI()
    course_name = "219241 ISP"
    course_info, assignments_info = api.assignments_for_specific_course(course_name)
    user_email = api.get_user_email()

    if course_info and assignments_info:
        print("User Email:", user_email)
        print("Course Information:", course_info)
        print("Assignments Information:", assignments_info)
        print()
