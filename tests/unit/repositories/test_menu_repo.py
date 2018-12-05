from tests.base_test_case import BaseTestCase
from app.models.menu import Menu
from factories.menu_factory import MenuFactory
from app.repositories.menu_repo import MenuRepo


class TestMenuRepo(BaseTestCase):

  def setUp(self):
    self.BaseSetUp()
    self.repo = MenuRepo()

  def test_new_menu_method_returns_new_menu_object(self):
    menu = MenuFactory.build()
    new_menu = self.repo.new_menu(
      menu.date.strftime('%Y-%m-%d'), menu.meal_period, 1, menu.allowed_side,
      menu.allowed_protein, [1,2], [3,4], 1,1
    )

    self.assertIsInstance(new_menu, Menu)
    self.assertEqual(new_menu.allowed_protein, menu.allowed_protein)
    self.assertEqual(new_menu.allowed_side, menu.allowed_protein)
    self.assertEqual(new_menu.meal_period, menu.meal_period)
