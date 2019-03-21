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
        end_time_split = end_time.split(":")
        date_split = date.split("-")

        start_time = time(hour=int(start_time_split[0]), minute=int(start_time_split[1]))
        end_time = time(hour=int(end_time_split[0]), minute=int(end_time_split[1]))

        date = datetime(year=int(date_split[0]), month=int(date_split[1]), day=int(date_split[2]))

        new_meal_session = self.meal_session_repo.new_meal_session(
            name=name, start_time=start_time, stop_time=end_time,
            date=date, location_id=location_id
        )

        new_meal_session.name = new_meal_session.name.value

        new_meal_session.start_time = "".join(
            [str(new_meal_session.start_time.hour), ":", str(new_meal_session.start_time.minute)])
        new_meal_session.stop_time = "".join(
            [str(new_meal_session.stop_time.hour), ":", str(new_meal_session.stop_time.minute)])

        new_meal_session.date = new_meal_session.date.strftime("%Y-%m-%d")

        return self.handle_response('OK', payload={'mealSession': new_meal_session.serialize()}, status_code=201)

