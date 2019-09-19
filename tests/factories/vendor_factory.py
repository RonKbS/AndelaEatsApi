import json

import factory

from andelaeats.user.models import User
from andelaeats.vendor.models import Vendor

from .base import BaseFactory
from .user_factory import UserFactory


def user_gen(user):
    user = UserFactory()
    user.save()
    return user


class VendorFactory(BaseFactory):
    class Meta:
        model = Vendor
        exclude = ("active", "modified")

    name = factory.Faker("company")
    address = factory.Faker("address")
    telephone = factory.Faker("url")
    contact_id = factory.SelfAttribute("contact.id")
    image_url = factory.Faker("url")
    contact = factory.LazyAttribute(lambda x: user_gen(x))
