from rest_framework import status

from planmebackend.utils.setupTest import BaseTestCase


class TaskTestCase(BaseTestCase):
    """This class defines the test suite for the user model."""

    def setUp(self):
        """Define the test client and other test variables."""
        super().setUp()

    def test_get_all_tasks(self):
        """Test the API for getting all tasks."""
        response = self.client.get(self.task_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_one_task(self):
        """Test the API for getting one task."""
        response = self.client.get(f"{self.task_url}{self.task.id}/")
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
                },
            }
        }
        response = self.client.post(self.task_url, data, format="vnd.api+json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_task(self):
        """Test the API for updating a task."""
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
                },
            }
        }
        response = self.client.put(f"{self.task_url}{self.task.id}/", data, format="vnd.api+json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_task(self):
        """Test the API for deleting a task."""
        response = self.client.delete(f"{self.task_url}{self.task.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
