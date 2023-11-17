import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
from notification import NotificationSystem

class TestNotificationSystem(unittest.TestCase):

    def setUp(self):
        # Mocking the classroom API
        self.mock_classroom_api = MagicMock()
        # Initialize the NotificationSystem with the mocked API
        self.notification_system = NotificationSystem(self.mock_classroom_api)

    @patch('notification.open', create=True)
    def test_load_seen_assignments(self, mock_open):
        # Test that assignments_seen loads correctly
        mock_open.return_value.__enter__.return_value.read.return_value = '{"assignment_1": "2023-11-14"}'
        seen_assignments = self.notification_system.load_seen_assignments()
        self.assertEqual(seen_assignments, {"assignment_1": "2023-11-14"})

    @patch('json.dump')
    @patch('notification.open', create=True)
    def test_save_seen_assignments(self, mock_open, mock_json_dump):
        # Test that assignments_seen saves correctly
        self.notification_system.assignments_seen = {"assignment_2": "2023-11-15"}
        self.notification_system.save_seen_assignments()
        mock_open.assert_called_with('assignments_seen.json', 'w', encoding='utf-8')
        mock_json_dump.assert_called_with({"assignment_2": "2023-11-15"}, mock_open.return_value.__enter__.return_value)

    @patch('notification.smtplib.SMTP')
    def test_send_email(self, mock_smtp):
        # Test that send_email sends an email correctly
        self.notification_system.send_email('test@example.com', 'Test Subject', 'Test Body')
        mock_smtp.assert_called_with('smtp.gmail.com', 587)
        instance = mock_smtp.return_value
        instance.starttls.assert_called_once()
        instance.login.assert_called_once_with('planmeproject.app@gmail.com', 'gopc cpyi lzhi blnx')
        # Further assertions can be made to check the message contents

if __name__ == '__main__':
    unittest.main()
