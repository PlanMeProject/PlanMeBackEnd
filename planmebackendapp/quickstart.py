# from google_auth_oauthlib.flow import InstalledAppFlow
# from googleapiclient.discovery import build

# # Initialize the API
# scopes = [
#     'https://www.googleapis.com/auth/classroom.courses.readonly',
#     'https://www.googleapis.com/auth/classroom.rosters.readonly',
#     'https://www.googleapis.com/auth/classroom.course-work.readonly',
#     'https://www.googleapis.com/auth/classroom.student-submissions.me.readonly',
# ]

# flow = InstalledAppFlow.from_client_secrets_file('credentials.json', scopes)
# credentials = flow.run_local_server(port=0)
# service = build('classroom', 'v1', credentials=credentials)

# # Get the list of courses where you are a student
# results = service.courses().list(studentId='me').execute()
# courses = results.get('courses', [])

# # Get the list of students in the course
# students_results = service.courses().students().list(courseId=course['id']).execute()
# students = students_results.get('students', [])

# def student_information(students):

#     user = {
#         'course_id': students[0]['courseId'],
#         'user_id': students[0]['userId'],
#         'name': students[0]['profile']['name']['givenName'],
#         'family_name': students[0]['profile']['name']['familyName'],
#         'full_name': students[0]['profile']['name']['fullName'],
#     }

#     return user

# print(student_information(students))
# # Loop through each course
# # for course in courses:
# #     print("Course Name:", course['name'])
# #     # Get the list of students in the course
# #     print(student_information(course))
#     # print()

#     # Loop through each student
#     # for student in students:
#     #     # print("Student Name:", student['profile']['name']['fullName'])
#     #     print(student['profile']['name'])
#     # print()
#     # Get the list of assignments (course work) in the course
#     # coursework_results = service.courses().courseWork().list(courseId=course['id']).execute()
#     # course_works = coursework_results.get('courseWork', [])

#     # Loop through each assignment
#     # for work in course_works:
#     #     # Get student submissions for this assignment
#     #     submissions_results = service.courses().courseWork().studentSubmissions().list(
#     #         courseId=course['id'], courseWorkId=work['id'], userId='me').execute()
#     #     submissions = submissions_results.get('studentSubmissions', [])

#     #     # Check if the assignment is not done
#     #     if not any(submission.get('state') in ['TURNED_IN', 'RETURNED'] for submission in submissions):
#     #         print("Assignment Title:", work['title'])
#     #         print("Assignment Description:", work.get('description', 'No description'))
#     #         print("Due Date:", work.get('dueDate', 'No due date'))

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


def main():
    service = initialize_api()
    courses = get_courses(service)
    for course in courses:
        print(course)
        print()

    # for course in courses:
    #     print("Course Name:", course['name'])
    #     students = get_students(service, course['id'])
    #     print(student_information(students))
    #     print()


if __name__ == "__main__":
    main()
