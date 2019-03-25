"""Module for integration tests for Meal session endpoints"""

from datetime import datetime, time
from tests.base_test_case import BaseTestCase
from app.repositories.meal_session_repo import MealSessionRepo
from factories import MealSessionFactory, LocationFactory, RoleFactory, UserRoleFactory


class TestMealSessionEndpoints(BaseTestCase):
    """Test class for meal session endpoints"""

    def setUp(self):
        self.BaseSetUp()
        self.current_date = datetime.now()

    def test_create_non_existing_meal_session_succeeds(self):
        """

        :return:
        """

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
        """

        :return:
        """
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
        """

        :return:
        """
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
        """

        :return:
        """
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
        """

        :return:
        """
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
        """

        :return:
        """
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
        """

        :return:
        """
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
        """

        :return:
        """
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
        """

        :return:
        """
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
            'lunch meal session(s) already exist between the specified start and stop times'
        )

    def test_create_meal_session_with_invalid_date_fails(self):
        """

        :return:
        """
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
        """

        :return:
        """
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
        """

        :return:
        """
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
        """

        :return:
        """
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
        """

        :return:
        """
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
        """

        :return:
        """
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
