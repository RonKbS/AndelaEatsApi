import factory
from app.utils import db
from app.models.permission import Permission
from factories.role_factory import RoleFactory


class PermissionFactory(factory.alchemy.SQLAlchemyModelFactory):

    class Meta:
        model = Permission
        sqlalchemy_session = db.session

    name = factory.Faker('name')
    role = factory.SubFactory(RoleFactory)
    keyword = factory.Faker('word')
