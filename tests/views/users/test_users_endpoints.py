import json

import pytest

from andelaeats.constants.errors import jwt_errors
from andelaeats.constants.success import messages
from andelaeats.user.models import User
from andelaeats.user.schema import UserSchema

from ...factories import UserFactory
from ..generator import ViewTestsMeta

api_version = "api/v1"


@pytest.mark.usefixtures("db")
class TestUserEndpoints(metaclass=ViewTestsMeta):
    """User tests."""

    url = "user.users"
    schema = UserSchema
    factory = UserFactory
    model = User

    def test_update_user_endpoint_for_another_user_with_same_slack_id_fails(
        self, client, user
    ):
        user_two = UserFactory.build(slack_id=user.slack_id)
        response = client.put(
            f"{api_version}/users/{user.uuid}", data=UserSchema().dumps(user_two)
        )
        assert response.status_code == 400

        assert response.json["error"]["slack_id"][0] == messages["DUPLICATE_ID"].format(
            "user", "slack_id", user.slack_id
        )

    def test_update_user_endpoint_for_another_user_with_same_user_id_fails(
        self, client, user
    ):
        user_two = UserFactory.build(user_id=user.user_id)
        response = client.put(
            f"{api_version}/users/{user.uuid}", data=UserSchema().dumps(user_two)
        )
        assert response.status_code == 400
        assert response.json["error"]["user_id"][0] == messages["DUPLICATE_ID"].format(
            "user", "user_id", user.user_id
        )
