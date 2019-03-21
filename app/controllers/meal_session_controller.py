from datetime import datetime, time
from app.controllers.base_controller import BaseController
from app.repositories.meal_session_repo import MealSessionRepo
from app.utils.auth import Auth


class MealSessionController(BaseController):

    def __init__(self, request):
        BaseController.__init__(self, request)
        self.meal_session_repo = MealSessionRepo

    def create_session(self):

        location_id = Auth.get_location()
        name, start_time, end_time, date = self.request_params('name', 'startTime', 'endTime', 'date')

        start_time_split = start_time.split(":")
        end_time_split = start_time.split(":")
        date_split = date.split("-")

        start_time = time(hour=start_time_split[0], minute=start_time_split[1])
        end_time = time(hour=end_time_split[0], minute=end_time_split[1])

        date = datetime(year=date_split[0], month=date_split[1], day=date_split[2])

        new_meal_session = self.meal_session_repo.new_meal_session(
            name=name, start_time=start_time, stop_time=end_time,
            date=date, location_id=location_id
        )

        return self.handle_response('OK', payload={'mealSession': new_meal_session}, status_code=201)


