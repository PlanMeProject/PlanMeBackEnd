import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime, timedelta

class NotificationSystem:
    """
    A system to send notifications about new assignments or upcoming deadlines
    based on information from a classroom API.
    """
    def __init__(self, classroom_api):
        """
        Initialize the NotificationSystem with a classroom API.
        """
        self.classroom_api = classroom_api
        self.assignments_seen = self.load_seen_assignments()

    def send_email(self, recipient_email, subject, body):
        """
        Send an email with the given recipient, subject, and body.
        """
        sender_email = "planmeproject.app@gmail.com"
        password = "your_password_here"  # Password should be secured

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, password)
        server.send_message(msg)
        server.quit()

    def load_seen_assignments(self):
        """
        Load seen assignments from a file.
        """
        try:
            with open('assignments_seen.json', 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def save_seen_assignments(self):
        """
        Save the seen assignments to a file.
        """
        with open('assignments_seen.json', 'w', encoding='utf-8') as file:
            json.dump(self.assignments_seen, file)

    def check_for_new_assignments(self):
        """
        Check for new assignments and send notifications accordingly.
        """
        today = datetime.today().date()
        recipient_email = self.classroom_api.get_user_email()
        courses = self.classroom_api.get_courses()

        for course in courses:
            course_data, assignments_info = self.classroom_api.course_information(course)

            for assignment in assignments_info:
                assignment_id = f"{assignment['course_id']}_{assignment['title']}"
                if assignment['due_date']:
                    due_date = datetime.strptime(assignment['due_date'], '%Y-%m-%d').date()
                else:
                    continue

                if assignment_id not in self.assignments_seen:
                    self.assignments_seen[assignment_id] = today.isoformat()
                    email_subject = f"New Assignment in {course_data['course_name']}"
                    email_body = f"New assignment: {assignment['title']} due in {assignment['due_date']}"
                    self.send_email(recipient_email, email_subject, email_body)

                elif due_date - today == timedelta(days=3):
                    email_subject = f"Upcoming Assignment Due in {course_data['course_name']}"
                    email_body = f"{assignment['title']} is due in 3 days"
                    self.send_email(recipient_email, email_subject, email_body)

        self.save_seen_assignments()
