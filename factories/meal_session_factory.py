import factory
from app.utils import db
from datetime import datetime, time
from app.models.meal_session import MealSession
from factories.location_factory import LocationFactory


class MealSessionFactory(factory.alchemy.SQLAlchemyModelFactory):

    class Meta:
        model = MealSession
        sqlalchemy_session = db.session
        force_flush = True

    name = 'breakfast'
    start_time = time(hour=8)
    stop_time = time(hour=10, minute=30)
    date = datetime.now()
    location = factory.SubFactory(LocationFactory)
    is_deleted = False
