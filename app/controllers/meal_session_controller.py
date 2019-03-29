import pytz
from flask import make_response, jsonify
from datetime import datetime
from app.controllers.base_controller import BaseController
from app.repositories.meal_session_repo import MealSessionRepo
from app.repositories.meal_service_repo import MealServiceRepo
from app.utils.auth import Auth


class MealSessionController(BaseController):

    def __init__(self, request):
        BaseController.__init__(self, request)
        self.meal_session_repo = MealSessionRepo()
        self.meal_service_repo = MealServiceRepo()

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

        error_message_mapper = self.meal_session_repo.return_error_message_mapper()

        tz = self.meal_session_repo.get_location_time_zone(location_id)
        exception_message = error_message_mapper.get(tz)

        if exception_message:
            return make_response(jsonify({'msg': exception_message}), 400)

        start_time = self.meal_session_repo.return_as_object(start_time, "time")
        end_time = self.meal_session_repo.return_as_object(end_time, "time")

        date_sent = self.meal_session_repo.return_as_object(date, "date")
        current_date = datetime.now(tz)

        message = self.meal_session_repo.validate_times_and_dates_not_greater_than_each_other(
            start_time,
            end_time,
            datetime(year=current_date.year, month=current_date.month, day=current_date.day),
            date_sent
        )

        error_message = error_message_mapper.get(message)

        if error_message:
            return make_response(jsonify({'msg': error_message}), 400)

        message = self.meal_session_repo.validate_meal_session_times(
            **{
                "name": name,
                "date_sent": date_sent,
                "location_id": location_id,
                "start_time": start_time,
                "end_time": end_time,
            }
        )

        message = error_message_mapper.get(message)

        if message:
            return make_response(jsonify({'msg': message}), 400)

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

    def update_session(self, meal_session_id):
        """
        Updates a meal session if all data sent meets specified requirements

        :return: Json Response
        """
        meal_session = self.meal_session_repo.get(meal_session_id)

        if not meal_session:
            return self.handle_response("Meal session Not Found", status_code=404)

        name, start_time, end_time, date, location_id = self.request_params(
            'name', 'startTime', 'endTime', 'date', 'locationId'
        )

        if not location_id:
            location_id = Auth.get_location()

        meal_session_data = {
            "name": name,
            "start_time": start_time,
            "end_time": end_time,
            "date": date,
            "location_id": location_id,
            "meal_session_id": meal_session.id,
            "meal_session": meal_session,
        }

        validated_data = self.meal_session_repo.validate_update_of_meal_session(
            **meal_session_data
        )

        error_message = validated_data.get("error_message")

        if error_message:
            return make_response(jsonify({'msg': error_message}), 400)

        meal_session_updated = self.meal_session_repo.update_meal_session(
            meal_session,
            name=validated_data.get("name"),
            start_time=validated_data.get("start_time"),
            stop_time=validated_data.get("end_time"),
            date=validated_data.get("date"),
            location_id=validated_data.get("location_id")
        )

        meal_session_updated.name = meal_session_updated.name.value

        meal_session_updated.start_time = self.meal_session_repo.get_time_as_string(
            meal_session_updated.start_time.hour,
            meal_session_updated.start_time.minute
        )

        meal_session_updated.stop_time = self.meal_session_repo.get_time_as_string(
            meal_session_updated.stop_time.hour,
            meal_session_updated.stop_time.minute
        )

        meal_session_updated.date = meal_session_updated.date.strftime("%Y-%m-%d")

        return self.handle_response('OK', payload={'mealSession': meal_session_updated.serialize()}, status_code=200)

    def list_meal_sessions(self):
        """
        List all meal-sessions in the application, based on provided query
        """
        options = self.get_params_dict()
        options['is_deleted'] = False
        sessions = self.meal_session_repo.filter_by(**options)
        if sessions.items:
            session_list = [session.serialize() for session in sessions.items]
            return self.handle_response(
                'OK',
                payload={'MealSessions': session_list,
                         'meta': self.pagination_meta(sessions)})

        return self.handle_response('No meal sessions found', status_code=404)
