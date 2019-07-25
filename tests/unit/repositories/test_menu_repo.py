from tests.base_test_case import BaseTestCase
from app.models.menu import Menu
from factories.menu_factory import MenuFactory
from app.repositories.menu_repo import MenuRepo
from factories.location_factory import LocationFactory
from factories.meal_item_factory import MealItemFactory
from factories.vendor_engagement_factory import VendorEngagementFactory


class TestMenuRepo(BaseTestCase):

    def setUp(self):
        self.repo = MenuRepo()
        self.BaseSetUp()

    def tearDown(self):
        self.BaseTearDown()

    def test_new_menu_method_returns_new_menu_object(self):
        location = LocationFactory()
        meal_item = MealItemFactory.create(location=location)
        vendor_engagement = VendorEngagementFactory()
        menu = MenuFactory(
            location=location,
            main_meal_id=meal_item.id,
            vendor_engagement=vendor_engagement
        )

        new_menu = self.repo.new_menu(
            menu.date.strftime('%Y-%m-%d'), menu.meal_period, menu.main_meal_id, menu.allowed_side,
            menu.allowed_protein, [1,2], [3,4], vendor_engagement.id, location.id
        )

        self.assertIsInstance(new_menu, Menu)
        self.assertEqual(new_menu.allowed_protein, menu.allowed_protein)
        self.assertEqual(new_menu.allowed_side, menu.allowed_protein)
        self.assertEqual(new_menu.meal_period, menu.meal_period)

        self.assertIsInstance(new_menu, Menu)
        self.assertEqual(new_menu.allowed_protein, menu.allowed_protein)
        self.assertEqual(new_menu.allowed_side, menu.allowed_protein)
        self.assertEqual(new_menu.meal_period, menu.meal_period)
