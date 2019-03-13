from tests.base_test_case import BaseTestCase
from app.utils.auth import Auth, jwt
from unittest.mock import patch
from collections import namedtuple


class TestAuth(BaseTestCase):

    def setUp(self):
        self.BaseSetUp()

    def test_get_user_method_return_dict_of_user_data_if_valid_header_present(self):

        with self.app.test_request_context(path='/api/v1/vendors', method='GET', headers=self.headers()) as request:
            user_data = Auth._get_user()

            self.assertIsInstance(user_data, dict)
            self.assertIsNotNone(user_data)
            self.assertJSONKeysPresent(user_data, 'id', 'first_name', 'last_name', 'email')

    def test_user_method_return_list_of_user_data_based_on_supplied_keys(self):

        with self.app.test_request_context(path='/api/v1/vendors', method='GET', headers=self.headers()) as request:
            decoded = Auth.decode_token(self.get_valid_token())

            values = Auth.user('id', 'first_name', 'last_name', 'email')
            id, first_name, last_name, email = values

            self.assertIsInstance(values, list)
            self.assertEquals(decoded['UserInfo']['id'], id)
            self.assertEquals(decoded['UserInfo']['first_name'], first_name)
            self.assertEquals(decoded['UserInfo']['last_name'], last_name)
            self.assertEquals(decoded['UserInfo']['email'], email)

    def test_get_token_throws_exception_when_auth_header_missing(self):
        try:
            Auth.get_token()
            assert False
        except Exception as e:
            assert True

    def test_get_token_return_token_if_valid_header_present(self):

        with self.app.test_request_context(path='/api/v1/vendors', method='GET', headers=self.headers()) as request:
            token = Auth.get_token()

            self.assertIsInstance(token, str)
            self.assertIsNotNone(token)


    def test_decode_token_throws_exception_on_invalid_token(self):
        try:
            Auth.decode_token(self.get_invalid_token())
            assert False
        except Exception as e:
            assert True

    def test_decode_token_returns_dict_on_valid_token(self):
        token = Auth.decode_token(self.get_valid_token())
        if type(token) is dict:
            assert True
        else:
            assert False

    def test_get_location_throws_exception_when_location_header_missing(self):
        try:
            Auth.get_location()
            assert False
        except Exception as e:
            assert True

    def test_get_location_throws_exception_for_invalid_location_id(self):
        try:
            Auth.get_location('A')
            assert False
        except Exception as e:
            assert True


    def test_get_location_header_returns_int_value_when_location_header_present(self):
        with self.app.test_request_context(path='/api/v1/vendors', method='GET', headers=self.headers()) as request:
            location = Auth.get_location()
            self.assertIsInstance(location, int)
            self.assertIsNotNone(location)

    def test_unauthenticated_calls_throw_error(self):
        with self.app.test_request_context(path='/api/v1/vendors', method='GET',
                                                   headers=self.headers_without_token()) as request:
            self.assertRaises(Exception)

    def test_get_token_method_checks_no_authorization(self):

        with self.assertRaises(Exception) as e:

            class requestObject:
                headers = {}

            Auth.get_token(request_obj=requestObject)

        self.assertEqual(e.exception.args[0], 'Authorization Header is Expected')

    def test_user_method_raises_expection_when_not_auth_provided(self):

        with self.assertRaises(Exception) as e:
             Auth.user()

        self.assertEqual(e.exception.args[0], 'Authorization Header is Expected')

    @patch('app.utils.auth.Auth.get_token')
    def test_user_method_raises_expection_with_an_invalid_token(self, mock_get_token):

        with self.assertRaises(Exception) as e:
            mock_get_token.return_val = 'invalid_token'
            Auth.user()

        self.assertEqual(e.exception.args[0], 'Error Decoding')

    @patch('app.utils.auth.jwt.decode')
    def test_decode_token_method_raises_expection_with_an_expired_token(self, mock_jwt_decode):

        with self.assertRaises(Exception) as e:
            mock_jwt_decode.side_effect = jwt.ExpiredSignature()
            Auth.decode_token('tdtddyd')

        self.assertEqual(e.exception.args[0], 'Token is Expired')

    @patch('app.utils.auth.Auth.user')
    def test_has_permission_method_handles_missing_user_id(self, mock_auth_user):

        mock_auth_user.return_value = None

        response = Auth.has_permission('permission')('permission')()

        self.assertEqual(response[0].get_json()['msg'], 'Missing User ID in token')

    @patch('app.repositories.role_repo.RoleRepo.get')
    @patch('app.repositories.user_role_repo.UserRoleRepo.find_first')
    @patch('app.utils.auth.Auth.user')
    def test_has_role_method_handles_succeeds(self, mock_auth_user, mock_find_first, mock_role_repo):

        def mock_get(*args):
            get_obj = namedtuple('mock', 'name')

            return get_obj('admin')

        class MockRole:
            role_id = 1

        mock_auth_user.return_value = {'id': 1}
        mock_find_first.return_value = MockRole
        mock_role_repo.return_value = mock_get()

        response = Auth.has_role('admin')(lambda n: n)('test')

        self.assertEqual(response, 'test')

    @patch('app.utils.auth.Auth.user')
    def test_has_role_method_handles_user_not_found(self, mock_auth_user):

        mock_auth_user.return_value = None

        response = Auth.has_role('admin')(lambda n: n)('test')

        self.assertEqual(response[0].get_json()['msg'], 'Missing User ID in token')

    @patch('app.repositories.user_role_repo.UserRoleRepo.find_first')
    @patch('app.utils.auth.Auth.user')
    def test_has_role_method_handles_role_not_fond(self, mock_auth_user, mock_find_first):

        mock_auth_user.return_value = {'id': 1}
        mock_find_first.return_value = None

        response = Auth.has_role('admin')(lambda n: n)('test')

        self.assertEqual(response[0].get_json()['msg'], 'Access Error - No Role Granted')

    @patch('app.repositories.role_repo.RoleRepo.get')
    @patch('app.repositories.user_role_repo.UserRoleRepo.find_first')
    @patch('app.utils.auth.Auth.user')
    def test_has_role_method_handles_unmatching_roles(self, mock_auth_user, mock_find_first, mock_role_repo):

        def mock_get(*args):
            get_obj = namedtuple('mock', 'name')

            return get_obj('user')

        class MockRole:
            role_id = 1

        mock_auth_user.return_value = {'id': 1}
        mock_find_first.return_value = MockRole
        mock_role_repo.return_value = mock_get()

        response = Auth.has_role('admin')(lambda n: n)('test')

        self.assertEqual(response[0].get_json()['msg'], 'Access Error - This role does not have the access rights')
