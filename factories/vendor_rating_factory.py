'''Factory module for generating fake instances of VendorRating class'''
import factory
import factory.fuzzy
from app.utils import db
from app.models import VendorRating
from .vendor_factory import VendorFactory
from .vendor_engagement_factory import VendorEngagementFactory
from tests.base_test_case import BaseTestCase


class VendorRatingFactory(factory.alchemy.SQLAlchemyModelFactory):

    class Meta:
        model = VendorRating
        sqlalchemy_session = db.session

    vendor = factory.SubFactory(VendorFactory)
    engagement = factory.SubFactory(VendorEngagementFactory)

    id = factory.Sequence(lambda n: n)
    vendor_id = factory.SelfAttribute('vendor.id')
    engagement_id = factory.SelfAttribute('engagement.id')
    user_id = BaseTestCase.user_id()
    service_date = factory.Faker('date_time')
    rating_type = 'order'
    comment = factory.Faker('sentence')
    rating = 4
    channel = factory.Faker('word')
