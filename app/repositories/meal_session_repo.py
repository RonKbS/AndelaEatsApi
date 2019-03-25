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
        if MealSession.query.filter(
                MealSession.name == kwargs.get('name'),
                MealSession.date == kwargs.get('date_sent'),
                MealSession.location_id == kwargs.get('location_id'),
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
