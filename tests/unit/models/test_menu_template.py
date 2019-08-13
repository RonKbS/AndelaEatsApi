from app.models import Activity, MenuTemplate, MenuTemplateItem
from factories import LocationFactory, MealItemFactory
from factories.menu_template_factory import MenuTemplateWeekDayFactory
from tests.base_test_case import BaseTestCase


class TestMenuTemplate(BaseTestCase):

    def setUp(self):
        self.BaseSetUp()
        self.menu_template = MenuTemplate(
            name='New Menu Template',
            location=LocationFactory(),
            meal_period='lunch',
            description="somehting about it"
        )
        self.menu_template.save()

    def tearDown(self):
        self.BaseTearDown()

    def test_create_on_menu_template_model(self):
        self.assertNotEquals(self.menu_template.id, None)

    def test_create_on_menu_template_model_gets_logged(self):
        activity = [
            activity.action_details for activity in Activity.query.all()]
        self.assertTrue("New Menu Template" in activity[-1])

    def test_updating_menu_template_gets_logged(self):
        menu_template = MenuTemplate.query.get(self.menu_template.id)
        menu_template.name = "New Template name"
        menu_template.save()
        activity = [
            activity.action_details for activity in Activity.query.all()]
        self.assertTrue("New Template name" in activity[-1])


class TestMenuTemplateItem(BaseTestCase):

    def setUp(self):
        self.BaseSetUp()
        self.menu_template_item = MenuTemplateItem(
            main_meal=MealItemFactory(),
            side_items=[MealItemFactory()],
            protein_items=[MealItemFactory()],
            day=MenuTemplateWeekDayFactory(),
            allowed_protein=1
        )
        self.menu_template_item.save()

    def tearDown(self):
        self.BaseTearDown()

    def test_create_on_menu_template_item_model(self):
        self.assertNotEquals(self.menu_template_item.id, None)

    def test_hard_delete_a_menu_template_item_model(self):
        self.menu_template_item.side_items = []
        self.menu_template_item.protein_items = []
        self.menu_template_item.delete()
        self.assertEqual(MenuTemplateItem.query.get(
            self.menu_template_item.id), None)

    def test_create_on_menu_template_item_model_gets_logged(self):
        activity = [
            activity.action_details for activity in Activity.query.all()]
        self.assertTrue("MenuTemplateItem" in activity[-1])

    def test_updating_menu_template_item_gets_logged(self):
        menu_template_item = MenuTemplateItem.query.get(
            self.menu_template_item.id)
        menu_template_item.allowed_protein = 2
        menu_template_item.save()
        activity = [
            activity.action_details for activity in Activity.query.all()]
        self.assertTrue("'allowed_protein': 1" in activity[-1])
