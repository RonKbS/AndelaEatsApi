import pytz
from flask import make_response, jsonify
from datetime import datetime, time

from app.controllers.base_controller import BaseController
from app.repositories.meal_session_repo import MealSessionRepo
from app.repositories.meal_service_repo import MealServiceRepo
from app.utils.auth import Auth
from app.utils.location_time import get_location_time_zone
from app.business_logic.meal_session.meal_session_logic import MealSessionLogic


class MealSessionController(BaseController):

    def __init__(self, request):
        BaseController.__init__(self, request)
        self.meal_session_repo = MealSessionRepo()
        self.meal_service_repo = MealServiceRepo()
        self.business_logic = MealSessionLogic()

    def create_session(self):
        """
        Creates a meal session if all data sent meets specified requirements

        :return: Json Response
        """

        name, start_time, end_time, date, location_id = self.request_params(
            'name', 'startTime', 'endTime', 'date', 'locationId'
        )

        error_message, data = self.business_logic.validate_meal_session_details(**{
                "name": name,
                "date": date,
                "location_id": location_id,
                "start_time": start_time,
                "end_time": end_time,
        })

        if error_message:
            return make_response(jsonify({'msg': error_message}), 400)

        new_meal_session = self.meal_session_repo.new_meal_session(
            name=data['name'], start_time=data['start_time'], stop_time=data['end_time'],
            date=data['date_sent'], location_id=data['location_id']
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

        validated_data = self.business_logic.validate_update_of_meal_session(
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

        meal_session_updated.start_time = self.business_logic.get_time_as_string(
            meal_session_updated.start_time.hour,
            meal_session_updated.start_time.minute
        )

        meal_session_updated.stop_time = self.business_logic.get_time_as_string(
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

    def delete_session(self, meal_session_id):
        """
        Deletes a meal session if correct meal_session_id is sent

        :return: Json Response
        """
        meal_session = self.meal_session_repo.get(meal_session_id)

        if meal_session and not meal_session.is_deleted:
            meal_session = self.meal_session_repo.update(meal_session, **dict(is_deleted=True))
            meal_session.name = meal_session.name.value

            meal_session.start_time = self.business_logic.get_time_as_string(
                meal_session.start_time.hour,
                meal_session.start_time.minute
            )

            meal_session.stop_time = self.business_logic.get_time_as_string(
                meal_session.stop_time.hour,
                meal_session.stop_time.minute
            )

            meal_session.date = meal_session.date.strftime("%Y-%m-%d")

            return self.handle_response('Meal session deleted successfully',
                                        payload={'mealSession': meal_session.serialize()},
                                        status_code=200)

        return self.handle_response('Meal Session Not Found', status_code=404)