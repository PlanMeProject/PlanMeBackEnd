from rest_framework import status

from planmebackend.app.tests.setup import BaseTestCase


class UserTestCase(BaseTestCase):
    """This class defines the test suite for the user model."""

    def test_get_all_users(self):
        """Test the API can list all users."""
        response = self.client.get("/api/users/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_one_user(self):
        """Test the API can retrieve a single user."""
        response = self.client.get(f"/api/users/{self.user.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_user(self):
        """Test the API has user creation capability."""
        data = {
            "data": {
                "type": "UserViewSet",
                "attributes": {"username": "NewUser", "password": "NewPassword", "token": self.token.key},
            }
        }
        response = self.client.post("/api/users/", data, format="vnd.api+json")
        print("Create User Response:", response.content)  # Debugging line
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_user(self):
        """Test the API has user update capability."""
        data = {
            "data": {
                "type": "UserViewSet",
                "id": str(self.user.id),
                "attributes": {"username": "UpdatedUser", "password": "UpdatedPassword"},
            }
        }
        response = self.client.put(f"/api/users/{self.user.id}/", data, format="vnd.api+json")
        print("Update User Response:", response.content)  # Debugging line
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_user(self):
        """Test the API has user deletion capability."""
        response = self.client.delete(f"/api/users/{self.user.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
