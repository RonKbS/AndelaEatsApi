from flask import make_response, jsonify
from datetime import datetime, time
from app.repositories.base_repo import BaseRepo
from app.models.meal_session import MealSession


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

    @staticmethod
    def check_two_values_are_greater(*args):
        """
        Verifies whether arg[0] is greater than arg[1]

        :param args: tuple of length two
        :return: boolean
        """
        if (len(args) is 2) and (args[0] > args[1]):
            return True
        else:
            return False

    @staticmethod
    def check_meal_session_exists_in_specified_time(**kwargs):
        """
        Check whether a meal session is already taking place at the specified
        time. Examples of possible situations are:
        1. A start_time for lunch is specified for a lunch session that is already
           in existence.
        2. A stop_time is specified for the for a lunch session that is already
           in existence.

        :param kwargs:
               Possible keys: name, date_sent, start_time, stop_time, location_id

        :return: Boolean
        """

        meal_sessions = MealSession.query.filter(
            MealSession.name == kwargs.get('name'),
            MealSession.date == kwargs.get('date_sent'),
            MealSession.location_id == kwargs.get('location_id')
        )

        if meal_sessions.filter(
                MealSession.start_time <= kwargs.get('start_time'),
                MealSession.stop_time >= kwargs.get('start_time')).paginate(error_out=False).items \
                or \
            MealSession.query.filter(
                MealSession.name == kwargs.get('name'),
                MealSession.date == kwargs.get('date_sent'),
                MealSession.location_id == kwargs.get('location_id'),
                MealSession.start_time <= kwargs.get('end_time'),
                MealSession.stop_time >= kwargs.get('end_time')).paginate(error_out=False).items:
            return True
        else:
            return False

    @staticmethod
    def check_encloses_already_existing_meal_sessions(**kwargs):
        """
        Check whether time specified encloses already existing meal sessions
        For example: a lunch meal session may already exist between 13:00hrs and 14:00hrs
        and a user tries to create another meal session between 12:59 and 14:01hrs

        :param kwargs:
               Possible keys: name, date_sent, start_time, stop_time, location_id

        :return: Boolean
        """
        if MealSession.query.filter(
                MealSession.name == kwargs.get('name'),
                MealSession.date == kwargs.get('date_sent'),
                MealSession.location_id == kwargs.get('location_id'),
                MealSession.start_time >= kwargs.get('start_time'),
                MealSession.stop_time <= kwargs.get('end_time')).paginate(error_out=False).items:
            return True
        else:
            return False

    @staticmethod
    def format_preceding(hour_or_minute):
        """
        Transform an integer such as 2 to a str '02'

        :param hour_or_minute: int
        :return: formatted string: string
        """
        return '{:02d}'.format(hour_or_minute)

    @classmethod
    def get_time_as_string(cls, hour, minute):
        """
        Transform times provided to a string of the form 08:00

        :param hour: int
        :param minute: int
        :return: string
        """
        return "".join([cls.format_preceding(hour), ":", cls.format_preceding(minute)])

    @staticmethod
    def return_as_object(type_as_string, type_sent):
        """
        Transform a time/date sent as a string into a native python time/datetime object

        :param1 type_as_string: string
        :param2 type_sent: string that represents that may be date or time
        :return: time or datetime object
        """

        splitter_mapper = {
            "time": ":",
            "date": "-"
        }

        splitter = splitter_mapper.get(type_sent)

        if splitter is not None:
            type_split = type_as_string.split(splitter)

        if type_sent is "time" and type_split:
            return time(hour=int(type_split[0]), minute=int(type_split[1]))

        if type_sent is "date" and type_split:
            return datetime(year=int(type_split[0]), month=int(type_split[1]), day=int(type_split[2]))
