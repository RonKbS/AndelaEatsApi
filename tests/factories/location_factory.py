import factory

from andelaeats.constants.time_zones import timezone
from andelaeats.location.models import City

from .base import BaseFactory


class LocationFactory(BaseFactory):
    class Meta:
        model = City

    name = factory.Faker("city")
    timezone = factory.Iterator(timezone)
