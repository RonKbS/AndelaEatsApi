import factory
from app.utils import db
from app.models.user_role import UserRole
from factories.role_factory import RoleFactory
from factories.location_factory import LocationFactory
from tests.base_test_case import fake


class UserRoleFactory(factory.alchemy.SQLAlchemyModelFactory):

	class Meta:
		model = UserRole
		sqlalchemy_session = db.session

	location = factory.SubFactory(LocationFactory)
	id = factory.Sequence(lambda n: n)
	role_id = factory.SubFactory(RoleFactory)
	user_id = factory.Sequence(lambda n: n)
	location_id = factory.SelfAttribute('location.id')
	email = fake.email()
