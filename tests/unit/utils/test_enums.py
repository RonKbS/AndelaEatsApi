from tests.base_test_case import BaseTestCase

from app.utils.enums import (MealTypes, Channels, MealPeriods, OrderStatus, RatingType, ActionType, FaqCategoryType,
                             MealSessionNames)

class TestEnums(BaseTestCase):

    def setUp(self):
        self.BaseSetUp()

    def tearDown(self):
        self.BaseTearDown()

    def test_meal_types_enums(self):
        values = ['main', 'side', 'protein']

        for value in values:
            result = MealTypes.has_value(value)

            self.assertTrue(result)

    def test_channels_enums(self):
        values = ['web', 'slack', 'mobile']

        for value in values:
            result = Channels.has_value(value)

            self.assertTrue(result)

    def test_meal_periods_enums(self):
        values = ['lunch', 'breakfast']

        for value in values:
            result = MealPeriods.has_value(value)

            self.assertTrue(result)

    def test_order_status_enums(self):
        values = ['booked', 'collected', 'cancelled']

        for value in values:
            result = OrderStatus.has_value(value)

            self.assertTrue(result)

    def test_rating_tyoe_enums(self):
        values = ['meal', 'order', 'engagement']

        for value in values:
            result = RatingType.has_value(value)

            self.assertTrue(result)

    def test_action_type_enums(self):
        values = ['create', 'update', 'delete']

        for value in values:
            result = ActionType.has_value(value)

            self.assertTrue(result)

    def test_faq_category_enums(self):
        values = ['user_faq', 'admin_faq']

        for value in values:
            result = FaqCategoryType.has_value(value)

            self.assertTrue(result)

    def test_meal_session_names_enums(self):
        values = ['breakfast', 'lunch']

        for value in values:
            result = MealSessionNames.has_value(value)

            self.assertTrue(result)




