import pytest

from andelaeats.constants.errors import jwt_errors
from andelaeats.user.models import User

from ...factories import UserFactory

api_version = "api/v1"


@pytest.mark.usefixtures("db")
class TestUserEndpoints:
    """User tests."""

    def test_get_all_users(self, client):
        response = client.get(f"{api_version}/users/")
        assert response.status_code == 200
