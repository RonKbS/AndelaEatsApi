import factory
from app.utils import db
from app.models.user import User


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session = db.session

    id = factory.Sequence(lambda n: n)
    slack_id = factory.Sequence(lambda n: n)
    first_name = factory.Faker('name')
    last_name = factory.Faker('name')
    email = factory.Faker('email')
    user_role_id = factory.Sequence(lambda n: n)
    image_url = factory.Faker('url')

