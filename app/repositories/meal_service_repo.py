from app.repositories.base_repo import BaseRepo
from app.models.meal_service import MealService
from datetime import datetime


class MealServiceRepo(BaseRepo):

    def __init__(self):
        BaseRepo.__init__(self, MealService)

    @staticmethod
    def new_meal_service(user_id, session_id, date=datetime.now()):
        meal_service = MealService(user_id=user_id, session_id=session_id, date=date)
        meal_service.save()
        return meal_service

