'''Factory module for generating fake instances of VendorRating class'''
import factory
import factory.fuzzy
from app.utils import db
from app.models import VendorRating
from .vendor_factory import VendorFactory
from tests.base_test_case import BaseTestCase


class VendorRatingFactory(factory.alchemy.SQLAlchemyModelFactory):

	class Meta:
		model = VendorRating
		sqlalchemy_session = db.session

	vendor = factory.SubFactory(VendorFactory)
	
	id = factory.Sequence(lambda n: n)
	vendor_id = factory.SelfAttribute('vendor.id')
	user_id = BaseTestCase.user_id()
	comment = factory.Faker('sentence')
	rating = factory.fuzzy.FuzzyInteger(5)
	channel = factory.Faker('word')
