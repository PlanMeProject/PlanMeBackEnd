from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


class GoogleClassroomAPI:
    def __init__(self):
        self.service = self.initialize_api()

    def initialize_api(self):
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
        results = self.service.courses().list(studentId="me").execute()
        return results.get("courses", [])

    def get_students(self, course_id):
        students_results = self.service.courses().students().list(courseId=course_id).execute()
        return students_results.get("students", [])

    def get_works(self, course_id):
        coursework_results = self.service.courses().courseWork().list(courseId=course_id).execute()
        return coursework_results

    def student_information(self, students):
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

    def task(self, course):
        course_data = {
            "course_id": course["id"],
            "course_name": course["name"],
            "course_section": course.get("section"),
            "course_description": course.get("description"),
            "course_status": course.get("courseState"),
        }
        return course_data

    def subtask(self, course_id):
        assignments = self.get_works(course_id).get("courseWork", [])

        assignments_info = []
        for assignment in assignments:
            # Get student submissions for this assignment
            submissions_results = (
                self.service.courses()
                .courseWork()
                .studentSubmissions()
                .list(courseId=course_id, courseWorkId=assignment["id"], userId="me")
                .execute()
            )
            submissions = submissions_results.get("studentSubmissions", [])

            # Check if the assignment is not done
            if not any(submission.get("state") in ["TURNED_IN", "RETURNED"] for submission in submissions):
                info = {
                    "course_id": course_id,
                    "title": assignment.get("title"),
                    "description": assignment.get("description"),
                    "due_date": str(assignment.get("dueDate", {}).get("year"))
                    + "-"
                    + str(assignment.get("dueDate", {}).get("month"))
                    + "-"
                    + str(assignment.get("dueDate", {}).get("day")),
                    "status": assignment.get("state"),
                    "max_points": assignment.get("maxPoints"),
                }
                assignments_info.append(info)
        return assignments_info

    def main(self):
        courses = self.get_courses()
        for course in courses:
            print("Course Information:", self.task(course))
            print("Assignments Information:", self.subtask(course["id"]))
            print()


if __name__ == "__main__":
    api = GoogleClassroomAPI()
    api.main()
