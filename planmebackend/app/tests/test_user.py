"""The module for tests the User model."""
from rest_framework import status

from planmebackend.utils.setup_test import BaseTestCase


class UserTestCase(BaseTestCase):
    """This class defines the test suite for the user model."""

    def test_get_one_user(self):
        """Test the API can retrieve a single user."""
        response = self.client.get(f"{self.user_url}{self.user.id}/")
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_update_user(self):
        """Test the API has user update capability."""
        data = {
            "data": {
                "type": "UserViewSet",
                "id": str(self.user.id),
                "attributes": {
                    "username": "UpdatedUser",
                    "password": "UpdatedPassword",
                },
            }
        }
        response = self.client.put(
            f"{self.user_url}{self.user.id}/", data, format="vnd.api+json"
        )
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_delete_user(self):
        """Test the API has user deletion capability."""
        response = self.client.delete(f"{self.user_url}{self.user.id}/")
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
