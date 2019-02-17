from tests.base_test_case import BaseTestCase
from subprocess import call
from app.utils.seeders.seed_database import model_mapper, bulk_insert
from unittest.mock import patch
from sqlalchemy.exc import SQLAlchemyError


class TestSeeders(BaseTestCase):

    def setUp(self):
        self.BaseSetUp()

    def test_flask_seed_database_succeeds_without_arguments(self):

        call(['flask', 'seed_database'])

        for data in model_mapper.values():
            model = data.get('model')
            result = model.query.count()

            assert result > 0

    def test_flask_database_succeeds_valid_arguments(self):

        call(['flask', 'seed_database', 'location'])

        model = model_mapper.get('location').get('model')
        result = model.query.count()

        assert result > 0

    @patch('app.utils.seeders.seed_database.db.session.bulk_insert_mappings')
    def test_flask_seed_raises_expection_on_duplicate_seed_data(self, mock_bulk_insert):

        mock_bulk_insert.side_effect = SQLAlchemyError()

        with self.assertRaises(Exception) as e:
            bulk_insert(**model_mapper.get('location'))

