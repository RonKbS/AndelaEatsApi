import pytz
from flask import make_response, jsonify
from datetime import datetime, time

from app.controllers.base_controller import BaseController
from app.repositories.meal_session_repo import MealSessionRepo
from app.repositories.location_repo import LocationRepo
from app.utils.auth import Auth


class MealSessionController(BaseController):

    def __init__(self, request):
        BaseController.__init__(self, request)
        self.meal_session_repo = MealSessionRepo()

    def create_session(self):
        """
        Creates a meal session if all data sent meets specified requirements

        :return: Json Response
        """

        name, start_time, end_time, date, location_id = self.request_params(
            'name', 'startTime', 'endTime', 'date', 'locationId'
        )

        if not location_id:
            location_id = Auth.get_location()

        tz = self.meal_session_repo.get_location_time_zone(location_id)

        tz_exception_message_mapper = {
            AttributeError: 'The location specified does not exist',
            pytz.exceptions.UnknownTimeZoneError: 'The location specified is in an unknown time zone'
        }

        exception_message = tz_exception_message_mapper.get(tz)

        if exception_message:
            return make_response(jsonify({'msg': exception_message}), 400)

        start_time = self.meal_session_repo.return_as_object(start_time, "time")
        end_time = self.meal_session_repo.return_as_object(end_time, "time")

        if self.meal_session_repo.check_two_values_are_greater(
            start_time,
            end_time,
        ):
            return make_response(
                jsonify({'msg': 'The start time cannot be after end time'}), 400
            )

        date_sent = self.meal_session_repo.return_as_object(date, "date")
        current_date = datetime.now(tz)

        if self.meal_session_repo.check_two_values_are_greater(
            datetime(year=current_date.year, month=current_date.month,day=current_date.day),
            date_sent
        ):
            return make_response(
                jsonify({'msg': 'Date provided cannot be one before the current date'}), 400
            )

        if self.meal_session_repo.filter_by(name=name, start_time=start_time, stop_time=end_time,
                                            date=date_sent, location_id=location_id).items:
            return make_response(
                jsonify({'msg': 'This exact meal session already exists'}), 400
            )

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
            date=date_sent, location_id=location_id
        )

        new_meal_session.name = new_meal_session.name.value

        new_meal_session.start_time = self.meal_session_repo.get_time_as_string(
            new_meal_session.start_time.hour,
            new_meal_session.start_time.minute
        )

        new_meal_session.stop_time = self.meal_session_repo.get_time_as_string(
            new_meal_session.stop_time.hour,
            new_meal_session.stop_time.minute
        )

        new_meal_session.date = new_meal_session.date.strftime("%Y-%m-%d")

        return self.handle_response('OK', payload={'mealSession': new_meal_session.serialize()}, status_code=201)

