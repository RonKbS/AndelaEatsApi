import base64
from tests.base_test_case import BaseTestCase
from app.models.about import About
from factories.about_factory import AboutFactory
from app.repositories.about_repo import AboutRepo


class TestAboutRepo(BaseTestCase):
    """
    Test class for the About repo
    """

    def setUp(self):
        self.BaseSetUp()
        self.repo = AboutRepo()

    def test_new_about_method_returns_new_about_object(self):
        """
        Test that new_about method actually creates an item in the database and returns
        an instance
        :return: None
        """
        new_about = self.repo.new_about(
            base64.b64encode("<html><head meta=\"utf-8\"></head></html>".encode('utf-8'))
        )

        self.assertIsInstance(new_about, About)
        self.assertIn(
            "meta=\"utf-8\"",
            base64.b64decode(new_about.details).decode('utf-8')
        )

    def test_first_item_method_returns_first_object(self):
        """
        Test first_item method actually returns the first item in the database
        :return: None
        """
        AboutFactory.create(
            details=base64.b64encode("<html><head meta=\"utf-8\"></head></html>".encode('utf-8'))
        )

        existing_about = self.repo.get_first_item()

        self.assertIsInstance(existing_about, About)
        self.assertIn(
            "meta=\"utf-8\"",
            base64.b64decode(existing_about.details).decode('utf-8')
        )

    def test_first_item_method_returns_nothing(self):
        """
        Test that the first_item method does not return anything when the database is empty
        :return: None
        """
        existing_about = self.repo.get_first_item()
        self.assertIsNone(existing_about)


