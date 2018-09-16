import factory
from app.utils import db
from app.models.role import Role


class RoleFactory(factory.alchemy.SQLAlchemyModelFactory):

	class Meta:
		model = Role
		sqlalchemy_session = db.session
	
	id = factory.Sequence(lambda n: n)
	name = factory.Faker('word')
	help = 'A Help Message'
		
			