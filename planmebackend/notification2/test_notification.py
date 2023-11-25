"""
This module contains unit tests for the NotificationSystem class. It tests the functionality
of loading and saving seen assignments, as well as sending email notifications. The tests use
mocking to simulate the behavior of external dependencies like file operations and SMTP servers.
"""

import unittest
from unittest.mock import patch, MagicMock
from planmebackend.notification2.notification import NotificationSystem

class TestNotificationSystem(unittest.TestCase):
    """
    Test suite for the NotificationSystem class.
    """

    def setUp(self):
        """
        Set up the test environment by mocking the classroom API and initializing
        the NotificationSystem with the mocked API.
        """
        self.mock_classroom_api = MagicMock()
        self.notification_system = NotificationSystem(self.mock_classroom_api)

    @patch('notification.open', create=True)
    def test_load_seen_assignments(self, mock_open):
        """
        Test that assignments_seen loads correctly from the file.
        """
        mock_data = '{"assignment_1": "2023-11-14"}'
        mock_open.return_value.__enter__.return_value.read.return_value = mock_data
        seen_assignments = self.notification_system.load_seen_assignments()
        self.assertEqual(seen_assignments, {"assignment_1": "2023-11-14"})

    @patch('json.dump')
    @patch('notification.open', create=True)
    def test_save_seen_assignments(self, mock_open, mock_json_dump):
        """
        Test that assignments_seen saves correctly to the file.
        """
        self.notification_system.assignments_seen = {"assignment_2": "2023-11-15"}
        self.notification_system.save_seen_assignments()
        mock_open.assert_called_with('assignments_seen.json', 'w', encoding='utf-8')
        mock_json_dump.assert_called_with({"assignment_2": "2023-11-15"},
                                          mock_open.return_value.__enter__.return_value)

    @patch('notification.smtplib.SMTP')
    def test_send_email(self, mock_smtp):
        """
        Test that the send_email method sends an email correctly.
        """
        self.notification_system.send_email('test@example.com', 'Test Subject', 'Test Body')
        mock_smtp.assert_called_with('smtp.gmail.com', 587)
        instance = mock_smtp.return_value
        instance.starttls.assert_called_once()
        instance.login.assert_called_once_with('planmeproject.app@gmail.com', 'gopc cpyi lzhi blnx')
        # Additional assertions can be added to check the message contents

if __name__ == '__main__':
    unittest.main()
