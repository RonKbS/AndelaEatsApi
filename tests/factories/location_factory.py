import factory

from andelaeats.constants.zones import locations, timezone
from andelaeats.location.models import Location

from .base import BaseFactory


class LocationFactory(BaseFactory):
    class Meta:
        model = Location

    name = factory.Iterator(locations)
    timezone = factory.Iterator(timezone)
