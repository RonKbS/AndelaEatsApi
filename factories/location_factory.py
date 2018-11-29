'''A module of location factory'''
import factory
from app.utils import db
from app.models import Location

class LocationFactory(factory.alchemy.SQLAlchemyModelFactory):

	class Meta:
		model = Location
		sqlalchemy_session = db.session
		# sqlalchemy_session_persistence = 'commit'

	id = factory.Sequence(lambda n: n)
	name = factory.Faker('name')
