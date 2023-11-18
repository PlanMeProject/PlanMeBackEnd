"""The module for setting up the test suite."""
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase

from planmebackend.app.models import DeletedTask, SubTask, Task, User


class BaseTestCase(APITestCase):
    """This class defines the test suite for the user model."""

    def setUp(self):
        """Define the test client and other test variables."""
        self.user = User.objects.create_user(username="testuser", token="testtoken")
        self.task = Task.objects.create(
            title="Test Task",
            description="This is a test description",
            summarized_text="Summarized text",
            due_date="2022-12-31",
            status="Pending",
            user=self.user,
        )
        self.deleted_task = DeletedTask.objects.create(
            title="Test Task",
            user=self.user,
        )
        self.subtask = SubTask.objects.create(title="Test SubTask", status="Pending", task=self.task)
        self.user_url = "/api/users/"
        self.task_url = f"/api/users/{self.user.id}/tasks/"
        self.deleted_task_url = f"/api/users/{self.user.id}/deleted-tasks/"
        self.subtask_url = f"/api/users/{self.user.id}/tasks/{self.task.id}/subtasks/"
        self.tts_url = "/api/tts/"
        self.summarize_url = "/api/summarize/"
        self.token, created = Token.objects.get_or_create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
