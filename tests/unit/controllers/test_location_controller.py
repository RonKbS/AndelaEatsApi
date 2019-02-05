'''Unit tests for app.location_controller module.
'''
from datetime import datetime
from unittest.mock import patch

from app.controllers.location_controller import LocationController
from app.models.location import Location
from app.repositories.location_repo import LocationRepo
from tests.base_test_case import BaseTestCase


class TestLocationController(BaseTestCase):

    def setUp(self):
        self.BaseSetUp()

    @patch.object(LocationRepo, 'fetch_all')
    @patch.object(LocationController, 'pagination_meta')
    def test_list_locations_ok_response(
        self,
        mock_location_controller_pagination_meta,
        mock_location_repo_fetch_all
    ):
        '''Test fetch_all response.
        '''
        # Arrange
        with self.app.app_context():
            mock_location = Location(
                id=1,
                created_at=datetime.now(),
                updated_at=datetime.now(),
                name='Mock location',
                zone='Mock zone'
            )
            mock_location_repo_fetch_all.return_value.items = [mock_location, ]
            mock_location_controller_pagination_meta.return_value = {
                'total_rows': 1,
                'total_pages': 1,
                'current_page': 1,
                'next_page': False,
                'prev_page': False
            }
            location_controller = LocationController(self.request_context)

            # Act
            result = location_controller.list_locations()

            # Assert
            assert result.status_code == 200
            assert result.get_json()['msg'] == 'OK'

    @patch.object(LocationRepo, 'get')
    def test_get_location_doesnot_exist(
        self,
        mock_location_repo_get
    ):
        '''Test get_location response when the location does not exist.
        '''
        # Arrange
        with self.app.app_context():
            mock_location_repo_get.return_value = None
            mock_location_id = 1
            location_controller = LocationController(self.request_context)

            # Act
            result = location_controller.get_location(mock_location_id)

            # Assert
            assert result.status_code == 400
            assert result.get_json()['msg'] == 'Invalid or Missing location_id'

    @patch.object(LocationRepo, 'get')
    def test_get_location_ok_response(
        self,
        mock_location_repo_get
    ):
        '''Test get_location OK response.
        '''
        # Arrange
        with self.app.app_context():
            mock_location = Location(
                id=1,
                created_at=datetime.now(),
                updated_at=datetime.now(),
                name='Mock location',
                zone='Mock zone'
            )
            mock_location_id = 1
            mock_location_repo_get.return_value = mock_location
            location_controller = LocationController(self.request_context)

            # Act
            result = location_controller.get_location(mock_location_id)

            # Assert
            assert result.status_code == 200
            assert result.get_json()['msg'] == 'OK'
