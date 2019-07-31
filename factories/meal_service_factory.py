import factory
from app.utils import db
from datetime import datetime
from app.models.meal_service import MealService
from factories.user_factory import UserFactory
from factories.meal_session_factory import MealSessionFactory


class MealServiceFactory(factory.alchemy.SQLAlchemyModelFactory):

    class Meta:
        model = MealService
        sqlalchemy_session = db.session

    user_id = factory.Sequence(lambda n: n)
    user = factory.SubFactory(UserFactory)
    session_id = factory.Sequence(lambda n: n)
    session = factory.SubFactory(MealSessionFactory)
    date = datetime.now()
