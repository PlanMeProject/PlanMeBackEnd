"""The module for tests the Task model."""
import logging

from rest_framework import status

from planmebackend.app.models import DeletedTask, Task
from planmebackend.utils.setup_test import BaseTestCase


class TaskTestCase(BaseTestCase):
    """This class defines the test suite for the user model."""

    def test_get_all_tasks(self):
        """Test the API for getting all tasks."""
        response = self.client.get(f"{self.task_url}?user_id={self.user.id}")
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_get_one_task(self):
        """Test the API for getting one task."""
        response = self.client.get(f"{self.task_url}{self.task.id}/")
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_create_task(self):
        """Test the API for creating a task."""
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
        if response.status_code != status.HTTP_201_CREATED:
            logging.error("Create Task Error:  %s", response.data)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

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
        if response.status_code != status.HTTP_200_OK:
            logging.error("Update Task Error:  %s", response.data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_delete_task(self):
        """Test the API for deleting a task and creating a deleted task record."""
        response = self.client.delete(f"{self.task_url}{self.task.id}/")
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

        with self.assertRaises(Task.DoesNotExist):
            Task.objects.get(id=self.task.id)

        deleted_task_exists = DeletedTask.objects.filter(
            title=self.task.title, course=self.task.course, user=self.task.user
        ).exists()
        self.assertTrue(deleted_task_exists)
