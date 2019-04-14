"""Module for integration tests for Meal session endpoints"""

from datetime import datetime, time, timedelta
from tests.base_test_case import BaseTestCase
from app.repositories.meal_session_repo import MealSessionRepo
from factories import MealSessionFactory, LocationFactory, RoleFactory, UserRoleFactory, PermissionFactory


class TestMealSessionEndpoints(BaseTestCase):
    """Test class for meal session endpoints"""

    def setUp(self):
        self.BaseSetUp()
        self.current_date = datetime.now()

    def test_create_non_existing_meal_session_succeeds(self):

        new_location = LocationFactory.create(id=1, name="Lagos")

        new_role = RoleFactory.create(name='admin')
        UserRoleFactory.create(user_id=self.user_id(), role_id=new_role.id)

        meal_session_data = {
            "name": "lunch",
            "startTime": "13:00",
            "endTime": "14:00",
            "date": "".join([
                MealSessionRepo.format_preceding(self.current_date.year),
                "-",
                MealSessionRepo.format_preceding(self.current_date.month),
                "-",
                MealSessionRepo.format_preceding(self.current_date.day)]),
            "locationId": new_location.id
        }

        response = self.client().post(self.make_url('/meals/session'),
                                      data=self.encode_to_json_string(meal_session_data),
                                      headers=self.headers())

        response_json = self.decode_from_json_string(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response_json['msg'], 'OK')
        self.assertEqual(response_json['payload']['mealSession']['name'], meal_session_data['name'])
        self.assertEqual(response_json['payload']['mealSession']['startTime'], meal_session_data['startTime'])
        self.assertEqual(response_json['payload']['mealSession']['stopTime'], meal_session_data['endTime'])
        self.assertEqual(response_json['payload']['mealSession']['date'], meal_session_data['date'])
        self.assertEqual(response_json['payload']['mealSession']['locationId'], meal_session_data['locationId'])

    def test_create_already_existing_meal_session_fails(self):

        new_location = LocationFactory.create(id=1000, name="Lagos")

        new_role = RoleFactory.create(name='admin')
        UserRoleFactory.create(user_id=self.user_id(), role_id=new_role.id)

        meal_session_data = {
            "name": "lunch",
            "startTime": "13:00",
            "endTime": "14:00",
            "date": "".join([
                MealSessionRepo.format_preceding(self.current_date.year),
                "-",
                MealSessionRepo.format_preceding(self.current_date.month),
                "-",
                MealSessionRepo.format_preceding(self.current_date.day)]),
            "locationId": new_location.id
        }

        # Create first meal session
        MealSessionFactory.create(
            name="lunch",
            start_time=time(hour=13, minute=0),
            stop_time=time(hour=14, minute=0),
            date=datetime(year=self.current_date.year, month=self.current_date.month, day=self.current_date.day),
            location_id=new_location.id
        )

        # Try to create second meal session
        response = self.client().post(self.make_url('/meals/session'),
                                      data=self.encode_to_json_string(meal_session_data),
                                      headers=self.headers())

        response_json = self.decode_from_json_string(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_json['msg'], 'This exact meal session already exists')

    def test_create_meal_session_using_no_existing_location_id_fails(self):

        LocationFactory.create(id=1, name="Lagos")

        new_role = RoleFactory.create(name='admin')
        UserRoleFactory.create(user_id=self.user_id(), role_id=new_role.id)

        meal_session_data = {
            "name": "lunch",
            "startTime": "13:00",
            "endTime": "14:00",
            "date": "".join([
                MealSessionRepo.format_preceding(self.current_date.year),
                "-",
                MealSessionRepo.format_preceding(self.current_date.month),
                "-",
                MealSessionRepo.format_preceding(self.current_date.day)]),
            "locationId": 100
        }

        response = self.client().post(self.make_url('/meals/session'),
                                      data=self.encode_to_json_string(meal_session_data),
                                      headers=self.headers())

        response_json = self.decode_from_json_string(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_json['msg'], 'The location specified does not exist')

    def test_create_meal_session_using_location_id_with_incorrect_timezone_name_fails(self):

        new_location = LocationFactory.create(id=1, name="Russian Republic")

        new_role = RoleFactory.create(name='admin')
        UserRoleFactory.create(user_id=self.user_id(), role_id=new_role.id)

        meal_session_data = {
            "name": "lunch",
            "startTime": "13:00",
            "endTime": "14:00",
            "date": "".join([
                MealSessionRepo.format_preceding(self.current_date.year),
                "-",
                MealSessionRepo.format_preceding(self.current_date.month),
                "-",
                MealSessionRepo.format_preceding(self.current_date.day)]),
            "locationId": new_location.id
        }

        response = self.client().post(self.make_url('/meals/session'),
                                      data=self.encode_to_json_string(meal_session_data),
                                      headers=self.headers())

        response_json = self.decode_from_json_string(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_json['msg'], 'The location specified is in an unknown time zone')

    def test_create_meal_session_with_start_time_after_end_time_fails(self):

        new_location = LocationFactory.create(id=1, name="Lagos")

        new_role = RoleFactory.create(name='admin')
        UserRoleFactory.create(user_id=self.user_id(), role_id=new_role.id)

        meal_session_data = {
            "name": "lunch",
            "startTime": "14:00",
            "endTime": "13:00",
            "date": "".join([
                MealSessionRepo.format_preceding(self.current_date.year),
                "-",
                MealSessionRepo.format_preceding(self.current_date.month),
                "-",
                MealSessionRepo.format_preceding(self.current_date.day)]),
            "locationId": new_location.id
        }

        response = self.client().post(self.make_url('/meals/session'),
                                      data=self.encode_to_json_string(meal_session_data),
                                      headers=self.headers())

    def test_create_meal_session_having_date_sent_before_present_date_fails(self):

        new_location = LocationFactory.create(id=1, name="Lagos")

        new_role = RoleFactory.create(name='admin')
        UserRoleFactory.create(user_id=self.user_id(), role_id=new_role.id)

        import pytz
        tz = pytz.timezone('Africa/Lagos')
        self.current_date = datetime.now(tz)

        meal_session_data = {
            "name": "lunch",
            "startTime": "13:00",
            "endTime": "14:00",
            "date": "".join([
                MealSessionRepo.format_preceding(self.current_date.year - 1),
                "-",
                MealSessionRepo.format_preceding(self.current_date.month),
                "-",
                MealSessionRepo.format_preceding(self.current_date.day)]),
            "locationId": new_location.id
        }

        response = self.client().post(self.make_url('/meals/session'),
                                      data=self.encode_to_json_string(meal_session_data),
                                      headers=self.headers())

        response_json = self.decode_from_json_string(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_json['msg'], 'Date provided cannot be one before the current date')

    def test_create_meal_session_with_start_time_beginning_in_an_existing_session_fails(self):

        new_location = LocationFactory.create(id=1, name="Lagos")

        new_role = RoleFactory.create(name='admin')
        UserRoleFactory.create(user_id=self.user_id(), role_id=new_role.id)

        # Create first meal session between 1:00PM and 2:00PM
        MealSessionFactory.create(
            name="lunch",
            start_time=time(hour=13, minute=0),
            stop_time=time(hour=14, minute=0),
            date=datetime(year=self.current_date.year, month=self.current_date.month, day=self.current_date.day),
            location_id=new_location.id
        )

        meal_session_data = {
            "name": "lunch",
            "startTime": "13:10",
            "endTime": "14:30",
            "date": "".join([
                MealSessionRepo.format_preceding(self.current_date.year),
                "-",
                MealSessionRepo.format_preceding(self.current_date.month),
                "-",
                MealSessionRepo.format_preceding(self.current_date.day)]),
            "locationId": new_location.id
        }

        # Create another meal session with the same name starting in between the time another with the same
        # name
        response = self.client().post(self.make_url('/meals/session'),
                                      data=self.encode_to_json_string(meal_session_data),
                                      headers=self.headers())

        response_json = self.decode_from_json_string(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response_json['msg'],
            'This exact meal session already exists between the specified start and stop times'
        )

    def test_create_meal_session_with_stop_time_ending_in_an_existing_session_fails(self):

        new_location = LocationFactory.create(id=1, name="Lagos")

        new_role = RoleFactory.create(name='admin')
        UserRoleFactory.create(user_id=self.user_id(), role_id=new_role.id)

        # Create first meal session between 1:00PM and 2:00PM
        MealSessionFactory.create(
            name="lunch",
            start_time=time(hour=13, minute=0),
            stop_time=time(hour=14, minute=0),
            date=datetime(year=self.current_date.year, month=self.current_date.month, day=self.current_date.day),
            location_id=new_location.id
        )

        meal_session_data = {
            "name": "lunch",
            "startTime": "12:10",
            "endTime": "13:30",
            "date": "".join([
                MealSessionRepo.format_preceding(self.current_date.year),
                "-",
                MealSessionRepo.format_preceding(self.current_date.month),
                "-",
                MealSessionRepo.format_preceding(self.current_date.day)]),
            "locationId": new_location.id
        }

        # Create another meal session with the same name ending in between the time another with the same
        # name
        response = self.client().post(self.make_url('/meals/session'),
                                      data=self.encode_to_json_string(meal_session_data),
                                      headers=self.headers())

        response_json = self.decode_from_json_string(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response_json['msg'],
            'This exact meal session already exists between the specified start and stop times'
        )

    def test_create_meal_session_with_start_time_and_stop_time_in_enclosing_an_existing_session_fails(self):

        new_location = LocationFactory.create(id=1, name="Lagos")

        new_role = RoleFactory.create(name='admin')
        UserRoleFactory.create(user_id=self.user_id(), role_id=new_role.id)

        # Create first meal session between 1:00PM and 2:00PM
        MealSessionFactory.create(
            name="lunch",
            start_time=time(hour=13, minute=0),
            stop_time=time(hour=14, minute=0),
            date=datetime(year=self.current_date.year, month=self.current_date.month, day=self.current_date.day),
            location_id=new_location.id
        )

        meal_session_data = {
            "name": "lunch",
            "startTime": "12:10",
            "endTime": "14:45",
            "date": "".join([
                MealSessionRepo.format_preceding(self.current_date.year),
                "-",
                MealSessionRepo.format_preceding(self.current_date.month),
                "-",
                MealSessionRepo.format_preceding(self.current_date.day)]),
            "locationId": new_location.id
        }

        response = self.client().post(self.make_url('/meals/session'),
                                      data=self.encode_to_json_string(meal_session_data),
                                      headers=self.headers())

        response_json = self.decode_from_json_string(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response_json['msg'],
            'The start and stop times specified enclose one or more types of the same meal session'
        )

    def test_create_meal_session_with_invalid_date_fails(self):

        new_location = LocationFactory.create(id=1, name="Lagos")

        new_role = RoleFactory.create(name='admin')
        UserRoleFactory.create(user_id=self.user_id(), role_id=new_role.id)

        meal_session_data = {
            "name": "lunch",
            "startTime": "12:10",
            "endTime": "14:45",
            "date": "knknslkfgm;;;.fsg;",
            "locationId": new_location.id
        }

        response = self.client().post(self.make_url('/meals/session'),
                                      data=self.encode_to_json_string(meal_session_data),
                                      headers=self.headers())

        response_json = self.decode_from_json_string(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response_json['msg'],
            'Bad Request - date should be valid date. Format: YYYY-MM-DD'
        )

    def test_create_meal_session_with_invalid_name_fails(self):

        new_location = LocationFactory.create(id=1, name="Lagos")

        new_role = RoleFactory.create(name='admin')
        UserRoleFactory.create(user_id=self.user_id(), role_id=new_role.id)

        meal_session_data = {
            "name": "some invalid name",
            "startTime": "12:10",
            "endTime": "14:45",
            "date": "".join([
                MealSessionRepo.format_preceding(self.current_date.year),
                "-",
                MealSessionRepo.format_preceding(self.current_date.month),
                "-",
                MealSessionRepo.format_preceding(self.current_date.day)]),
            "locationId": new_location.id
        }

        response = self.client().post(self.make_url('/meals/session'),
                                      data=self.encode_to_json_string(meal_session_data),
                                      headers=self.headers())

        response_json = self.decode_from_json_string(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response_json['msg'],
            "Bad Request - 'some invalid name' is not a valid value for key 'name'. values must be any of the following ['breakfast', 'lunch']"
        )

    def test_create_meal_session_with_invalid_start_time_fails(self):

        new_location = LocationFactory.create(id=1, name="Lagos")

        new_role = RoleFactory.create(name='admin')
        UserRoleFactory.create(user_id=self.user_id(), role_id=new_role.id)

        meal_session_data = {
            "name": "lunch",
            "startTime": "90:10",
            "endTime": "14:45",
            "date": "".join([
                MealSessionRepo.format_preceding(self.current_date.year),
                "-",
                MealSessionRepo.format_preceding(self.current_date.month),
                "-",
                MealSessionRepo.format_preceding(self.current_date.day)]),
            "locationId": new_location.id
        }

        response = self.client().post(self.make_url('/meals/session'),
                                      data=self.encode_to_json_string(meal_session_data),
                                      headers=self.headers())

        response_json = self.decode_from_json_string(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response_json['msg'],
            "Bad Request - startTime should be valid time. Format: Hrs:Mins. Eg 17:59"
        )

    def test_create_meal_session_with_invalid_stop_time_fails(self):

        new_location = LocationFactory.create(id=1, name="Lagos")

        new_role = RoleFactory.create(name='admin')
        UserRoleFactory.create(user_id=self.user_id(), role_id=new_role.id)

        meal_session_data = {
            "name": "lunch",
            "startTime": "13:10",
            "endTime": "41:45",
            "date": "".join([
                MealSessionRepo.format_preceding(self.current_date.year),
                "-",
                MealSessionRepo.format_preceding(self.current_date.month),
                "-",
                MealSessionRepo.format_preceding(self.current_date.day)]),
            "locationId": new_location.id
        }

        response = self.client().post(self.make_url('/meals/session'),
                                      data=self.encode_to_json_string(meal_session_data),
                                      headers=self.headers())

        response_json = self.decode_from_json_string(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response_json['msg'],
            "Bad Request - endTime should be valid time. Format: Hrs:Mins. Eg 17:59"
        )

    def test_create_meal_session_with_non_integer_location_id_fails(self):

        LocationFactory.create(id=1, name="Lagos")

        new_role = RoleFactory.create(name='admin')
        UserRoleFactory.create(user_id=self.user_id(), role_id=new_role.id)

        meal_session_data = {
            "name": "lunch",
            "startTime": "13:10",
            "endTime": "14:45",
            "date": "".join([
                MealSessionRepo.format_preceding(self.current_date.year),
                "-",
                MealSessionRepo.format_preceding(self.current_date.month),
                "-",
                MealSessionRepo.format_preceding(self.current_date.day)]),
            "locationId": "non integer"
        }

        response = self.client().post(self.make_url('/meals/session'),
                                      data=self.encode_to_json_string(meal_session_data),
                                      headers=self.headers())

        response_json = self.decode_from_json_string(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response_json['msg'],
            "Bad Request - locationId must be integer"
        )

    def test_create_meal_session_falls_back_to_location_id_in_header_when_non_sent(self):

        LocationFactory.create(id=1, name="Lagos")

        new_role = RoleFactory.create(name='admin')
        UserRoleFactory.create(user_id=self.user_id(), role_id=new_role.id)

        meal_session_data = {
            "name": "lunch",
            "startTime": "13:10",
            "endTime": "14:45",
            "date": "".join([
                MealSessionRepo.format_preceding(self.current_date.year),
                "-",
                MealSessionRepo.format_preceding(self.current_date.month),
                "-",
                MealSessionRepo.format_preceding(self.current_date.day)]),
        }

        response = self.client().post(self.make_url('/meals/session'),
                                      data=self.encode_to_json_string(meal_session_data),
                                      headers=self.headers())

        response_json = self.decode_from_json_string(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response_json['msg'], 'OK')
        self.assertEqual(response_json['payload']['mealSession']['name'], meal_session_data['name'])
        self.assertEqual(response_json['payload']['mealSession']['startTime'], meal_session_data['startTime'])
        self.assertEqual(response_json['payload']['mealSession']['stopTime'], meal_session_data['endTime'])
        self.assertEqual(response_json['payload']['mealSession']['date'], meal_session_data['date'])
        self.assertEqual(response_json['payload']['mealSession']['locationId'], int(self.headers().get('X-Location')))


    def test_update_already_existing_meal_session_succeeds(self):

        new_location = LocationFactory.create(id=1, name="Lagos")

        new_role = RoleFactory.create(name='admin')
        UserRoleFactory.create(user_id=self.user_id(), role_id=new_role.id)

        meal_session_data = {
            "name": "lunch",
            "startTime": "13:00",
            "endTime": "14:00",
            "date": "".join([
                MealSessionRepo.format_preceding(self.current_date.year),
                "-",
                MealSessionRepo.format_preceding(self.current_date.month),
                "-",
                MealSessionRepo.format_preceding(self.current_date.day)]),
            "locationId": new_location.id
        }

        # Create meal session
        meal_session = MealSessionFactory.create(
            name="lunch",
            start_time=time(hour=13, minute=0),
            stop_time=time(hour=14, minute=0),
            date=datetime(year=self.current_date.year, month=self.current_date.month, day=self.current_date.day),
            location_id=new_location.id
        )

        # Update meal session with the same data
        response = self.client().put(self.make_url('/meals/session/' + str(meal_session.id)),
                                      data=self.encode_to_json_string(meal_session_data),
                                      headers=self.headers())

        response_json = self.decode_from_json_string(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json['msg'], 'OK')
        self.assertEqual(response_json['payload']['mealSession']['name'], meal_session_data['name'])
        self.assertEqual(response_json['payload']['mealSession']['startTime'], meal_session_data['startTime'])
        self.assertEqual(response_json['payload']['mealSession']['stopTime'], meal_session_data['endTime'])
        self.assertEqual(response_json['payload']['mealSession']['date'], meal_session_data['date'])
        self.assertEqual(response_json['payload']['mealSession']['locationId'], int(self.headers().get('X-Location')))

    def test_update_meal_session_using_non_existing_location_id_fails(self):
        LocationFactory.create(id=1, name="Lagos")

        new_role = RoleFactory.create(name='admin')
        UserRoleFactory.create(user_id=self.user_id(), role_id=new_role.id)

        meal_session_data = {
            "name": "lunch",
            "startTime": "13:00",
            "endTime": "14:00",
            "date": "".join([
                MealSessionRepo.format_preceding(self.current_date.year),
                "-",
                MealSessionRepo.format_preceding(self.current_date.month),
                "-",
                MealSessionRepo.format_preceding(self.current_date.day)]),
            "locationId": 100
        }

        # Create meal session
        meal_session = MealSessionFactory.create(
            name="lunch",
            start_time=time(hour=13, minute=0),
            stop_time=time(hour=14, minute=0),
            date=datetime(year=self.current_date.year, month=self.current_date.month, day=self.current_date.day),
            location_id=100
        )

        # Update meal session with non existing location ID
        response = self.client().put(self.make_url('/meals/session/' + str(meal_session.id)),
                                     data=self.encode_to_json_string(meal_session_data),
                                     headers=self.headers())

        response_json = self.decode_from_json_string(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_json['msg'], 'The location specified does not exist')

    def test_update_of_non_existing_meal_session_fails(self):
        location = LocationFactory.create(id=1, name="Lagos")

        new_role = RoleFactory.create(name='admin')
        UserRoleFactory.create(user_id=self.user_id(), role_id=new_role.id)

        meal_session_data = {
            "name": "lunch",
            "startTime": "13:00",
            "endTime": "14:00",
            "date": "".join([
                MealSessionRepo.format_preceding(self.current_date.year),
                "-",
                MealSessionRepo.format_preceding(self.current_date.month),
                "-",
                MealSessionRepo.format_preceding(self.current_date.day)]),
            "locationId": location.id
        }

        # Create meal session
        meal_session = MealSessionFactory.create(
            name="lunch",
            start_time=time(hour=13, minute=0),
            stop_time=time(hour=14, minute=0),
            date=datetime(year=self.current_date.year, month=self.current_date.month, day=self.current_date.day),
            location_id=100
        )

        # Update meal session with non existing location ID
        response = self.client().put(self.make_url('/meals/session/' + str(meal_session.id + 1)),
                                     data=self.encode_to_json_string(meal_session_data),
                                     headers=self.headers())

        response_json = self.decode_from_json_string(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response_json['msg'], 'Meal session Not Found')

    def test_update_meal_session_using_location_id_with_incorrect_timezone_name_fails(self):
        new_location_authentic = LocationFactory.create(id=1, name="Lagos")
        new_location_fake = LocationFactory.create(id=2, name="Russian Republic")

        new_role = RoleFactory.create(name='admin')
        UserRoleFactory.create(user_id=self.user_id(), role_id=new_role.id)

        meal_session_data = {
            "name": "lunch",
            "startTime": "13:00",
            "endTime": "14:00",
            "date": "".join([
                MealSessionRepo.format_preceding(self.current_date.year),
                "-",
                MealSessionRepo.format_preceding(self.current_date.month),
                "-",
                MealSessionRepo.format_preceding(self.current_date.day)]),
            "locationId": new_location_fake.id
        }

        # Create meal session
        meal_session = MealSessionFactory.create(
            name="lunch",
            start_time=time(hour=13, minute=0),
            stop_time=time(hour=14, minute=0),
            date=datetime(year=self.current_date.year, month=self.current_date.month, day=self.current_date.day),
            location_id=new_location_authentic.id
        )

        # Update meal session with non existing location ID
        response = self.client().put(self.make_url('/meals/session/' + str(meal_session.id)),
                                     data=self.encode_to_json_string(meal_session_data),
                                     headers=self.headers())

        response_json = self.decode_from_json_string(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_json['msg'], 'The location specified is in an unknown time zone')

    def test_update_meal_session_with_start_time_after_end_time_fails(self):
        new_location = LocationFactory.create(id=1, name="Lagos")

        new_role = RoleFactory.create(name='admin')
        UserRoleFactory.create(user_id=self.user_id(), role_id=new_role.id)

        meal_session_data = {
            "name": "lunch",
            "startTime": "14:00",
            "endTime": "13:00",
            "date": "".join([
                MealSessionRepo.format_preceding(self.current_date.year),
                "-",
                MealSessionRepo.format_preceding(self.current_date.month),
                "-",
                MealSessionRepo.format_preceding(self.current_date.day)]),
            "locationId": new_location.id
        }

        # Create meal session
        meal_session = MealSessionFactory.create(
            name="lunch",
            start_time=time(hour=13, minute=0),
            stop_time=time(hour=14, minute=0),
            date=datetime(year=self.current_date.year, month=self.current_date.month, day=self.current_date.day),
            location_id=new_location.id
        )

        # Update meal session with non existing location ID
        response = self.client().put(self.make_url('/meals/session/' + str(meal_session.id)),
                                     data=self.encode_to_json_string(meal_session_data),
                                     headers=self.headers())
        response_json = self.decode_from_json_string(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_json['msg'], 'The start time cannot be after end time')

    def test_update_meal_session_having_date_sent_before_present_date_fails(self):
        new_location = LocationFactory.create(id=1, name="Lagos")

        new_role = RoleFactory.create(name='admin')
        UserRoleFactory.create(user_id=self.user_id(), role_id=new_role.id)

        import pytz
        tz = pytz.timezone('Africa/Lagos')
        self.current_date = datetime.now(tz)

        meal_session_data = {
            "name": "lunch",
            "startTime": "13:00",
            "endTime": "14:00",
            "date": "".join([
                MealSessionRepo.format_preceding(self.current_date.year - 1),
                "-",
                MealSessionRepo.format_preceding(self.current_date.month),
                "-",
                MealSessionRepo.format_preceding(self.current_date.day)]),
            "locationId": new_location.id
        }

        # Create meal session
        meal_session = MealSessionFactory.create(
            name="lunch",
            start_time=time(hour=13, minute=0),
            stop_time=time(hour=14, minute=0),
            date=datetime(year=self.current_date.year, month=self.current_date.month, day=self.current_date.day),
            location_id=new_location.id
        )

        # Update meal session with non existing location ID
        response = self.client().put(self.make_url('/meals/session/' + str(meal_session.id)),
                                     data=self.encode_to_json_string(meal_session_data),
                                     headers=self.headers())

        response_json = self.decode_from_json_string(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_json['msg'], 'Date provided cannot be one before the current date')

    def test_update_meal_session_with_start_time_beginning_in_an_existing_session_fails(self):
        new_location = LocationFactory.create(id=1, name="Lagos")

        new_role = RoleFactory.create(name='admin')
        UserRoleFactory.create(user_id=self.user_id(), role_id=new_role.id)

        # Create first meal session between 1:00PM and 2:00PM
        MealSessionFactory.create(
            name="lunch",
            start_time=time(hour=13, minute=0),
            stop_time=time(hour=14, minute=0),
            date=datetime(year=self.current_date.year, month=self.current_date.month, day=self.current_date.day),
            location_id=new_location.id
        )

        meal_session_data = {
            "name": "lunch",
            "startTime": "13:10",
            "endTime": "14:30",
            "date": "".join([
                MealSessionRepo.format_preceding(self.current_date.year),
                "-",
                MealSessionRepo.format_preceding(self.current_date.month),
                "-",
                MealSessionRepo.format_preceding(self.current_date.day)]),
            "locationId": new_location.id
        }

        # Create meal session in another time other than what was created
        meal_session = MealSessionFactory.create(
            name="lunch",
            start_time=time(hour=15, minute=0),
            stop_time=time(hour=16, minute=0),
            date=datetime(year=self.current_date.year, month=self.current_date.month, day=self.current_date.day),
            location_id=new_location.id
        )

        # Try to update the meal session to the time of an existing one
        response = self.client().put(self.make_url('/meals/session/' + str(meal_session.id)),
                                     data=self.encode_to_json_string(meal_session_data),
                                     headers=self.headers())

        response_json = self.decode_from_json_string(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response_json['msg'],
            'This exact meal session already exists between the specified start and stop times'
        )

    def test_update_of_meal_session_to_an_already_existing_meal_session_fails(self):
        new_location = LocationFactory.create(id=1, name="Lagos")

        new_role = RoleFactory.create(name='admin')
        UserRoleFactory.create(user_id=self.user_id(), role_id=new_role.id)

        # Create first meal session between 1:00PM and 2:00PM
        MealSessionFactory.create(
            name="lunch",
            start_time=time(hour=13, minute=0),
            stop_time=time(hour=14, minute=0),
            date=datetime(year=self.current_date.year, month=self.current_date.month, day=self.current_date.day),
            location_id=new_location.id
        )

        meal_session_data = {
            "name": "lunch",
            "startTime": "13:00",
            "endTime": "14:00",
            "date": "".join([
                MealSessionRepo.format_preceding(self.current_date.year),
                "-",
                MealSessionRepo.format_preceding(self.current_date.month),
                "-",
                MealSessionRepo.format_preceding(self.current_date.day)]),
            "locationId": new_location.id
        }

        # Create meal session in another time other than what was created
        meal_session = MealSessionFactory.create(
            name="lunch",
            start_time=time(hour=15, minute=0),
            stop_time=time(hour=16, minute=0),
            date=datetime(year=self.current_date.year, month=self.current_date.month, day=self.current_date.day),
            location_id=new_location.id
        )

        # Try to update the meal session with the exact details of an already existing one
        response = self.client().put(self.make_url('/meals/session/' + str(meal_session.id)),
                                     data=self.encode_to_json_string(meal_session_data),
                                     headers=self.headers())

        response_json = self.decode_from_json_string(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response_json['msg'],
            'This exact meal session already exists'
        )

    def test_update_meal_session_with_stop_time_ending_in_an_existing_session_fails(self):
        new_location = LocationFactory.create(id=1, name="Lagos")

        new_role = RoleFactory.create(name='admin')
        UserRoleFactory.create(user_id=self.user_id(), role_id=new_role.id)

        # Create first meal session between 1:00PM and 2:00PM
        MealSessionFactory.create(
            name="lunch",
            start_time=time(hour=13, minute=0),
            stop_time=time(hour=14, minute=0),
            date=datetime(year=self.current_date.year, month=self.current_date.month, day=self.current_date.day),
            location_id=new_location.id
        )

        meal_session_data = {
            "name": "lunch",
            "startTime": "12:10",
            "endTime": "13:30",
            "date": "".join([
                MealSessionRepo.format_preceding(self.current_date.year),
                "-",
                MealSessionRepo.format_preceding(self.current_date.month),
                "-",
                MealSessionRepo.format_preceding(self.current_date.day)]),
            "locationId": new_location.id
        }

        # Create meal session in another time other than what was created
        meal_session = MealSessionFactory.create(
            name="lunch",
            start_time=time(hour=15, minute=0),
            stop_time=time(hour=16, minute=0),
            date=datetime(year=self.current_date.year, month=self.current_date.month, day=self.current_date.day),
            location_id=new_location.id
        )

        # Try to update the meal session to the time of an existing one
        response = self.client().put(self.make_url('/meals/session/' + str(meal_session.id)),
                                     data=self.encode_to_json_string(meal_session_data),
                                     headers=self.headers())

        response_json = self.decode_from_json_string(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response_json['msg'],
            'This exact meal session already exists between the specified start and stop times'
        )

    def test_update_meal_session_with_start_time_and_stop_time_enclosing_an_existing_session_fails(self):
        new_location = LocationFactory.create(id=1, name="Lagos")

        new_role = RoleFactory.create(name='admin')
        UserRoleFactory.create(user_id=self.user_id(), role_id=new_role.id)

        # Create first meal session between 1:00PM and 2:00PM
        MealSessionFactory.create(
            name="lunch",
            start_time=time(hour=13, minute=0),
            stop_time=time(hour=14, minute=0),
            date=datetime(year=self.current_date.year, month=self.current_date.month, day=self.current_date.day),
            location_id=new_location.id
        )

        meal_session_data = {
            "name": "lunch",
            "startTime": "13:10",
            "endTime": "13:30",
            "date": "".join([
                MealSessionRepo.format_preceding(self.current_date.year),
                "-",
                MealSessionRepo.format_preceding(self.current_date.month),
                "-",
                MealSessionRepo.format_preceding(self.current_date.day)]),
            "locationId": new_location.id
        }

        # Create meal session in another time other than what was created
        meal_session = MealSessionFactory.create(
            name="lunch",
            start_time=time(hour=15, minute=0),
            stop_time=time(hour=16, minute=0),
            date=datetime(year=self.current_date.year, month=self.current_date.month, day=self.current_date.day),
            location_id=new_location.id
        )

        # Try to update the meal session to the time of an existing one
        response = self.client().put(self.make_url('/meals/session/' + str(meal_session.id)),
                                     data=self.encode_to_json_string(meal_session_data),
                                     headers=self.headers())

        response_json = self.decode_from_json_string(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response_json['msg'],
            'The start and stop times specified enclose one or more types of the same meal session'
        )

    def test_update_meal_session_with_invalid_date_fails(self):
        new_location = LocationFactory.create(id=1, name="Lagos")

        new_role = RoleFactory.create(name='admin')
        UserRoleFactory.create(user_id=self.user_id(), role_id=new_role.id)

        meal_session_data = {
            "name": "lunch",
            "startTime": "12:10",
            "endTime": "14:45",
            "date": "knknslkfgm;;;.fsg;",
            "locationId": new_location.id
        }

        meal_session = MealSessionFactory.create(
            name="lunch",
            start_time=time(hour=15, minute=0),
            stop_time=time(hour=16, minute=0),
            date=datetime(year=self.current_date.year, month=self.current_date.month, day=self.current_date.day),
            location_id=new_location.id
        )

        # Try to update the meal session to the time of an existing one
        response = self.client().put(self.make_url('/meals/session/' + str(meal_session.id)),
                                     data=self.encode_to_json_string(meal_session_data),
                                     headers=self.headers())

        response_json = self.decode_from_json_string(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response_json['msg'],
            'Bad Request - date should be valid date. Format: YYYY-MM-DD'
        )

    def test_update_of_meal_session_created_before_current_date_fails(self):
        new_location = LocationFactory.create(id=1, name="Lagos")

        new_role = RoleFactory.create(name='admin')
        UserRoleFactory.create(user_id=self.user_id(), role_id=new_role.id)

        meal_session_data = {
            "name": "lunch",
            "startTime": "12:10",
            "endTime": "14:45",
            "date": "".join([
                MealSessionRepo.format_preceding(self.current_date.year),
                "-",
                MealSessionRepo.format_preceding(self.current_date.month),
                "-",
                MealSessionRepo.format_preceding(self.current_date.day)]),
            "locationId": new_location.id
        }

        meal_session = MealSessionFactory.create(
            name="lunch",
            start_time=time(hour=15, minute=0),
            stop_time=time(hour=16, minute=0),
            date=datetime(
                year=self.current_date.year,
                month=self.current_date.month,
                day=self.current_date.day) - timedelta(days=2),
            location_id=new_location.id
        )

        # Try to update the meal session to the time of an existing one
        response = self.client().put(self.make_url('/meals/session/' + str(meal_session.id)),
                                     data=self.encode_to_json_string(meal_session_data),
                                     headers=self.headers())

        response_json = self.decode_from_json_string(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response_json['msg'],
            'Cannot create a meal session before current date'
        )

    def test_update_meal_session_with_invalid_name_fails(self):
        new_location = LocationFactory.create(id=1, name="Lagos")

        new_role = RoleFactory.create(name='admin')
        UserRoleFactory.create(user_id=self.user_id(), role_id=new_role.id)

        meal_session_data = {
            "name": "some invalid name",
            "startTime": "12:10",
            "endTime": "14:45",
            "date": "".join([
                MealSessionRepo.format_preceding(self.current_date.year),
                "-",
                MealSessionRepo.format_preceding(self.current_date.month),
                "-",
                MealSessionRepo.format_preceding(self.current_date.day)]),
            "locationId": new_location.id
        }

        meal_session = MealSessionFactory.create(
            name="lunch",
            start_time=time(hour=15, minute=0),
            stop_time=time(hour=16, minute=0),
            date=datetime(year=self.current_date.year, month=self.current_date.month, day=self.current_date.day),
            location_id=new_location.id
        )

        # Try to update the meal session to the time of an existing one
        response = self.client().put(self.make_url('/meals/session/' + str(meal_session.id)),
                                     data=self.encode_to_json_string(meal_session_data),
                                     headers=self.headers())

        response_json = self.decode_from_json_string(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response_json['msg'],
            "Bad Request - 'some invalid name' is not a valid value for key 'name'. values must be any of the following ['breakfast', 'lunch']"
        )

    def test_update_meal_session_with_invalid_start_time_fails(self):
        new_location = LocationFactory.create(id=1, name="Lagos")

        new_role = RoleFactory.create(name='admin')
        UserRoleFactory.create(user_id=self.user_id(), role_id=new_role.id)

        meal_session_data = {
            "name": "lunch",
            "startTime": "90:10",
            "endTime": "14:45",
            "date": "".join([
                MealSessionRepo.format_preceding(self.current_date.year),
                "-",
                MealSessionRepo.format_preceding(self.current_date.month),
                "-",
                MealSessionRepo.format_preceding(self.current_date.day)]),
            "locationId": new_location.id
        }

        meal_session = MealSessionFactory.create(
            name="lunch",
            start_time=time(hour=15, minute=0),
            stop_time=time(hour=16, minute=0),
            date=datetime(year=self.current_date.year, month=self.current_date.month, day=self.current_date.day),
            location_id=new_location.id
        )

        # Try to update the meal session to the time of an existing one
        response = self.client().put(self.make_url('/meals/session/' + str(meal_session.id)),
                                     data=self.encode_to_json_string(meal_session_data),
                                     headers=self.headers())

        response_json = self.decode_from_json_string(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response_json['msg'],
            "Bad Request - startTime should be valid time. Format: Hrs:Mins. Eg 17:59"
        )

    def test_update_meal_session_with_invalid_stop_time_fails(self):
        new_location = LocationFactory.create(id=1, name="Lagos")

        new_role = RoleFactory.create(name='admin')
        UserRoleFactory.create(user_id=self.user_id(), role_id=new_role.id)

        meal_session_data = {
            "name": "lunch",
            "startTime": "13:10",
            "endTime": "41:45",
            "date": "".join([
                MealSessionRepo.format_preceding(self.current_date.year),
                "-",
                MealSessionRepo.format_preceding(self.current_date.month),
                "-",
                MealSessionRepo.format_preceding(self.current_date.day)]),
            "locationId": new_location.id
        }

        meal_session = MealSessionFactory.create(
            name="lunch",
            start_time=time(hour=15, minute=0),
            stop_time=time(hour=16, minute=0),
            date=datetime(year=self.current_date.year, month=self.current_date.month, day=self.current_date.day),
            location_id=new_location.id
        )

        # Try to update the meal session to the time of an existing one
        response = self.client().put(self.make_url('/meals/session/' + str(meal_session.id)),
                                     data=self.encode_to_json_string(meal_session_data),
                                     headers=self.headers())

        response_json = self.decode_from_json_string(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response_json['msg'],
            "Bad Request - endTime should be valid time. Format: Hrs:Mins. Eg 17:59"
        )

    def test_update_meal_session_with_non_integer_location_id_fails(self):
        new_location = LocationFactory.create(id=1, name="Lagos")

        new_role = RoleFactory.create(name='admin')
        UserRoleFactory.create(user_id=self.user_id(), role_id=new_role.id)

        meal_session_data = {
            "name": "lunch",
            "startTime": "13:10",
            "endTime": "14:45",
            "date": "".join([
                MealSessionRepo.format_preceding(self.current_date.year),
                "-",
                MealSessionRepo.format_preceding(self.current_date.month),
                "-",
                MealSessionRepo.format_preceding(self.current_date.day)]),
            "locationId": "non integer"
        }

        meal_session = MealSessionFactory.create(
            name="lunch",
            start_time=time(hour=15, minute=0),
            stop_time=time(hour=16, minute=0),
            date=datetime(year=self.current_date.year, month=self.current_date.month, day=self.current_date.day),
            location_id=new_location.id
        )

        # Try to update the meal session to the time of an existing one
        response = self.client().put(self.make_url('/meals/session/' + str(meal_session.id)),
                                     data=self.encode_to_json_string(meal_session_data),
                                     headers=self.headers())

        response_json = self.decode_from_json_string(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response_json['msg'],
            "Bad Request - locationId must be integer"
        )

    def test_update_meal_session_falls_back_to_location_id_in_header_when_none_sent(self):
        new_location = LocationFactory.create(id=1, name="Lagos")

        new_role = RoleFactory.create(name='admin')
        UserRoleFactory.create(user_id=self.user_id(), role_id=new_role.id)

        meal_session_data = {
            "name": "lunch",
            "startTime": "13:10",
            "endTime": "14:45",
            "date": "".join([
                MealSessionRepo.format_preceding(self.current_date.year),
                "-",
                MealSessionRepo.format_preceding(self.current_date.month),
                "-",
                MealSessionRepo.format_preceding(self.current_date.day)]),
        }

        meal_session = MealSessionFactory.create(
            name="lunch",
            start_time=time(hour=15, minute=0),
            stop_time=time(hour=16, minute=0),
            date=datetime(year=self.current_date.year, month=self.current_date.month, day=self.current_date.day),
            location_id=new_location.id
        )

        # Try to update the meal session to the time of an existing one
        response = self.client().put(self.make_url('/meals/session/' + str(meal_session.id)),
                                     data=self.encode_to_json_string(meal_session_data),
                                     headers=self.headers())

        response_json = self.decode_from_json_string(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json['msg'], 'OK')
        self.assertEqual(response_json['payload']['mealSession']['name'], meal_session_data['name'])
        self.assertEqual(response_json['payload']['mealSession']['startTime'], meal_session_data['startTime'])
        self.assertEqual(response_json['payload']['mealSession']['stopTime'], meal_session_data['endTime'])
        self.assertEqual(response_json['payload']['mealSession']['date'], meal_session_data['date'])
        self.assertEqual(response_json['payload']['mealSession']['locationId'], int(self.headers().get('X-Location')))

    def test_list_mealsession_fails_without_right_permission(self):

        MealSessionFactory.create_batch(10)
        role1 = RoleFactory.create(name='adminn')
        user_id = BaseTestCase.user_id()
        PermissionFactory.create(keyword='view_sessions', role_id=role1.id)
        UserRoleFactory.create(user_id=user_id, role_id=role1.id)

        response = self.client().get(self.make_url('/meals/session/'), headers=self.headers())
        response_json = self.decode_from_json_string(response.data.decode('utf-8'))

        self.assert400(response)
        self.assertEqual(response_json['msg'], 'Access Error - This role does not have the access rights')

    def test_list_mealsession_with_right_permission(self):

        MealSessionFactory.create_batch(10)
        role1 = RoleFactory.create(name='admin')
        user_id = BaseTestCase.user_id()
        PermissionFactory.create(keyword='view_sessions', role_id=role1.id)
        UserRoleFactory.create(user_id=user_id, role_id=role1.id)

        response = self.client().get(self.make_url('/meals/session/'), headers=self.headers())
        response_json = self.decode_from_json_string(response.data.decode('utf-8'))

        self.assert200(response)
        self.assertEqual(response_json['msg'], 'OK')

    def test_list_mealsession_when_none_exists(self):

        role1 = RoleFactory.create(name='admin')
        user_id = BaseTestCase.user_id()
        PermissionFactory.create(keyword='view_sessions', role_id=role1.id)
        UserRoleFactory.create(user_id=user_id, role_id=role1.id)

        response = self.client().get(self.make_url('/meals/session/'), headers=self.headers())
        response_json = self.decode_from_json_string(response.data.decode('utf-8'))

        self.assert404(response)
        self.assertEqual(response_json['msg'], 'No meal sessions found')


    def test_delete_meal_session_succeds(self):

        location = LocationFactory.create(id=1, name="Lagos")

        new_role = RoleFactory.create(name='admin')
        UserRoleFactory.create(user_id=self.user_id(), role_id=new_role.id)

        meal_session = MealSessionFactory.create(id=1, location_id=location.id)

        response = self.client().delete(self.make_url('/meals/session/'+ str(meal_session.id)),
                                        headers=self.headers())

        response_json = self.decode_from_json_string(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json['msg'], 'Meal session deleted successfully')
        self.assertEqual(response_json['payload']['mealSession']['id'], meal_session.id)
        self.assertEqual(response_json['payload']['mealSession']['name'], meal_session.name)
        self.assertEqual(response_json['payload']['mealSession']['startTime'], meal_session.start_time)
        self.assertEqual(response_json['payload']['mealSession']['stopTime'], meal_session.stop_time)
        self.assertEqual(response_json['payload']['mealSession']['date'], meal_session.date)
        self.assertEqual(response_json['payload']['mealSession']['locationId'], meal_session.location_id)

    def test_delete_meal_session_for_one_already_deleted_fails(self):

        location = LocationFactory.create(id=1, name="Lagos")

        new_role = RoleFactory.create(name='admin')
        UserRoleFactory.create(user_id=self.user_id(), role_id=new_role.id)

        meal_session = MealSessionFactory.create(id=1, location_id=location.id, is_deleted=True)

        meal_session_id = str(meal_session.id)

        response = self.client().delete(self.make_url('/meals/session/' + meal_session_id),
                                        headers=self.headers())

        response_json = self.decode_from_json_string(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response_json['msg'], 'Meal Session Not Found')

    def test_delete_meal_session_for_none_existing_session_fails(self):
        location = LocationFactory.create(id=1, name="Lagos")

        new_role = RoleFactory.create(name='admin')
        UserRoleFactory.create(user_id=self.user_id(), role_id=new_role.id)

        meal_session = MealSessionFactory.create(id=1, location_id=location.id, is_deleted=True)

        meal_session_id = str(meal_session.id + 1)

        response = self.client().delete(self.make_url('/meals/session/' + meal_session_id),
                                        headers=self.headers())

        response_json = self.decode_from_json_string(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response_json['msg'], 'Meal Session Not Found')
