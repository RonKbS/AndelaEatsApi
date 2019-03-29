from tests.base_test_case import BaseTestCase
from app.utils.security import Security
from app.models import Faq
from unittest.mock import patch


class TestSecurity(BaseTestCase):

    def setUp(self):
        self.BaseSetUp()

    def test_url_validator_validates_empty_request_args(self):

        response = Security.url_validator('rules')('function')()

        self.assertEqual(response[0].get_json()['msg'], 'Bad Request - Request Must be Properly Formatted')

    def test_url_validator_validates_required_int_request_args(self):

        class MockRequest:
            args = {'age': 46}

        with patch('app.utils.security.request', new_callable=MockRequest):

            response = Security.url_validator(['age|required:int'])(lambda *args, **kwargs: ('test',))()

        self.assertEqual(response, ('test',))

    def test_url_validator_validates_required_int_missing(self):

        class MockRequest:
            args = {'name': 'test'}

        with patch('app.utils.security.request', new_callable=MockRequest):

            response = Security.url_validator(['age|required:int'])(lambda *args, **kwargs: ('test',))()

        self.assertEqual(response[0].get_json()['msg'], 'Bad Request - age is required')

    def test_url_validator_validates_invalid_int_type(self):

        class MockRequest:
            args = {'age': 'test'}

        with patch('app.utils.security.request', new_callable=MockRequest):

            response = Security.url_validator(['age|required:int'])(lambda *args, **kwargs: ('test',))()

        self.assertEqual(response[0].get_json()['msg'], 'Bad Request - age must be integer')

    def test_url_validator_validates_optional_int_request_args(self):

        class MockRequest:
            args = {'name': 'test'}

        with patch('app.utils.security.request', new_callable=MockRequest):

            response = Security.url_validator(['age|optional:int'])(lambda *args, **kwargs: ('test',))()

        self.assertEqual(response, ('test',))

    def test_url_validator_validates_range(self):
        class MockRequest:
            args = {'dates': '2019-02-02:2019-01-01'}

        with patch('app.utils.security.request', new_callable=MockRequest):
            response = Security.url_validator(['dates|optional:range'])(lambda *args, **kwargs: ('test',))()

        self.assertEqual(
            response[0].get_json()['msg'],
            'Bad Request - Start Date [2019-02-02 00:00:00] must be less than End Date[2019-01-01 00:00:00]')

    def test_url_validator_validates_float_type(self):
        class MockRequest:
            args = {'dates': '2019-02-02:2019-01-01'}

        with patch('app.utils.security.request', new_callable=MockRequest):
            response = Security.url_validator(['dates|optional:float'])(lambda *args, **kwargs: ('test',))()

        self.assertEqual(
            response[0].get_json()['msg'], 'Bad Request - dates must be float')

    def test_url_validator_validates_maximum_value(self):
        class MockRequest:
            args = {'age': 20}

        with patch('app.utils.security.request', new_callable=MockRequest):
            response = Security.url_validator(['age|required:max-17'])(lambda *args, **kwargs: ('test',))()

        self.assertEqual(
            response[0].get_json()['msg'], 'Bad Request - age can only have a max value of 17')

    def test_url_validator_validates_minimum_value(self):
        class MockRequest:
            args = {'age': 17}

        with patch('app.utils.security.request', new_callable=MockRequest):
            response = Security.url_validator(['age|required:min-18'])(lambda *args, **kwargs: ('test',))()

        self.assertEqual(
            response[0].get_json()['msg'], 'Bad Request - age can only have a min value of 18')

    def test_url_validator_validates_length_value(self):
        class MockRequest:
            args = {'username': 'name-longer-than-10-chars'}

        with patch('app.utils.security.request', new_callable=MockRequest):
            response = Security.url_validator(['username|required:length-10'])(lambda *args, **kwargs: ('test',))()

        self.assertEqual(
            response[0].get_json()['msg'], 'Bad Request - username can only have a len of 10')

    def test_url_validator_validates_exists(self):
        class MockRequest:
            args = {'proteinItems': 1}

        with patch('app.utils.security.request', new_callable=MockRequest):
            response = Security.url_validator(['proteinItems|exists|meal_item|id'])(lambda *args, **kwargs: ('test',))()

        self.assertEqual(
            response[0].get_json()['msg'], 'Bad Request - proteinItems contains invalid id(s) for meal_item table ')

    def test_url_validator_validates_list_exists(self):
        class MockRequest:
            args = {'proteinItems': [1]}

        with patch('app.utils.security.request', new_callable=MockRequest):
            response = Security.url_validator(['proteinItems|exists|meal_item|id'])(lambda *args, **kwargs: ('test',))()

        self.assertEqual(
            response[0].get_json()['msg'], 'Bad Request - proteinItems contains invalid id(s) for meal_item table ')

    def test_url_validator_validates_date(self):
        class MockRequest:
            args = {'startDate': 'not a valid date'}

        with patch('app.utils.security.request', new_callable=MockRequest):
            response = Security.url_validator(['startDate|required:date'])(lambda *args, **kwargs: ('test',))()

        self.assertEqual(
            response[0].get_json()['msg'], 'Bad Request - startDate should be valid date. Format: YYYY-MM-DD')

    def test_url_validator_validates_list(self):
        class MockRequest:
            args = {'mealList': 'not a valid list'}

        with patch('app.utils.security.request', new_callable=MockRequest):
            response = Security.url_validator(['mealList|required:list'])(lambda *args, **kwargs: ('test',))()

        self.assertEqual(
            response[0].get_json()['msg'], 'Bad Request - mealList must be a list')

    def test_url_validator_validates_list_int_not_a_valid_list(self):
        class MockRequest:
            args = {'mealList': 'not a valid list'}

        with patch('app.utils.security.request', new_callable=MockRequest):
            response = Security.url_validator(['mealList|required:list_int'])(lambda *args, **kwargs: ('test',))()

        self.assertEqual(
            response[0].get_json()['msg'], 'Bad Request - mealList must be a list')

    def test_url_validator_validates_list_int_items_are_all_int(self):
        class MockRequest:
            args = {'mealList': [1, 2, 'string']}

        with patch('app.utils.security.request', new_callable=MockRequest):
            response = Security.url_validator(['mealList|required:list_int'])(lambda *args, **kwargs: ('test',))()

        self.assertEqual(
            response[0].get_json()['msg'], 'Bad Request - [string] in list must be integer')

    def test_validator_validates_empty_request_json(self):
        class MockRequest:
            json = {}

        with patch('app.utils.security.request', new_callable=MockRequest):
            response = Security.validator(['mealList|required:list_int'])(lambda *args, **kwargs: ('test',))()

        self.assertEqual(
            response[0].get_json()['msg'], 'Bad Request - Request Must be JSON Formatted')

    def test_validator_validates_int_request_json(self):
        class MockRequest:
            json = {
                'age': 'test'
            }

            @classmethod
            def get_json(cls):
                return cls.json

        with patch('app.utils.security.request', new_callable=MockRequest):
            response = Security.validator(['age|required:int'])(lambda *args, **kwargs: ('test',))()

        self.assertEqual(
            response[0].get_json()['msg'], 'Bad Request - age must be integer')

    def test_validator_validates_float_request_json(self):
        class MockRequest:
            json = {
                'age': 'test'
            }

            @classmethod
            def get_json(cls):
                return cls.json

        with patch('app.utils.security.request', new_callable=MockRequest):
            response = Security.validator(['age|required:float'])(lambda *args, **kwargs: ('test',))()

        self.assertEqual(
            response[0].get_json()['msg'], 'Bad Request - age must be float')

    def test_validator_validates_maximum_value_in_request_json(self):
        class MockRequest:
            json = {
                'age': 20
            }

            @classmethod
            def get_json(cls):
                return cls.json

        with patch('app.utils.security.request', new_callable=MockRequest):
            response = Security.validator(['age|required:max-17'])(lambda *args, **kwargs: ('test',))()

        self.assertEqual(
            response[0].get_json()['msg'], 'Bad Request - age can only have a max value of 17')

    def test_validator_validates_minimum_value_in_request_json(self):
        class MockRequest:
            json = {
                'age': 17
            }

            @classmethod
            def get_json(cls):
                return cls.json

        with patch('app.utils.security.request', new_callable=MockRequest):
            response = Security.validator(['age|required:min-18'])(lambda *args, **kwargs: ('test',))()

        self.assertEqual(
            response[0].get_json()['msg'], 'Bad Request - age can only have a min value of 18')

    def test_validator_validates_length_value_in_request_json(self):
        class MockRequest:
            json = {
                'username': 'username-longer-than-10-chars'
            }

            @classmethod
            def get_json(cls):
                return cls.json

        with patch('app.utils.security.request', new_callable=MockRequest):
            response = Security.validator(['username|required:length-10'])(lambda *args, **kwargs: ('test',))()

        self.assertEqual(
            response[0].get_json()['msg'], 'Bad Request - username can only have a len of 10')

    def test_validator_validates_date_in_request_json(self):
        class MockRequest:
            json = {
                'startDate': 'invalid date'
            }

            @classmethod
            def get_json(cls):
                return cls.json

        with patch('app.utils.security.request', new_callable=MockRequest):
            response = Security.validator(['startDate|required:date'])(lambda *args, **kwargs: ('test',))()

        self.assertEqual(
            response[0].get_json()['msg'], 'Bad Request - startDate should be valid date. Format: YYYY-MM-DD')

    def test_validator_validates_list_in_request_json(self):
        class MockRequest:
            json = {
                'mealList': 'invalid list'
            }

            @classmethod
            def get_json(cls):
                return cls.json

        with patch('app.utils.security.request', new_callable=MockRequest):
            response = Security.validator(['mealList|required:list'])(lambda *args, **kwargs: ('test',))()

        self.assertEqual(
            response[0].get_json()['msg'], 'Bad Request - mealList must be a list')

    def test_validator_validates_list_int_in_request_json(self):
        class MockRequest:
            json = {
                'mealList': 'invalid list'
            }

            @classmethod
            def get_json(cls):
                return cls.json

        with patch('app.utils.security.request', new_callable=MockRequest):
            response = Security.validator(['mealList|required:list_int'])(lambda *args, **kwargs: ('test',))()

        self.assertEqual(
            response[0].get_json()['msg'], 'Bad Request - mealList must be a list')

    def test_validator_validates_list_int_contains_only_ints_in_request_json(self):
        class MockRequest:
            json = {
                'mealList': [1, 2, 'not an int']
            }

            @classmethod
            def get_json(cls):
                return cls.json

        with patch('app.utils.security.request', new_callable=MockRequest):
            response = Security.validator(['mealList|required:list_int'])(lambda *args, **kwargs: ('test',))()

        self.assertEqual(
            response[0].get_json()['msg'], 'Bad Request - [not an int] in list must be integer')

    def test_validator_validates_enums(self):
        class MockRequest:
            json = {
                'category': 'user_faqs'
            }

            @classmethod
            def get_json(cls):
                return cls.json

        with patch('app.utils.security.request', new_callable=MockRequest):
            response = Security.validator(['category|required:enum_FaqCategoryType'])(lambda *args, **kwargs: ('test',))()

        self.assertEqual(
            response[0].get_json()['msg'],
            "Bad Request - 'user_faqs' is not a valid value for key 'category'. "
            "values must be any of the following ['user_faq', 'admin_faq']"
        )

    def test_validate_query_params_validates_model_fields(self):

        class MockRequest:
            args = {'unknown': 46}

        with patch('app.utils.security.request', new_callable=MockRequest):

            response = Security.validate_query_params(Faq)(lambda *args, **kwargs: ('test',))()

        self.assertEqual(
            response[0].get_json()['msg'],
            "Invalid keys ['unknown']. The supported keys are "
            "['Id', 'IsDeleted', 'CreatedAt', 'UpdatedAt', 'Category', 'Question', 'Answer']"
        )

    def test_validate_query_params_succeeds_with_enpty_args(self):

        class MockRequest:
            args = {}

        with patch('app.utils.security.request', new_callable=MockRequest):

            response = Security.validate_query_params(Faq)(lambda *args, **kwargs: ('test',))()

        self.assertEqual(response, ('test',))

    def test_validate_enums_validates_enum_values(self):

        response = Security.validate_enums('enum_FaqCategoryType', 'category', 'user_faqs')

        self.assertEqual(
            response[0].get_json()['msg'],
            "Bad Request - 'user_faqs' is not a valid value for key 'category'. "
            "values must be any of the following ['user_faq', 'admin_faq']"
        )

    def test_validator_validates_for_non_enum_required_and_non_existing_enum(self):
        class MockRequest:
            args = {
                'action_typ': 'create'
            }

        with patch('app.utils.security.request', new_callable=MockRequest):
            response = Security.url_validator(['action_typ|enum_options'])(lambda *args, **kwargs: ('test',))()

        self.assertIn(
            'Bad Request - Invalid search field', response[0].get_json()['msg'])

    def test_validator_validates_email(self):
        class MockRequest:
            json = {
                'email': 'invalid@email'
            }

            @classmethod
            def get_json(cls):
                return cls.json

        with patch('app.utils.security.request', new_callable=MockRequest):
            response = Security.validator(['email|required:email'])(lambda *args, **kwargs: ('test',))()

        self.assertEqual(
            response[0].get_json()['msg'], "Bad Request - 'invalid@email' is not a valid email address.")

    def test_validator_validates_urls(self):
        class MockRequest:
            json = {
                'imageUrl': 'invalid@url'
            }

            @classmethod
            def get_json(cls):
                return cls.json

        with patch('app.utils.security.request', new_callable=MockRequest):
            response = Security.validator(['imageUrl|required:url'])(lambda *args, **kwargs: ('test',))()

        self.assertEqual(
            response[0].get_json()['msg'], "Bad Request - 'invalid@url' is not a valid url.")
