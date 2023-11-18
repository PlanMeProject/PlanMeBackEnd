from django.contrib.auth import get_user_model

from planmebackend.app.models import DeletedTask, Task

from .google_classroom_service import GoogleClassroomAPI


class AssignmentsService:
    @staticmethod
    def get_user(user_id):
        User = get_user_model()
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise Exception("User not found")

    def process_courses(self, courses, access_token, check_status, user):
        new_tasks = []
        for course in courses:
            course_id = course.get("title", {}).get("id", "")
            course_name = course.get("title", {}).get("name", "")
            assignments = GoogleClassroomAPI.get_course_work(access_token, course_id)
            new_tasks.extend(
                self.process_assignments(assignments, course_id, course_name, access_token, check_status, user)
            )
        return new_tasks

    def process_assignments(self, assignments, course_id, course_name, access_token, check_status, user):
        tasks = []
        for assignment in assignments:
            if Task.objects.filter(title=assignment.get("title", ""), user=user).exists():
                continue

            if DeletedTask.objects.filter(title=assignment.get("title", ""), user=user).exists():
                continue

            if check_status and GoogleClassroomAPI.should_skip_assignment(access_token, course_id, assignment):
                continue

            due_date = GoogleClassroomAPI.parse_due_date(assignment.get("dueDate", {}))
            tasks.append(self.create_task_from_assignment(assignment, due_date, user, course_name))
        return tasks

    @staticmethod
    def create_task_from_assignment(assignment, due_date, user, course_name):
        return Task(
            title=assignment.get("title", ""),
            description=assignment.get("description", ""),
            summarized_text=assignment.get("description", ""),
            due_date=due_date,
            status="Todo",
            course=course_name,
            user=user,
        )
