"""The module for tests the SubTask model."""
import logging

from rest_framework import status

from planmebackend.utils.setup_test import BaseTestCase


class SubTaskTestCase(BaseTestCase):
    """This class defines the test suite for the SubTask model."""

    def test_get_all_subtasks(self):
        """Test the API for getting all subtasks."""
        response = self.client.get(self.subtask_url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_get_one_subtask(self):
        """Test the API for getting one subtask."""
        response = self.client.get(f"{self.subtask_url}{self.subtask.id}/")
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_create_subtask(self):
        """Test the API for creating a subtask."""
        data = {"data": {"type": "SubTaskViewSet", "attributes": {"title": "New SubTask", "status": "Pending"}}}
        response = self.client.post(self.subtask_url, data, format="vnd.api+json")
        if response.status_code != status.HTTP_201_CREATED:
            logging.error("Create SubTask Error:  %s", response.data)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

    def test_update_subtask(self):
        """Test the API for updating a subtask."""
        data = {
            "data": {
                "type": "SubTaskViewSet",
                "id": str(self.subtask.id),
                "attributes": {"title": "Updated SubTask", "status": "Complete"},
            }
        }
        response = self.client.put(f"{self.subtask_url}{self.subtask.id}/", data, format="vnd.api+json")
        if response.status_code != status.HTTP_200_OK:
            logging.error("Update SubTask Error:  %s", response.data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_delete_subtask(self):
        """Test the API for deleting a subtask."""
        response = self.client.delete(f"{self.subtask_url}{self.subtask.id}/")
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
