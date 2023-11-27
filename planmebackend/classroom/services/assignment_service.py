"""The module defines the AssignmentsService class."""
from django.contrib.auth import get_user_model

from planmebackend.app.models import DeletedTask, Task

from .google_classroom_service import GoogleClassroomAPI


class AssignmentsService:
    """Service for handling operations related to assignments."""

    @staticmethod
    def get_user(user_id):
        """
        Retrieve a user by their ID.

        :param user_id: ID of the user to retrieve.
        :return: User instance.
        :raises: Exception if user not found.
        """
        User = get_user_model()
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise Exception("User not found")

    def process_courses(self, courses, access_token, check_status, user):
        """
        Process courses from Google Classroom.

        :param courses: List of courses to process.
        :param access_token: Google Classroom API access token.
        :param check_status: Status to check for assignments.
        :param user: User associated with the courses.
        :return: List of new task instances.
        """
        new_tasks = []
        for course in courses:
            course_id = course.get("title", {}).get("id", "")
            course_name = course.get("title", {}).get("name", "")
            assignments = GoogleClassroomAPI.get_course_work(
                access_token, course_id
            )
            new_tasks.extend(
                self.process_assignments(
                    assignments,
                    course_id,
                    course_name,
                    access_token,
                    check_status,
                    user,
                )
            )
        return new_tasks

    def process_assignments(
        self,
        assignments,
        course_id,
        course_name,
        access_token,
        check_status,
        user,
    ):
        """
        Process assignments from Google Classroom.

        :param assignments: Assignments to process.
        :param course_id: ID of the course.
        :param course_name: Name of the course.
        :param access_token: Google Classroom API access token.
        :param check_status: Status to check for assignments.
        :param user: User associated with the assignments.
        :return: List of task instances.
        """
        """Process assignments from Google Classroom."""
        tasks = []
        for assignment in assignments:
            if Task.objects.filter(
                title=assignment.get("title", ""), user=user
            ).exists():
                continue

            if DeletedTask.objects.filter(
                title=assignment.get("title", ""), user=user
            ).exists():
                continue

            if check_status and GoogleClassroomAPI.should_skip_assignment(
                access_token, course_id, assignment
            ):
                continue

            due_date = GoogleClassroomAPI.parse_due_date(
                assignment.get("dueDate", {})
            )
            tasks.append(
                self.create_task_from_assignment(
                    assignment, due_date, user, course_name
                )
            )
        return tasks

    @staticmethod
    def create_task_from_assignment(assignment, due_date, user, course_name):
        """
        Create a Task instance from an assignment.

        :param assignment: Assignment data.
        :param due_date: Due date of the assignment.
        :param user: User associated with the assignment.
        :param course_name: Name of the course.
        :return: Task instance.
        """
        return Task(
            title=assignment.get("title", ""),
            description=assignment.get(
                "description",
                "You should fill in the description to use the AI.",
            ),
            summarized_text=assignment.get("description", ""),
            due_date=due_date,
            status="Todo",
            course=course_name,
            user=user,
        )
