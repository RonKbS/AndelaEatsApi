import pytz
from datetime import date

from app.repositories.base_repo import BaseRepo
from app.models.meal_session import MealSession
from app.utils.location_time import get_location_time_zone


class MealSessionRepo(BaseRepo):

    def __init__(self):
        BaseRepo.__init__(self, MealSession)

    @staticmethod
    def new_meal_session(**kwargs):
        """
        :parameter
            kwargs: key-values pairs and the following are the required keys:
                    {name, start_time, stop_time, date, location_id}

        """

        meal_session = MealSession(**kwargs)
        meal_session.save()

        return meal_session

    def update_meal_session(self, meals_session_instance, **kwargs):
        """
        :parameter
            kwargs: key-values pairs and the following are the required keys:
                    {name, start_time, stop_time, date, location_id}

        """
        return self.update(meals_session_instance, **kwargs)

    @classmethod
    def get_by_date_location(cls, meal_date: date, location_id: int):
        return MealSession.query.filter(
            MealSession.date == meal_date and
            MealSession.location_id == location_id).all()
