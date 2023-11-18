import logging

from rest_framework import status

from planmebackend.utils.setup_test import BaseTestCase


class DeletedTaskTestCase(BaseTestCase):
    """This class defines the test suite for the DeletedTask model."""

    def test_get_all_deleted_tasks(self):
        """Test the API for getting all deleted tasks."""
        response = self.client.get(f"{self.deleted_task_url}?user_id={self.user.id}")
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_create_deleted_task(self):
        """Test the API for creating a deleted task."""
        data = {
            "data": {
                "type": "DeletedTaskViewSet",
                "attributes": {"title": "Deleted Task", "course": "Test Course", "user": self.user.id},
            }
        }
        response = self.client.post(self.deleted_task_url, data, format="vnd.api+json")
        if response.status_code != status.HTTP_201_CREATED:
            logging.error("Create Task Error:  %s", response.data)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

    def test_delete_deleted_task(self):
        """Test the API for deleting a deleted task."""
        response = self.client.delete(f"{self.deleted_task_url}{self.deleted_task.id}/")
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
