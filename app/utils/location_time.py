from app.models import Location
import pytz


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