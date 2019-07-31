from tests.base_test_case import BaseTestCase
from app.models.base_model import BaseModel
from unittest.mock import patch, MagicMock


class TestBaseModel(BaseTestCase):

    def setUp(self):
        self.BaseSetUp()

    def tearDown(self):
        self.BaseTearDown()

    def test_base_model_delete_method(self):

        with patch('app.models.base_model.db.session') as mock_db:
            mock_delete = MagicMock(return_value=None)
            mock_commit = MagicMock(return_value=None)

            mock_db.delete = mock_delete
            mock_db.commit = mock_commit

            BaseModel().delete()

            mock_delete.assert_called_once()
            mock_commit.assert_called_once()
