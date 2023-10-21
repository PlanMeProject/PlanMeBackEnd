from rest_framework import status

from planmebackend.app.tests.setup import BaseTestCase


class UserTestCase(BaseTestCase):
    """This class defines the test suite for the user model."""

    def test_get_all_users(self):
        """Test the api has user creation capability."""
        response = self.client.get("/api/users/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_one_user(self):
        """Test the api has user creation capability."""
        response = self.client.get(f"/api/users/{self.user.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
