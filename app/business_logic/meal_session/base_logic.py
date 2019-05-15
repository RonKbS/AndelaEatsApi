import pytz
from datetime import datetime, time
from app.models.location import Location


class BaseLogic(object):
    def __init__(self):
        pass

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

    @staticmethod
    def get_location_time_zone(location_id):
        """
        Get the time zone of a particular location

        :param location_id: string representing location id
        :return: timezone object
        :raises: AttributeError, pytz.exceptions.UnknownTimeZoneError
        """
        location = Location.query.filter_by(id=location_id).first()

        try:
            return pytz.timezone('Africa/' + location.name)
        except AttributeError:
            return AttributeError
        except pytz.exceptions.UnknownTimeZoneError:
            return pytz.exceptions.UnknownTimeZoneError
