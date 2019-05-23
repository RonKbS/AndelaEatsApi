'''
Unit tests for the User Controller.
'''
from datetime import datetime
from unittest.mock import patch

from app.controllers.user_controller import UserController
from app.models.user_role import UserRole
from tests.base_test_case import BaseTestCase
from factories.user_factory import UserFactory
from factories import RoleFactory, UserRoleFactory
from factories.location_factory import LocationFactory
from app.utils.auth import Auth


class TestUserController(BaseTestCase):
    '''
    UserController test class.
    '''

    def setUp(self):
        self.BaseSetUp()
        self.mock_user_role = UserRole(
            id=1,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            role_id=1,
            location_id=1,
            user_id='mock',
            is_active=True
        )

    @patch('app.repositories.user_role_repo.UserRoleRepo.filter_by')
    @patch('app.services.andela.AndelaService.get_user_by_email_or_id')
    def test_list_admin_users_ok_response(
        self,
        mock_get_user_by_email_or_id,
        mock_filter_by
    ):
        '''
        Test list_admin_users OK response.
        '''
        # Arrange
        with self.app.app_context():
            mock_filter_by.return_value.items = [self.mock_user_role, ]
            mock_get_user_by_email_or_id.return_value = {
                "id": "-LXTuXlk2W4Gskt8KTte",
                "email": "joseph.serunjogi@andela.com",
                "first_name": "Joseph",
                "last_name": "Serunjogi",
                "name": "Joseph Serunjogi"
            }
            user_controller = UserController(self.request_context)

            # Act
            result = user_controller.list_admin_users()

            # Assert
            assert result.status_code == 200
            assert result.get_json()['msg'] == 'OK'

    @patch.object(Auth, 'get_location')
    @patch.object(UserController, 'request_params')
    def test_create_user_succeeds(self, mock_request_params, mock_get_location):
        location = LocationFactory()
        role = RoleFactory(name='test_role')

        with self.app.app_context():
            mock_get_location.return_value = location.id

            mock_request_params.return_value = [
                "Joseph",
                "Serunjogi",
                None,
                None,
                "-LXTuXlk2W4Gskt8KTte",
                role.id
            ]
            user_controller = UserController(self.request_context)

            # Act
            result = user_controller.create_user()

            # Assert
            assert result.status_code == 201
            assert result.get_json()['msg'] == 'OK'

    @patch.object(UserController, 'request_params')
    def test_create_user_method_handles_user_creation_with_duplicate_slack_id(self, mock_request_params):
        with self.app.app_context():
            user = UserFactory(slack_id="-LXTuXlk2W4Gskt8KTte")
            role = RoleFactory(name='test_role')

            mock_request_params.return_value = [
                "Joseph",
                "Serunjogi",
                None,
                user.slack_id,
                "-LXTuXlk2W4Gskt8KTte",
                role.id
            ]

            user_controller = UserController(self.request_context)

            response = user_controller.create_user()

            self.assertEqual(response.status_code, 400)
            self.assertEqual(
                response.get_json()['msg'],
                "User with slackId '{}' already exists".format(user.slack_id)
            )

    @patch.object(UserController, 'request_params')
    def test_create_user_method_handles_user_creation_with_duplicate_user_id(self, mock_request_params):
        with self.app.app_context():
            user = UserFactory(user_id="-LXTuXlk2W4Gskt8KTte")
            role = RoleFactory(name='test_role')

            mock_request_params.return_value = [
                "Joseph",
                "Serunjogi",
                None,
                None,
                user.user_id,
                role.id
            ]

            user_controller = UserController(self.request_context)

            response = user_controller.create_user()

            self.assertEqual(response.status_code, 400)
            self.assertEqual(
                response.get_json()['msg'],
                "User with userId '{}' already exists".format(user.user_id)
            )

    @patch.object(UserController, 'request_params')
    def test_create_user_method_handles_user_creation_with_non_existent_role_id(self, mock_request_params):
        with self.app.app_context():
            user = UserFactory(user_id="-LXTuXlk2W4Gskt8KTte")

            non_existent_role_id = 100

            mock_request_params.return_value = [
                "Joseph",
                "Serunjogi",
                None,
                None,
                user.user_id,
                non_existent_role_id
            ]

            user_controller = UserController(self.request_context)

            response = user_controller.create_user()

            self.assertEqual(response.status_code, 400)
            self.assertEqual(
                response.get_json()['msg'],
                "Role with userTypeId(roleId) {} does not exist".format(non_existent_role_id)
            )

    def test_list_user_succeeds(self):

        with self.app.app_context():
            role = RoleFactory()
            user_role = UserRoleFactory(role_id=role.id)
            user = UserFactory(slack_id="-LXTuXlk2W4Gskt8KTte", user_type_id=user_role.id)

            user_controller = UserController(self.request_context)

            response = user_controller.list_user(slack_id=user.slack_id)

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.get_json()['msg'], "OK")
            self.assertEqual(response.get_json()['payload']['user']['slackId'], user.slack_id)
            self.assertEqual(response.get_json()['payload']['user']['firstName'], user.first_name)
            self.assertEqual(response.get_json()['payload']['user']['lastName'], user.last_name)

    def test_list_user_when_user_found_succeeds(self):
        with self.app.app_context():

            user_controller = UserController(self.request_context)

            response = user_controller.list_user(slack_id="-LXTuXlk2W4Gskt8KTtedhmdydsbnyw")

            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.get_json()['msg'], 'User not found')
