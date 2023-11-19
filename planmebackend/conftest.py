"""The module defines the conftest class."""
import pytest
from django.contrib.auth import get_user_model


@pytest.fixture(autouse=True)
def media_storage(settings, tmpdir):
    """Set MEDIA_ROOT and clear it after the test runs."""
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture
def user(db):
    """Create a user for testing."""
    User = get_user_model()
    user = User.objects.create_user(
        username="testuser", password="testpass", email="test@example.com"
    )
    return user
