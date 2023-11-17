from datetime import datetime, timedelta
import json
import smtplib
from email.mime.multipart import MIMEMultipart
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
        self.assignments_seen = self.load_seen_assignments()

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
            "https://www.googleapis.com/auth/classroom.coursework.me"
        ]

        flow = InstalledAppFlow.from_client_secrets_file("credentials.json", scopes)
        flow.redirect_uri = 'http://localhost:57747/'
        local_server, wsgi_app, auth_url = flow.run_local_server(port=0, open_browser=False)
        credentials = flow.get_credentials(wsgi_app, local_server)
        classroom_service = build("classroom", "v1", credentials=credentials)
        user_info_service = build("oauth2", "v2", credentials=credentials)
        return classroom_service, user_info_service
    
    def get_user_email(self):
        """
        Retrieves the email address of the authenticated user.

        Returns:
            str: The user's email address.
        """
        user_info = self.user_info_service.userinfo().get().execute()
        return user_info.get('email')
    
    def send_email(self, recipient_email, subject, body):
        """
        Sends an email to the specified recipient.
        """
        sender_email = "planmeproject.app@gmail.com"
        password = "gopc cpyi lzhi blnx"

        # Create MIME object
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        # Setup the SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, password)

        # Send the email and close the connection
        server.send_message(msg)
        server.quit()
    
    def load_seen_assignments(self):
        """Load seen assignments from a file."""
        try:
            with open('assignments_seen.json', 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def save_seen_assignments(self):
        """Save seen assignments to a file."""
        with open('assignments_seen.json', 'w') as file:
            json.dump(self.assignments_seen, file)

    def check_for_new_assignments(self):
        """
        Modified method to check for new assignments and send email notifications.
        """
        today = datetime.today().date()
        recipient_email = self.get_user_email()
        courses = self.get_courses()

        for course in courses:
            course_data, assignments_info = self.course_information(course)

            for assignment in assignments_info:
                assignment_id = assignment['course_id'] + "_" + assignment['title']
                if assignment['due_date']:
                    due_date = datetime.strptime(assignment['due_date'], '%Y-%m-%d').date()
                else:
                    continue

                # Check if this is the first time seeing the assignment
                if assignment_id not in self.assignments_seen:
                    self.assignments_seen[assignment_id] = today.isoformat()
                    email_subject = f"New Assignment in {course_data['course_name']}"
                    email_body = f"New assignment: {assignment['title']}"
                    self.send_email(recipient_email, email_subject, email_body)

                # Check if today is three days before the due date
                elif due_date - today == timedelta(days=3):
                    email_subject = f"Upcoming Assignment Due in {course_data['course_name']}"
                    email_body = f"{assignment['title']} is due in 3 days"
                    self.send_email(recipient_email, email_subject, email_body)

        self.save_seen_assignments()

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


if __name__ == "__main__":
    classroom_api = GoogleClassroomAPI()
    classroom_api.check_for_new_assignments()
