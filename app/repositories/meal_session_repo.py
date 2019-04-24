import pytz
from datetime import datetime, time

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
    def return_base_use_filter(**kwargs):
        """
        Return base filter that is common among all queries

        :param kwargs: keys are name, date_sent, location_id
        :return: filter object
        """
        return MealSession.query.filter(
            MealSession.name == kwargs.get('name'),
            MealSession.date == kwargs.get('date_sent'),
            MealSession.location_id == kwargs.get('location_id')
        )

    @staticmethod
    def check_start_time_or_end_time_between_certain_range(meal_sessions, **kwargs):
        """
        Find all meal sessions that are have a start time or end time in an existing range

        :param1 meal_sessions: filter object
        :param1 kwargs: keys are start_time, end_time
        :return:
        """
        if meal_sessions.filter(
                MealSession.start_time <= kwargs.get('start_time'),
                MealSession.stop_time >= kwargs.get('start_time')).paginate(error_out=False).items \
                or \
                meal_sessions.filter(
                MealSession.start_time <= kwargs.get('end_time'),
                MealSession.stop_time >= kwargs.get('end_time')).paginate(error_out=False).items:
            return True
        else:
            return False

    @classmethod
    def check_meal_session_exists_in_specified_time(cls, **kwargs):
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

        meal_sessions = cls.return_base_use_filter(**kwargs)

        return cls.check_start_time_or_end_time_between_certain_range(meal_sessions, **kwargs)

    @classmethod
    def check_meal_session_exists_in_other_specified_times(cls, **kwargs):
        """
            Check whether a meal session other than the one with a particular
            session_id is already taking place at the specified
            time. Examples of possible situations are:
            1. A start_time for lunch is specified for a lunch session that is already
               in existence.
            2. A stop_time is specified for the for a lunch session that is already
               in existence.

            :param kwargs:
                   Possible keys: name, date_sent, start_time, stop_time, location_id

            :return: Boolean
        """

        meal_sessions = cls.return_base_use_filter(**kwargs).filter(
            MealSession.id != kwargs.get('meal_session_id')
        )

        return cls.check_start_time_or_end_time_between_certain_range(meal_sessions, **kwargs)

    @classmethod
    def check_encloses_already_existing_meal_sessions(cls, **kwargs):
        """
        Check whether time specified encloses already existing meal sessions
        For example: a lunch meal session may already exist between 13:00hrs and 14:00hrs
        and a user tries to create another meal session between 12:59 and 14:01hrs

        :param kwargs:
               Possible keys: name, date_sent, start_time, stop_time, location_id

        :return: Boolean
        """

        if cls.return_base_use_filter(**kwargs).filter(
                MealSession.start_time >= kwargs.get('start_time'),
                MealSession.stop_time <= kwargs.get('end_time')).paginate(error_out=False).items:
            return True
        else:
            return False

    @classmethod
    def check_encloses_already_existing_in_other_meal_sessions(cls, **kwargs):
        """
        Check whether time specified encloses already existing meal sessions other than a meal session specified
        For example: a lunch meal session may already exist between 13:00hrs and 14:00hrs
        and a user tries to create another meal session between 12:59 and 14:01hrs

        :param kwargs:
               Possible keys: name, date_sent, start_time, stop_time, location_id

        :return: Boolean
        """

        if cls.return_base_use_filter(**kwargs).filter(
                MealSession.start_time <= kwargs.get('start_time'),
                MealSession.stop_time >= kwargs.get('end_time'),
                MealSession.id != kwargs.get('meal_session_id')).paginate(error_out=False).items:
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

    @classmethod
    def validate_meal_session_already_exists(cls, **kwargs):
        """
        Check whether a particular meal session already exists

        :param kwargs: dict with keys name, data_sent, location_id, start_time and end_time
        :return: boolean
        """
        if cls.return_base_use_filter(**kwargs).filter(
            MealSession.start_time == kwargs.get('start_time'),
            MealSession.stop_time == kwargs.get('end_time')).paginate(error_out=False).items:
            return True
        else:
            return False

    @classmethod
    def validate_meal_session_already_exists_other_than_specified(cls, **kwargs):
        """
        Check whether a particular meal session already exists

        :param kwargs: dict with keys name, data_sent, location_id, start_time and end_time
        :return: boolean
        """
        if cls.return_base_use_filter(**kwargs).filter(
                MealSession.start_time == kwargs.get('start_time'),
                MealSession.stop_time == kwargs.get('end_time'),
                MealSession.id != kwargs.get('meal_session_id')).paginate(error_out=False).items:
            return True
        else:
            return False

    @classmethod
    def validate_meal_session_times(cls, **kwargs):
        """
        :param kwargs: dict with keys name, data_sent, location_id, start_time and end_time
        :return: string
        """
        if cls.validate_meal_session_already_exists(**kwargs):
            return "meal_session_already_exists"

        if cls.check_meal_session_exists_in_specified_time(**kwargs):
            return "meal_session_exists_in_specified_time"

        if cls.check_encloses_already_existing_meal_sessions(**kwargs):
            return "encloses_already_existing_meal_sessions"

    @classmethod
    def validate_update_meal_session_times(cls, **kwargs):
        """
        :param kwargs: dict with keys name, data_sent, location_id, start_time and end_time, meal_session_id
        :return: string
        """

        if cls.validate_meal_session_already_exists_other_than_specified(**kwargs):
            return "meal_session_already_exists"

        if cls.check_encloses_already_existing_in_other_meal_sessions(**kwargs):
            return "encloses_already_existing_meal_sessions"

        if cls.check_meal_session_exists_in_other_specified_times(**kwargs):
            return "meal_session_exists_in_specified_time"

    @classmethod
    def validate_times_and_dates_not_greater_than_each_other(cls, start_time, end_time, current_date, date_sent):
        """
        Check whether start_time is greater than end_time or current_date is greater than date_sent

        :return: string
        """
        if cls.check_two_values_are_greater(
            start_time,
            end_time,
        ):
            return "invalid_time"

        if cls.check_two_values_are_greater(
            current_date,
            date_sent
        ):
            return "invalid_date"

    @classmethod
    def validate_meal_created_after_or_on_current_date(cls, meal_session_date, current_date_with_tz):
        """

        :param meal_session_date: date meal session run
        :param current_date_with_tz: current date aware of the time zone
        :return: boolean
        """

        if cls.check_two_values_are_greater(
            current_date_with_tz,
            meal_session_date,
        ):
            return "meal session is before current date"

    @staticmethod
    def return_error_message_mapper():
        """
        Return a dictionary with all the error messages for the meal sessions
        :return: string
        """
        return {
            AttributeError: 'The location specified does not exist',
            pytz.exceptions.UnknownTimeZoneError: 'The location specified is in an unknown time zone',
            "invalid_time": 'The start time cannot be after end time',
            "invalid_date": 'Date provided cannot be one before the current date',
            "meal_session_exists_in_specified_time":
                "This exact meal session already exists between the specified start and stop times",
            "encloses_already_existing_meal_sessions":
                "The start and stop times specified enclose one or more types of the same meal session",
            "meal_session_already_exists": "This exact meal session already exists",
            "meal session is before current date": "Cannot create a meal session before current date"
        }

    @classmethod
    def validate_update_of_meal_session(cls, **kwargs):
        """
        Validates data sent from the update meal session endpoint
        :param kwargs: dictionary keys are name, start_time, end_time, date, location_id, meal_session
        :return:
        """
        validated_data = {
            "error_message": ""
        }

        # Dictionary with the with the possible error messages
        error_message_mapper = cls.return_error_message_mapper()

        # Get time zone object for the location specified
        tz = get_location_time_zone(kwargs.get('location_id'))

        exception_message = error_message_mapper.get(tz)

        if exception_message:
            validated_data["error_message"] = exception_message
            return validated_data

        start_time = cls.return_as_object(kwargs.get("start_time"), "time")
        end_time = cls.return_as_object(kwargs.get("end_time"), "time")

        date_sent = cls.return_as_object(kwargs.get("date"), "date")
        current_date = datetime.now(tz)

        message = cls.validate_times_and_dates_not_greater_than_each_other(
            start_time,
            end_time,
            datetime(year=current_date.year, month=current_date.month, day=current_date.day),
            date_sent
        )

        error_message = error_message_mapper.get(message)

        if error_message:
            validated_data["error_message"] = error_message
            return validated_data

        tz_stored_location = get_location_time_zone(kwargs.get("meal_session").location_id)
        current_date_using_stored_tz = datetime.now(tz_stored_location)

        # check if meal session date is before current date(using the time zone information used to create it)
        message = cls.validate_meal_created_after_or_on_current_date(
            kwargs.get("meal_session").date,
            datetime(
                year=current_date_using_stored_tz.year,
                month=current_date_using_stored_tz.month,
                day=current_date_using_stored_tz.day
            )
        )

        error_message = error_message_mapper.get(message)

        if error_message:
            validated_data["error_message"] = error_message
            return validated_data

        message = cls.validate_update_meal_session_times(
            **{
                "name": kwargs.get("name"),
                "date_sent": date_sent,
                "location_id": kwargs.get("location_id"),
                "start_time": start_time,
                "end_time": end_time,
                "meal_session_id": kwargs.get("meal_session").id
            }
        )

        message = error_message_mapper.get(message)

        if message:
            validated_data["error_message"] = message
            return validated_data

        validated_data = {
            "name": kwargs.get("name"),
            "date": date_sent,
            "location_id": kwargs.get("location_id"),
            "start_time": start_time,
            "end_time": end_time,
        }

        return validated_data
