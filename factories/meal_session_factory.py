import factory
from app.utils import db
from datetime import datetime, time, timedelta
from app.models.meal_session import MealSession


class MealSessionFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = MealSession
        sqlalchemy_session = db.session

    id = factory.Sequence(lambda n: n)
    name = 'breakfast'
    start_time = time(hour=8)
    stop_time =  time(hour=10, minute=30)
    date = datetime.now()
    location_id = factory.Sequence(lambda n: n)
    is_deleted = False
