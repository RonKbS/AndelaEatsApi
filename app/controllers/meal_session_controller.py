from flask import make_response, jsonify
from datetime import datetime, time
from app.controllers.base_controller import BaseController
from app.repositories.meal_session_repo import MealSessionRepo, MealSession
from app.utils.auth import Auth


class MealSessionController(BaseController):

    def __init__(self, request):
        BaseController.__init__(self, request)
        self.meal_session_repo = MealSessionRepo()

    def create_session(self):

        location_id = Auth.get_location()
        name, start_time, end_time, date = self.request_params('name', 'start_time', 'end_time', 'date')

        start_time_split = start_time.split(":")
        end_time_split = end_time.split(":")
        date_split = date.split("-")

        start_time = time(hour=int(start_time_split[0]), minute=int(start_time_split[1]))
        end_time = time(hour=int(end_time_split[0]), minute=int(end_time_split[1]))

        if self.meal_session_repo.check_two_values_are_greater(
            start_time,
            end_time,
        ):
            return make_response(
                jsonify({'msg': 'start time cannot  be after end time'}
                        ), 400)

        date_sent = datetime(year=int(date_split[0]), month=int(date_split[1]), day=int(date_split[2]))
        current_date = datetime.now()

        if self.meal_session_repo.check_two_values_are_greater(
            datetime(year=current_date.year, month=current_date.month,day=current_date.day),
            date_sent
        ):
            return make_response(
                jsonify({'msg': 'date provided cannot be one before the current date'}
                        ), 400)

        if self.meal_session_repo.filter_by(name=name, start_time=start_time, stop_time=end_time,
                                            date=date, location_id=location_id).items:
            return make_response(
                jsonify({'msg': 'This exact meal session already exists'}
                        ), 400)

        if self.meal_session_repo.check_meal_session_exists_in_specified_time(
            **{
                "name": name,
                "date_sent": date_sent,
                "location_id": location_id,
                "start_time": start_time,
                "end_time": end_time,
            }
        ):
            return make_response(
                jsonify({'msg': 'This exact meal session already exists between the specified start and stop times'}
                        ), 400)

        if self.meal_session_repo.check_encloses_already_existing_meal_sessions(
            **{
                "name": name,
                "date_sent": date_sent,
                "location_id": location_id,
                "start_time": start_time,
                "end_time": end_time,
            }
        ):
            return make_response(
                jsonify({'msg': '{} meal session(s) already exist between the specified start and stop times'.format(
                    name
                )}
                        ), 400)

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

