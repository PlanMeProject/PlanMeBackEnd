from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase

from planmebackend.app.models import User


class BaseTestCase(APITestCase):
    """This class defines the test suite for the user model."""

    def setUp(self):
        """Define the test client and other test variables."""
        self.user = User.objects.create_user(username="testuser", token="testtoken")

        self.token, created = Token.objects.get_or_create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
