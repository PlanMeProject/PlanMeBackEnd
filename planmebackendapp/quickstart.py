from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


def initialize_api():
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


def get_courses(service):
    results = service.courses().list(studentId="me").execute()
    return results.get("courses", [])


def get_students(service, course_id):
    students_results = service.courses().students().list(courseId=course_id).execute()
    return students_results.get("students", [])


def get_works(service, course_id):
    coursework_results = service.courses().courseWork().list(courseId=course_id).execute()
    return coursework_results


def student_information(students):
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


def task(course):
    pass


def subtask(course):
    pass


def main():
    service = initialize_api()
    courses = get_courses(service)
    for course in courses:
        print(course)
        print()


if __name__ == "__main__":
    main()
