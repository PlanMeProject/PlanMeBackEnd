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


...


def task(course):
    course_data = {
        "course_id": course["id"],
        "course_name": course["name"],
        "course_section": course.get("section"),
        "course_description": course.get("description"),
        "course_status": course.get("courseState"),
    }
    return course_data


def subtask(service, course_id):
    assignments = get_works(service, course_id).get("courseWork", [])

    assignments_info = []
    for assignment in assignments:
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


def main():
    service = initialize_api()
    courses = get_courses(service)
    for course in courses:
        print("Course Information:", task(course))
        print("Assignments Information:", subtask(service, course["id"]))
        print()


if __name__ == "__main__":
    main()
