'''Unit tests for the meal item controller.
'''
from datetime import datetime
from unittest.mock import patch

from app.controllers.meal_item_controller import MealItemController
from app.models import MealItem
from app.repositories.meal_item_repo import MealItemRepo
from app.utils.enums import MealTypes
from tests.base_test_case import BaseTestCase


class TestMealItemController(BaseTestCase):

    def setUp(self):
        self.BaseSetUp()
        self.mock_meal_item = MealItem(
            is_deleted=False,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            meal_type='Mock meal type',
            name='Mock meal item',
            description='Mock description',
            image='Mock image',
            location_id=1
        )

    @patch.object(MealItemRepo, 'get_unpaginated')
    @patch('app.Auth.get_location')
    def test_list_meals_ok_response(
        self,
        mock_get_location,
        mock_get_unpaginated
    ):
        '''Test list_meals OK response.
        '''
        # Arrange
        with self.app.app_context():
            mock_get_location.return_value = 1
            mock_get_unpaginated.return_value = [self.mock_meal_item, ]
            meal_item_controller = MealItemController(self.request_context)

            # Act
            result = meal_item_controller.list_meals()

            # Assert
            assert result.status_code == 200
            assert result.get_json()['msg'] == 'OK'

    @patch('app.Auth.get_location')
    @patch.object(MealItemRepo, 'filter_by')
    @patch.object(MealItemController, 'pagination_meta')
    def test_list_meals_page_ok_response(
        self,
        mock_pagination_meta,
        mock_filter_by,
        mock_get_location
    ):
        '''Test list_meals_page OK response.
        '''
        # Arrange
        with self.app.app_context():
            mock_get_location.return_value = 1
            mock_filter_by.return_value.items = [self.mock_meal_item, ]
            mock_pagination_meta.return_value = {
                'total_rows': 1,
                'total_pages': 1,
                'current_page': 1,
                'next_page': 1,
                'prev_page': 1
            }
            meal_item_controller = MealItemController(self.request_context)

            # Act
            result = meal_item_controller.list_meals_page(1, 10)

            # Assert
            assert result.status_code == 200
            assert result.get_json()['msg'] == 'OK'
