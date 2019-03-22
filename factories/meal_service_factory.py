import factory
from app.utils import db
from datetime import datetime
from app.models.meal_service import MealService


class MealServiceFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = MealService
        sqlalchemy_session = db.session

    id = factory.Sequence(lambda n: n)
    user_id = factory.Sequence(lambda n: n)
    session_id = factory.Sequence(lambda n: n)
    date = datetime.now()
