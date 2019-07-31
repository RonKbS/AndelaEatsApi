import factory
from app.utils import db
from app.models.user import User
from factories.user_role_factory import UserRoleFactory


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):

    class Meta:
        model = User
        sqlalchemy_session = db.session

    slack_id = factory.Sequence(lambda n: n)
    first_name = factory.Faker('name')
    last_name = factory.Faker('name')
    user_id = factory.Faker('word')
    user_type = factory.SubFactory(UserRoleFactory)
    image_url = factory.Faker('url')
