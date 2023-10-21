from rest_framework import status

from planmebackend.app.models import SubTask, Task
from planmebackend.app.tests.setup import BaseTestCase


class SubTaskTestCase(BaseTestCase):
    """This class defines the test suite for the SubTask model."""

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
        self.subtask = SubTask.objects.create(title="Test SubTask", status="Pending", task=self.task)
        self.task_url = f"/api/tasks/{self.task.id}/subtasks/"

    def test_get_all_subtasks(self):
        response = self.client.get(self.task_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_one_subtask(self):
        response = self.client.get(f"{self.task_url}{self.subtask.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_subtask(self):
        data = {
            "data": {
                "type": "SubTaskViewSet",
                "attributes": {"title": "New SubTask", "status": "Pending", "task": self.task.id},
            }
        }
        response = self.client.post(self.task_url, data, format="vnd.api+json")
        if response.status_code != status.HTTP_201_CREATED:
            print("Create SubTask Error: ", response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_subtask(self):
        data = {
            "data": {
                "type": "SubTaskViewSet",
                "id": str(self.subtask.id),
                "attributes": {"title": "Updated SubTask", "status": "Complete", "task": self.task.id},
            }
        }
        response = self.client.put(f"{self.task_url}{self.subtask.id}/", data, format="vnd.api+json")
        if response.status_code != status.HTTP_200_OK:
            print("Update SubTask Error: ", response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_subtask(self):
        response = self.client.delete(f"{self.task_url}{self.subtask.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
