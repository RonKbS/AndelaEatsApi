'''Unit tests for the menu_controller module.
'''
from datetime import datetime
from unittest.mock import Mock, patch

from app.controllers.menu_controller import MenuController
from app.models import MealItem, Menu
from app.repositories.menu_repo import MenuRepo
from app.repositories.meal_item_repo import MealItemRepo
from tests.base_test_case import BaseTestCase


class TestMenuController(BaseTestCase):

    def setUp(self):
        self.BaseSetUp()

    @patch.object(MenuRepo, 'get_meal_items')
    @patch.object(MealItemRepo, 'get')
    @patch.object(MenuRepo, 'new_menu')
    @patch.object(MenuRepo, 'get_unpaginated')
    @patch.object(MenuController, 'request_params')
    @patch('app.Auth.get_location')
    def test_create_menu_when_menu_exists(
        self,
        mock_get_location,
        mock_request_params,
        mock_get_unpaginated,
        mock_new_menu,
        mock_get,
        mock_get_meal_items
    ):
        '''Test the response returned when menu already exists.
        '''
        # Arrange
        with self.app.app_context():
            mock_get_location.return_value = 1
            mock_request_params.return_value = (
                None, None, None, None, None, None, None, None
            )
            mock_get_unpaginated.return_value = [
                {
                    'date': Mock(),
                    'meal_period': Mock(),
                    'location_id': Mock()
                },
            ]
            mock_new_menu.return_value = {
                'date': datetime.now(),
                'meal_period': Mock(),
                'main_meal_id': Mock(),
                'allowed_side': Mock(),
                'location_id': Mock()
            }
            mock_get.return_value = {
                'meal_type': Mock(),
                'name': Mock(),
                'description': Mock(),
                'image': Mock(),
                'location_id': Mock(),
                'location': Mock()
            }
            mock_get_meal_items.return_value = Mock()
            menu_controller = MenuController(self.request_context)

            # Act
            result = menu_controller.create_menu()

            # Assert
            assert result.status_code == 400
            assert result.get_json()['msg'] == "You can't create multiple " \
                "menus with same main item on the same day"

    @patch.object(MenuRepo, 'get_meal_items')
    @patch.object(MealItemRepo, 'get')
    @patch.object(MenuRepo, 'new_menu')
    @patch.object(MenuRepo, 'get_unpaginated')
    @patch.object(MenuController, 'request_params')
    @patch('app.Auth.get_location')
    def test_create_menu_successful(
        self,
        mock_get_location,
        mock_request_params,
        mock_get_unpaginated,
        mock_new_menu,
        mock_get,
        mock_get_meal_items
    ):
        '''Test response returned when the menu is created successfully.
        '''
        # Arrange
        with self.app.app_context():
            mock_get_location.return_value = 1
            mock_request_params.return_value = (
                None, None, None, None, None, None, None, None
            )
            mock_get_unpaginated.return_value = None
            mock_new_menu.return_value = MealItem(
                meal_type='',
                name='',
                description='',
                image='',
                location_id=0,
                created_at=datetime.now(),
                updated_at=datetime.now(),
                is_deleted=False,
                id=1,
                location={}
            )
            mock_get.return_value = MealItem(
                meal_type='',
                name='',
                description='',
                image='',
                location_id=0,
                created_at=datetime.now(),
                updated_at=datetime.now(),
                is_deleted=False,
                id=1
            )
            mock_get_meal_items.return_value = []
            menu_controller = MenuController(self.request_context)

            # Act
            result = menu_controller.create_menu()

            # Assert
            assert result.status_code == 201
            assert result.get_json()['msg'] == "OK"

    @patch.object(MenuRepo, 'get')
    def test_delete_menu_not_found(
        self,
        mock_menu_repo_get
    ):
        '''Test response on delete_menu when menu does not exist.
        '''
        # Arrange
        with self.app.app_context():
            mock_menu_repo_get.return_value = None
            menu_controller = MenuController(self.request_context)

            # Act
            result = menu_controller.delete_menu(1)

            # Assert
            assert result.status_code == 400
            assert result.get_json()['msg'] == 'Invalid or incorrect ' \
                'menu_id provided'

    @patch.object(MenuRepo, 'get')
    def test_delete_menu_already_deleted(
        self,
        mock_menu_repo_get
    ):
        '''Test response on delete_menu when menu is already
        deleted.
        '''
        # Arrange
        with self.app.app_context():
            mock_menu_repo_get.return_value = Menu(
                is_deleted=True
            )
            menu_controller = MenuController(self.request_context)

            # Act
            result = menu_controller.delete_menu(1)

            # Assert
            assert result.status_code == 400
            assert result.get_json()['msg'] == 'Menu has already been deleted'

    @patch.object(MealItemRepo, 'update')
    @patch.object(MenuRepo, 'get')
    def test_delete_menu_successful(
        self,
        mock_menu_repo_get,
        mock_meal_repo_update
    ):
        '''Test delete_menu success.
        '''
        with self.app.app_context():
            mock_menu_repo_get.return_value = Menu(
                is_deleted=False
            )
            mock_meal_repo_update.return_value = Mock()
            menu_controller = MenuController(self.request_context)

            # Act
            result = menu_controller.delete_menu(1)

            # Assert
            assert result.status_code == 200
            assert result.get_json()['msg'] == 'Menu deleted'
            assert result.get_json()['payload']['status'] == 'success'
