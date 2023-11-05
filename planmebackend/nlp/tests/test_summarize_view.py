"""Test cases for SummarizeViewSet."""
import logging
import uuid

from rest_framework import status

from planmebackend.utils.setupTest import BaseTestCase


class SummarizeViewSetTestCase(BaseTestCase):
    """Test cases for SummarizeViewSet."""

    def test_summarize_task(self):
        """Test if the summarize endpoint correctly updates a task's summary."""
        data = {
            "data": {
                "type": "SummarizeViewSet",
                "id": self.task.id,
                "attributes": {
                    "text": "This is a long description that needs to be summarized.",
                    "task_id": self.task.id,
                },
            }
        }

        response = self.client.put(f"{self.summarize_url}{self.task.id}/", data, format="vnd.api+json")

        if response.status_code != status.HTTP_201_CREATED:
            logging.error("Summarize Task Error: %s", response)

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.task.refresh_from_db()
        self.assertEqual(self.task.summarized_text, response.data["summarized_text"])

    def test_summarize_with_invalid_task_id(self):
        """Test summarizing with a non-existent task ID."""
        invalid_uuid = uuid.uuid4()
        data = {
            "data": {
                "type": "SummarizeViewSet",
                "id": invalid_uuid,
                "attributes": {
                    "text": "This text won't be summarized because the task does not exist.",
                    "task_id": invalid_uuid,
                },
            }
        }

        response = self.client.put(f"{self.summarize_url}{self.task.id}/", data, format="vnd.api+json")
        if response.status_code != status.HTTP_404_NOT_FOUND:
            logging.error("Summarize Task Error: %s", response)

        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_summarize_with_empty_text(self):
        """Test summarizing with empty text."""
        data = {
            "data": {
                "type": "SummarizeViewSet",
                "id": self.task.id,
                "attributes": {"text": "", "task_id": self.task.id},
            }
        }
        response = self.client.put(f"{self.summarize_url}{self.task.id}/", data, format="vnd.api+json")
        if response.status_code != status.HTTP_400_BAD_REQUEST:
            logging.error("Summarize Task Error: %s", response)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertIn("No text provided", response.data["data"])
