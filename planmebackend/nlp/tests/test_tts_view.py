"""App config for planmebackend app."""
import logging

from rest_framework import status

from planmebackend.app.models import SubTask
from planmebackend.utils.setup_test import BaseTestCase


class NLPTestCase(BaseTestCase):
    """Test cases for TTSViewSet."""

    def test_create_nlp_subtask(self):
        """
        Test if posting to NLP endpoint creates subtasks as expected.
        """
        data = {
            "data": {
                "type": "TTSViewSet",
                "attributes": {"text": "Read a book, Write a code, sleep enough.", "task_id": self.task.id},
            }
        }

        response = self.client.post(self.tts_url, data, format="vnd.api+json")
        if response.status_code != status.HTTP_201_CREATED:
            logging.error("Create SubTask Error: %s", response.data)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

    def test_create_empty_subtask(self):
        """
        Test that posting empty text to the NLP endpoint does not create any subtasks.
        """
        data = {
            "data": {
                "type": "TTSViewSet",
                "attributes": {"text": "", "task_id": self.task.id},
            }
        }

        response = self.client.post(self.tts_url, data, format="vnd.api+json")
        if response.status_code != status.HTTP_201_CREATED:
            logging.error("Create SubTask Error: %s", response.data)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

    def test_old_subtasks_are_deleted(self):
        """
        Test if old subtasks are deleted when new subtasks are created via the NLP endpoint.
        """
        old_subtask = SubTask.objects.create(task=self.task, title="Old Subtask", status="Todo")
        self.assertTrue(SubTask.objects.filter(task=self.task).exists())
        self.test_create_nlp_subtask()
        self.assertFalse(SubTask.objects.filter(pk=old_subtask.pk).exists())

    def test_old_subtasks_are_added(self):
        """
        Test if the correct number of subtasks are added after posting to the NLP endpoint.
        """
        self.assertEqual(1, SubTask.objects.all().count())
        self.test_create_nlp_subtask()
        subtasks_count = SubTask.objects.filter(task=self.task).count()
        self.assertEqual(3, subtasks_count)

    def test_no_old_subtask(self):
        """
        Test if subtasks are correctly created when there are no pre-existing subtasks.
        """
        self.assertEqual(1, SubTask.objects.all().count())
        SubTask.objects.filter(task=self.task).delete()
        self.assertEqual(0, SubTask.objects.all().count())
        self.test_create_nlp_subtask()
        subtasks_count = SubTask.objects.filter(task=self.task).count()
        self.assertEqual(3, subtasks_count)
