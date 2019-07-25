from tests.base_test_case import BaseTestCase
from app.models.order import Order
from factories.order_factory import OrderFactory
from factories.meal_item_factory import MealItemFactory
from app.repositories.order_repo import OrderRepo
from app.repositories.meal_item_repo import MealItemRepo
from factories.location_factory import LocationFactory
from factories.meal_item_factory import MealItemFactory
from factories.vendor_engagement_factory import VendorEngagementFactory
from factories.menu_factory import MenuFactory


class TestOrderRepo(BaseTestCase):

    def setUp(self):
        self.BaseSetUp()
        self.repo = OrderRepo()
        self.location = LocationFactory()
        self.meal_item = MealItemFactory(location_id=self.location.id)
        self.vendor_engagement = VendorEngagementFactory(
            location_id=self.location.id
        )
        self.menu = MenuFactory(
            location_id=self.location.id,
            main_meal_id=self.meal_item.id,
            vendor_engagement_id=self.vendor_engagement.id
        )

    def tearDown(self):
        self.BaseTearDown()

    def test_create_order_method_returns_new_order_object(self):
        order = OrderFactory.build(
            menu_id=self.menu.id,
            location_id=self.location.id
        )
        new_order = self.repo.create_order(
            order.user_id, order.date_booked_for.strftime('%Y-%m-%d'), order.meal_item_orders, order.location_id,
            order.menu_id, order.channel, order.meal_period
        )

        self.assertIsInstance(new_order, Order)
        self.assertEqual(new_order.user_id, order.user_id)
        self.assertEqual(new_order.meal_item_orders, order.meal_item_orders)
        self.assertEqual(new_order.meal_period, order.meal_period)

    def test_update_order_method_updates_order_object(self):
        new_meal = MealItemFactory(
            name=self.meal_item.name,
            image=self.meal_item.image,
            meal_type=self.meal_item.meal_type,
            location_id=self.meal_item.location.id
        )

        order = OrderFactory.create(
            menu_id=self.menu.id,
            location_id=self.location.id,
            location=self.location
        )
        new_order = self.repo.create_order(
            order.user_id, order.date_booked_for.strftime('%Y-%m-%d'), order.meal_item_orders, order.location_id,
            order.menu_id, order.channel, order.meal_period
        )

        update_meal_list = [new_meal]

        update_order = self.repo.update_order(
            order.user_id, order.date_booked_for.strftime('%Y-%m-%d'), new_order.date_booked.strftime('%Y-%m-%d'),
            update_meal_list, order.location_id
        )

        self.assertIsInstance(update_order, Order)
        self.assertEqual(new_order.user_id, order.user_id)
        self.assertEqual(update_order.meal_item_orders, update_meal_list)

    def test_get_range_paginated_options_method_returns_paginated_object(self):
        order = OrderFactory.build(
            menu_id=self.menu.id,
            location_id=self.location.id
        )
        new_order = self.repo.create_order(
            order.user_id, order.date_booked_for.strftime('%Y-%m-%d'), order.meal_item_orders, order.location_id,
            order.menu_id, order.channel, order.meal_period
        )

        paginated_result = self.repo.get_range_paginated_options(
            order.user_id, start_date=order.date_booked, end_date=order.date_booked_for
        )

        self.assertIsInstance(paginated_result.items[0], Order)
        self.assertEqual(paginated_result.items[0], new_order)

    def test_get_range_paginated_options_all_method_returns_paginated_object(self):
        order = OrderFactory.build(
            menu_id=self.menu.id,
            location_id=self.location.id
        )
        new_order = self.repo.create_order(
            order.user_id, order.date_booked_for.strftime('%Y-%m-%d'), order.meal_item_orders, order.location_id,
            order.menu_id, order.channel, order.meal_period
        )

        paginated_result = self.repo.get_range_paginated_options_all(
          start_date=order.date_booked, end_date=order.date_booked_for, location_id=new_order.location_id
        )

        self.assertIsInstance(paginated_result.items[0], Order)
        self.assertEqual(paginated_result.items[0], new_order)

    def test_user_has_order_method_user_has_order_when_user_has_an_order(self):
        order = OrderFactory.build(
            menu_id=self.menu.id,
            location_id=self.location.id
        )
        new_order = self.repo.create_order(
            order.user_id, order.date_booked_for.strftime('%Y-%m-%d'), order.meal_item_orders, order.location_id,
            order.menu_id, order.channel, order.meal_period
        )

        result = self.repo.user_has_order(
          order.user_id, date_booked=order.date_booked_for.strftime('%Y-%m-%d'), meal_period=new_order.meal_period
        )

        self.assertEqual(result, True)

    def test_user_has_order_method_user_has_order_when_user_has_no_order(self):
        order = OrderFactory.build(
            menu_id=self.menu.id,
            location_id=self.location.id
        )
        new_order = self.repo.create_order(
            order.user_id, order.date_booked_for.strftime('%Y-%m-%d'), order.meal_item_orders, order.location_id,
            order.menu_id, order.channel, order.meal_period
        )

        different_user_id = '-LG__88sozO1OGrqda2z_dghdsvnsdhgsd'

        result = self.repo.user_has_order(
            different_user_id, date_booked=order.date_booked_for.strftime('%Y-%m-%d'), meal_period=new_order.meal_period
        )

        self.assertEqual(result, False)
