import json

import factory

from andelaeats.user.models import User

from .base import BaseFactory


class UserFactory(BaseFactory):
    class Meta:
        """Factory configuration."""

        model = User

    slack_id = factory.Sequence(lambda n: n)
    first_name = factory.Faker("name")
    email = factory.Faker("email")
    last_name = factory.Faker("name")
    image_url = factory.Faker("url")
    user_id = factory.Sequence(lambda n: n + 1)
