"""
This module defines the NotificationSystem class, which interfaces with a classroom API
to track assignments and send email notifications about new assignments or upcoming deadlines.
The system checks for new assignments, determines if they are due soon, and sends
corresponding notifications to the user.
"""

import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
from planmebackend.app.models import User, Task


class NotificationSystem:
    """
    A system to send notifications about new assignments or upcoming deadlines
    based on information from a classroom API.
    """
    def __init__(self):
        """
        Initialize the NotificationSystem with a classroom API.
        """
        self.assignments_seen = self.load_seen_assignments()

    def send_email(self, recipient_email, subject, body, html=False):
        """
        Send an email with the given recipient, subject, and body.
        """
        sender_email = "planmeproject.app@gmail.com"
        password = "gopc cpyi lzhi blnx"

        msg = MIMEMultipart('alternative')
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject

        if html:
            msg.attach(MIMEText(body, 'html'))
        else:
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
        Check for new tasks and send an HTML table of all tasks to the user.
        """
        today = datetime.today().date()
        
        # Query all users
        for user in User.objects.all():
            recipient_email = user.email
            tasks = user.tasks.filter(due_date__gte=today)

            assignments_list = []

            for task in tasks:
                task_id = f"{task.id}_{task.title}"
                due_date = task.due_date if task.due_date else None

                if due_date and (task_id not in self.assignments_seen):
                    self.assignments_seen[task_id] = today.isoformat()
                    assignments_list.append({
                        'course_name': 'N/A',
                        'title': task.title,
                        'due_date': due_date.strftime('%Y-%m-%d')
                    })

        # Formatting the assignments into an HTML table
        email_body = """
            <html>
                <head>
                    <style>
                        table {
                            width: 100%;
                            border-collapse: collapse;
                        }
                        th, td {
                            border: 1px solid black;
                            padding: 8px;
                            text-align: left;
                        }
                        th {
                            background-color: #f2f2f2;
                        }
                    </style>
                </head>
                <body>
                    <h2>List of Assignments</h2>
                    <table>
                        <tr>
                            <th>Course Name</th>
                            <th>Assignment Title</th>
                            <th>Due Date</th>
                        </tr>
        """

        for assignment in assignments_list:
            email_body += f"""
                <tr>
                    <td>{assignment['course_name']}</td>
                    <td>{assignment['title']}</td>
                    <td>{assignment['due_date']}</td>
                </tr>
            """

        email_body += """
                    </table>
                </body>
            </html>
        """

        # Send the email if there are new assignments
        if assignments_list:
            email_subject = "Your Task Overview"
            self.send_email(recipient_email, email_subject, email_body, html=True)

        self.save_seen_assignments()

def main():
    notification_system = NotificationSystem()
    notification_system.check_for_new_assignments()

if __name__ == "__main__":
    main()
