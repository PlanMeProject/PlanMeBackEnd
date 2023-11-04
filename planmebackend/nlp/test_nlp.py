from rest_framework import status

from planmebackend.utils.setupTest import BaseTestCase


class NLPTestCase(BaseTestCase):
    def test_create_nlp_subtask(self):
        data = {
            "data": {
                "type": "NLPInferenceViewSet",
                "attributes": {"text": "Read a book, Write a code, sleep enough.", "task_id": self.task.id},
            }
        }

        response = self.client.post(self.subtask_url, data)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
