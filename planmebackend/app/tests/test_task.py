from rest_framework import status

from planmebackend.app.models import Task
from planmebackend.app.tests.setup import BaseTestCase


class TaskTestCase(BaseTestCase):
    """This class defines the test suite for the user model."""

    def setUp(self):
        """Define the test client and other test variables."""
        super().setUp()
        self.task = Task.objects.create(
            title="Test Task",
            description="This is a test description",
            summarized_text="Summarized text",
            due_date="2022-12-31",
            status="Pending",
            user=self.user,
        )

    def test_get_all_tasks(self):
        """Test the api has user creation capability."""
        response = self.client.get("/api/tasks/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_one_task(self):
        """Test the api has user creation capability."""
        response = self.client.get(f"/api/tasks/{self.task.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_task(self):
        data = {
            "data": {
                "type": "TaskViewSet",
                "attributes": {
                    "title": "New Task",
                    "description": "New description",
                    "summarized_text": "New summarized text",
                    "due_date": "2022-12-31",
                    "status": "Pending",
                    "user": self.user.id,
                },
            }
        }
        response = self.client.post("/api/tasks/", data, format="vnd.api+json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_task(self):
        """Test the api has task update capability."""
        data = {
            "data": {
                "type": "TaskViewSet",
                "id": str(self.task.id),
                "attributes": {
                    "title": "Update Task",
                    "description": "Update description",
                    "summarized_text": "Update summarized text",
                    "due_date": "2022-12-31",
                    "status": "Complete",
                    "user": self.user.id,
                },
            }
        }
        response = self.client.put(f"/api/tasks/{self.task.id}/", data, format="vnd.api+json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_task(self):
        """Test the api has user creation capability."""
        response = self.client.delete(f"/api/tasks/{self.task.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)