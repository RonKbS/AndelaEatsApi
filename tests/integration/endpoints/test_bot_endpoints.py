from datetime import datetime
from unittest.mock import patch, Mock

from app.controllers import BotController
from factories import LocationFactory, MenuFactory, MealItemFactory, \
    VendorEngagementFactory, OrderFactory
from tests.base_test_case import BaseTestCase
from tests.mock import (
    center_selected,
    date_selected,
    period_selected,
    action_selected_menu,
    action_selected_order,
    menu_list_rate,
    meal_to_book,
    final_selection,
    rating_selector,
    submit_rating
)


class TestBotEndpoints(BaseTestCase):

    def setUp(self):
        self.BaseSetUp()
        self.bot_controller = BotController(self.request_context)
        self.menu_factory = MenuFactory

    def tearDown(self):
        self.BaseTearDown()

    def test_bot(self):
        with self.app.app_context():
            response = self.client().post(self.make_url(f'/bot/'), headers=self.headers())

            response_json = self.decode_from_json_string(response.data.decode('utf-8'))
            self.assert200(response)
            self.assertEqual(response_json['text'], 'Welcome To Andela Eats')
            self.assertEqual(type(response_json['attachments']), list)
            self.assertEqual(response_json['attachments'][0]['callback_id'], 'center_selector')
            self.assertEqual(response_json['attachments'][0]['attachment_type'], 'default')

    @patch('app.controllers.bot_controller.LocationRepo')
    @patch('app.controllers.bot_controller.json.loads')
    @patch('app.controllers.bot_controller.BotController.get_menu_start_end_on')
    def test_interactions_after_selecting_location(self, mock_get_menu_start_end_on, mock_json_loads, mock_locationrepo_get):
        mock_json_loads.return_value = center_selected
        mock_get_menu_start_end_on.return_value = (datetime(2019, 2, 15), datetime(2019, 2, 15))
        mock_locationrepo_get.get.return_value = LocationFactory.create(id=1)

        response = self.client().post(self.make_url(f'/bot/interactions/'), headers=self.headers())
        response_json = self.decode_from_json_string(response.data.decode('utf-8'))

        self.assert200(response)
        self.assertEqual(response_json['type'], 'interactive_message')
        self.assertEqual(type(response_json['actions']), list)

    @patch('app.controllers.bot_controller.json.loads')
    def test_interactions_after_selecting_date(self, mock_json_loads):
        mock_json_loads.return_value = date_selected

        response = self.client().post(self.make_url(f'/bot/interactions/'), headers=self.headers())
        response_json = self.decode_from_json_string(response.data.decode('utf-8'))

        self.assert200(response)
        self.assertEqual(response_json['type'], 'interactive_message')
        self.assertEqual(type(response_json['actions']), list)

    @patch('app.controllers.bot_controller.json.loads')
    def test_interactions_after_selecting_period(self, mock_json_loads):
        mock_json_loads.return_value = period_selected

        response = self.client().post(self.make_url(f'/bot/interactions/'), headers=self.headers())
        response_json = self.decode_from_json_string(response.data.decode('utf-8'))

        self.assert200(response)
        self.assertEqual(response_json['type'], 'interactive_message')
        self.assertEqual(type(response_json['actions']), list)

    @patch('app.controllers.bot_controller.json.loads')
    def test_interactions_after_selecting_action_menu_list(self, mock_json_loads):
        mock_json_loads.return_value = action_selected_menu

        response = self.client().post(self.make_url(f'/bot/interactions/'), headers=self.headers())
        response_json = self.decode_from_json_string(response.data.decode('utf-8'))

        self.assert200(response)
        self.assertEqual(response_json['type'], 'interactive_message')
        self.assertEqual(type(response_json['actions']), list)

    @patch('app.repositories.MenuRepo.get_unpaginated')
    @patch('app.controllers.bot_controller.json.loads')
    def test_interactions_after_selecting_action_menu_list_with_menus(self, mock_json_loads, mock_menu_repo):
        mock_json_loads.return_value = action_selected_menu
        location = LocationFactory()
        side_meal_item = MealItemFactory(location=location, meal_type="side")
        side_meal_item.save()
        protein_meal_item = MealItemFactory(location=location, meal_type="protein")
        menu = MenuFactory.create(
            side_items=str(side_meal_item.id),
            protein_items=str(protein_meal_item.id)
        )
        mock_menu_repo.return_value = [menu]
        response = self.client().post(self.make_url(f'/bot/interactions/'), headers=self.headers())
        response_json = self.decode_from_json_string(response.data.decode('utf-8'))

        self.assert200(response)
        self.assertEqual(response_json['type'], 'interactive_message')
        self.assertEqual(type(response_json['actions']), list)

    @patch('app.controllers.bot_controller.json.loads')
    def test_interactions_after_selecting_action_order(self, mock_json_loads):
        mock_json_loads.return_value = action_selected_order

        response = self.client().post(self.make_url(f'/bot/interactions/'), headers=self.headers())
        response_json = self.decode_from_json_string(response.data.decode('utf-8'))

        self.assert200(response)
        self.assertEqual(response_json['type'], 'interactive_message')
        self.assertEqual(type(response_json['actions']), list)

    @patch('app.utils.slackhelper.SlackHelper.dialog')
    @patch('app.repositories.MenuRepo.get_unpaginated')
    @patch('app.controllers.bot_controller.json.loads')
    def test_interactions_after_selecting_action_order_with_menus(self, mock_json_loads, mock_menu_repo, mock_api):
        mock_json_loads.return_value = action_selected_order
        mock_menu_repo.return_value = [self.menu_factory.create()]
        mock_api.return_value = { 'ok': True }

        response = self.client().post(self.make_url(f'/bot/interactions/'), headers=self.headers())
        response_json = self.decode_from_json_string(response.data.decode('utf-8'))

        self.assert200(response)
        self.assertEqual(response_json['type'], 'interactive_message')
        self.assertEqual(type(response_json['actions']), list)

    @patch('app.controllers.bot_controller.json.loads')
    def test_interactions_after_selecting_menulist_rate(self, mock_json_loads):
        mock_json_loads.return_value = menu_list_rate

        response = self.client().post(self.make_url(f'/bot/interactions/'), headers=self.headers())
        response_json = self.decode_from_json_string(response.data.decode('utf-8'))

        self.assert200(response)
        self.assertEqual(response_json['type'], 'interactive_message')
        self.assertEqual(type(response_json['actions']), list)

    @patch('app.repositories.MenuRepo.get_unpaginated')
    @patch('app.controllers.bot_controller.json.loads')
    def test_interactions_after_selecting_menulist_rate_with_menus(self, mock_json_loads, mock_menu_repo):
        mock_json_loads.return_value = menu_list_rate
        mock_menu_repo.return_value = [self.menu_factory.create()]

        response = self.client().post(self.make_url(f'/bot/interactions/'), headers=self.headers())
        response_json = self.decode_from_json_string(response.data.decode('utf-8'))

        self.assert200(response)
        self.assertEqual(response_json['type'], 'interactive_message')
        self.assertEqual(type(response_json['actions']), list)

    @patch('app.utils.slackhelper.SlackHelper.dialog')
    @patch('app.controllers.bot_controller.requests.post')
    @patch('app.repositories.MenuRepo.get')
    @patch('app.services.andela.AndelaService.get_user_by_email_or_id')
    @patch('app.repositories.OrderRepo.user_has_order')
    @patch('app.utils.slackhelper.SlackHelper.user_info')
    @patch('app.controllers.bot_controller.json.loads')
    def test_interactions_after_selecting_menu_to_order_invalid(self, mock_json_loads, mock_user_info, mock_order_repo, mock_andela_service, mock_menu_repo, mock_post, mock_api_call):
        mock_json_loads.return_value = meal_to_book
        mock_user_info.return_value = {'user': {'profile': {'email': 'victor.adukwu@andela.com'}}}
        mock_andela_service.return_value = {'id': 'victor_adukwu_andela_com'}
        mock_menu_repo.return_value = Mock(self.menu_factory.create())
        mock_order_repo.return_value = True
        mock_api_call.return_value = { "ok": True }

        response = self.client().post(self.make_url(f'/bot/interactions/'), headers=self.headers())
        mock_post.assert_called_once()

        self.assert400(response)

    @patch('app.utils.slackhelper.SlackHelper.dialog')
    @patch('app.repositories.MealItemRepo.get_meal_items_by_ids')
    @patch('app.repositories.MenuRepo.get')
    @patch('app.services.andela.AndelaService.get_user_by_email_or_id')
    @patch('app.repositories.OrderRepo.user_has_order')
    @patch('app.utils.slackhelper.SlackHelper.user_info')
    @patch('app.controllers.bot_controller.json.loads')
    def test_interactions_after_selecting_menu_to_order_valid(self, mock_json_loads, mock_user_info, mock_order_repo,
                                                        mock_andela_service, mock_menu_repo, mock_meal_items, mock_api_call):
        mock_json_loads.return_value = meal_to_book
        mock_user_info.return_value = {'user': {'profile': {'email': 'victor.adukwu@andela.com'}}}
        mock_andela_service.return_value = {'id': 'victor_adukwu_andela_com'}
        mock_menu_repo.return_value = self.menu_factory.create(allowed_side=1, allowed_protein=1)
        mock_meal_items.return_values = MealItemFactory.create()
        mock_order_repo.return_value = False
        mock_api_call.return_value = { "ok": True}

        response = self.client().post(self.make_url(f'/bot/interactions/'), headers=self.headers())

        self.assert200(response)

    @patch('app.controllers.bot_controller.requests.post')
    @patch('app.repositories.MealItemRepo.get_meal_items_by_ids')
    @patch('app.repositories.MenuRepo.get')
    @patch('app.services.andela.AndelaService.get_user_by_email_or_id')
    @patch('app.repositories.OrderRepo.user_has_order')
    @patch('app.utils.slackhelper.SlackHelper.user_info')
    @patch('app.controllers.bot_controller.json.loads')
    def test_interactions_after_final_meal_selection(self, mock_json_loads, mock_user_info, mock_order_repo, mock_andela_service, mock_menu_repo, mock_meal_items, mock_post):
        location = LocationFactory.create()
        location.save()
        menu = MenuFactory.create()
        menu.save()

        final_selection['state'] = f'{menu.id}_breakfast_2019-02-19_order_{location.id}_1'
        mock_json_loads.return_value = final_selection
        mock_user_info.return_value = {'user': {'profile': {'email': 'victor.adukwu@andela.com'}}}
        mock_andela_service.return_value = {'id': 'victor_adukwu_andela_com', 'email': 'victor.adukwu@andela.com'}

        mock_menu_repo.return_value = menu

        order = OrderFactory.create(menu=menu, location=location)

        mock_order_repo.return_value = order
        mock_meal_items.return_values = MealItemFactory.create()

        response = self.client().post(self.make_url(f'/bot/interactions/'), headers=self.headers())
        response_json = self.decode_from_json_string(response.data.decode('utf-8'))

        self.assert200(response)
        self.assertEqual(response_json['type'], 'dialog_submission')
        mock_post.assert_called_once()

    @patch('app.utils.slackhelper.SlackHelper.dialog')
    @patch('app.repositories.MenuRepo.get')
    @patch('app.services.andela.AndelaService.get_user_by_email_or_id')
    @patch('app.utils.slackhelper.SlackHelper.user_info')
    @patch('app.controllers.bot_controller.json.loads')
    def test_interactions_after_selecting_menu_to_rate(self, mock_json_loads, mock_user_info,
                                                              mock_andela_service, mock_menu_repo, mock_api_call):
        mock_json_loads.return_value = rating_selector
        mock_user_info.return_value = {'user': {'profile': {'email': 'victor.adukwu@andela.com'}}}
        mock_andela_service.return_value = {'id': 'victor_adukwu_andela_com'}
        mock_menu_repo.return_value = self.menu_factory.create(allowed_side=1, allowed_protein=1)
        mock_api_call.return_value = {"ok": True}

        response = self.client().post(self.make_url(f'/bot/interactions/'), headers=self.headers())

        self.assert200(response)

    @patch('app.controllers.bot_controller.requests.post')
    @patch('app.repositories.VendorEngagementRepo.get')
    @patch('app.repositories.MenuRepo.get')
    @patch('app.services.andela.AndelaService.get_user_by_email_or_id')
    @patch('app.utils.slackhelper.SlackHelper.user_info')
    @patch('app.controllers.bot_controller.json.loads')
    def test_interactions_after_final_meal_selection_valid(
        self,
        mock_json_loads,
        mock_user_info,
        mock_andela_service,
        mock_menu_repo,
        mock_engagement_repo,
        mock_post
    ):
        location = LocationFactory.create()
        location.save()
        meal = MealItemFactory.create()
        meal.save()
        submit_rating['state'] = f'{meal.id}_breakfast_2019-02-20_rate_{location.id}_1'

        mock_json_loads.return_value = submit_rating
        mock_user_info.return_value = {'user': {'profile': {'email': 'victor.adukwu@andela.com'}}}
        mock_andela_service.return_value = {'id': 'victor_adukwu_andela_com'}
        engagement = VendorEngagementFactory.create()
        engagement.save()
        mock_engagement_repo.return_value = engagement
        mock_menu_repo.return_value = self	.menu_factory.create()
        response = self.client().post(self.make_url(f'/bot/interactions/'), headers=self.headers())
        response_json = self.decode_from_json_string(response.data.decode('utf-8'))
        mock_post.assert_called_once()
        self.assert200(response)
        self.assertEqual(response_json['type'], 'dialog_submission')

    @patch('app.controllers.bot_controller.requests.post')
    @patch('app.repositories.VendorRatingRepo.new_rating')
    @patch('app.repositories.VendorEngagementRepo.get')
    @patch('app.repositories.MenuRepo.get')
    @patch('app.services.andela.AndelaService.get_user_by_email_or_id')
    @patch('app.utils.slackhelper.SlackHelper.user_info')
    @patch('app.controllers.bot_controller.json.loads')
    def test_interactions_after_final_meal_selection_invalid(self, mock_json_loads, mock_user_info,
                                                     mock_andela_service, mock_menu_repo, mock_engagement_repo,
                                                     rating_repo, mock_post):
        mock_json_loads.return_value = submit_rating
        mock_user_info.return_value = {'user': {'profile': {'email': 'victor.adukwu@andela.com'}}}
        mock_andela_service.return_value = {'id': 'victor_adukwu_andela_com'}
        mock_engagement_repo.return_value = VendorEngagementFactory.create()
        mock_menu_repo.return_value = self.menu_factory.create()
        rating_repo.return_value = None

        response = self.client().post(self.make_url(f'/bot/interactions/'), headers=self.headers())
        response_json = self.decode_from_json_string(response.data.decode('utf-8'))
        mock_post.assert_called_once()
        self.assert200(response)
        self.assertEqual(response_json['type'], 'dialog_submission')

    @patch('app.controllers.bot_controller.current_time_by_zone')
    def test_get_menu_start_end_on_before_3pm_sunday(self, mock_get):

        mock_get.return_value = datetime.strptime('2019-02-10', '%Y-%m-%d')

        result = self.bot_controller.get_menu_start_end_on(LocationFactory.build())

        self.assertEqual(type(result), tuple)
        self.assertEqual(result[0], datetime(2019, 2, 11, 0, 0))
        self.assertEqual(result[1], datetime(2019, 2, 15, 0, 0))

    @patch('app.controllers.bot_controller.current_time_by_zone')
    def test_get_menu_start_end_on_after_3pm_sunday(self, mock_get):
        mock_get.return_value = datetime.strptime('2019-02-10 15:01', '%Y-%m-%d %H:%M')

        result = self.bot_controller.get_menu_start_end_on(LocationFactory.build())

        self.assertEqual(type(result), tuple)
        self.assertEqual(result[0].date(), datetime(2019, 2, 12).date())
        self.assertEqual(result[1].date(), datetime(2019, 2, 15).date())

    @patch('app.controllers.bot_controller.current_time_by_zone')
    def test_get_menu_start_end_on_before_3pm_monday(self, mock_get):
        mock_get.return_value = datetime.strptime('2019-02-11', '%Y-%m-%d')

        result = self.bot_controller.get_menu_start_end_on(LocationFactory.build())


        self.assertEqual(type(result), tuple)
        self.assertEqual(result[0], datetime(2019, 2, 12, 0, 0))
        self.assertEqual(result[1], datetime(2019, 2, 15, 0, 0))

    @patch('app.controllers.bot_controller.current_time_by_zone')
    def test_get_menu_start_end_on_after_3pm_monday(self, mock_get):
        mock_get.return_value = datetime.strptime('2019-02-11 15:01', '%Y-%m-%d %H:%M')

        result = self.bot_controller.get_menu_start_end_on(LocationFactory.build())

        self.assertEqual(type(result), tuple)
        self.assertEqual(result[0].date(), datetime(2019, 2, 13).date())
        self.assertEqual(result[1].date(), datetime(2019, 2, 15).date())

    @patch('app.controllers.bot_controller.current_time_by_zone')
    def test_get_menu_start_end_on_before_3pm_tuesday(self, mock_get):
        mock_get.return_value = datetime.strptime('2019-02-12', '%Y-%m-%d')

        result = self.bot_controller.get_menu_start_end_on(LocationFactory.build())

        self.assertEqual(type(result), tuple)
        self.assertEqual(result[0], datetime(2019, 2, 13, 0, 0))
        self.assertEqual(result[1], datetime(2019, 2, 15, 0, 0))

    @patch('app.controllers.bot_controller.current_time_by_zone')
    def test_get_menu_start_end_on_after_3pm_tuesday(self, mock_get):
        mock_get.return_value = datetime.strptime('2019-02-12 15:01', '%Y-%m-%d %H:%M')

        result = self.bot_controller.get_menu_start_end_on(LocationFactory.build())

        self.assertEqual(type(result), tuple)
        self.assertEqual(result[0].date(), datetime(2019, 2, 14).date())
        self.assertEqual(result[1].date(), datetime(2019, 2, 15).date())

    @patch('app.controllers.bot_controller.current_time_by_zone')
    def test_get_menu_start_end_on_before_3pm_wednesday(self, mock_get):
        mock_get.return_value = datetime.strptime('2019-02-13', '%Y-%m-%d')

        result = self.bot_controller.get_menu_start_end_on(LocationFactory.build())

        self.assertEqual(type(result), tuple)
        self.assertEqual(result[0], datetime(2019, 2, 14, 0, 0))
        self.assertEqual(result[1], datetime(2019, 2, 15, 0, 0))

    @patch('app.controllers.bot_controller.current_time_by_zone')
    def test_get_menu_start_end_on_after_3pm_wednesday(self, mock_get):
        mock_get.return_value = datetime.strptime('2019-02-13 15:01', '%Y-%m-%d %H:%M')

        result = self.bot_controller.get_menu_start_end_on(LocationFactory.build())

        self.assertEqual(type(result), tuple)
        self.assertEqual(result[0].date(), datetime(2019, 2, 15).date())
        self.assertEqual(result[1].date(), datetime(2019, 2, 15).date())

    @patch('app.controllers.bot_controller.current_time_by_zone')
    def test_get_menu_start_end_on_before_3pm_thursday(self, mock_get):
        mock_get.return_value = datetime.strptime('2019-02-14', '%Y-%m-%d')

        result = self.bot_controller.get_menu_start_end_on(LocationFactory.build())

        self.assertEqual(type(result), tuple)
        self.assertEqual(result[0], datetime(2019, 2, 15, 0, 0))
        self.assertEqual(result[1], datetime(2019, 2, 15, 0, 0))

    @patch('app.controllers.bot_controller.current_time_by_zone')
    def test_get_menu_start_end_on_after_3pm_thursday(self, mock_get):
        mock_get.return_value = datetime.strptime('2019-02-14 15:01', '%Y-%m-%d %H:%M')

        result = self.bot_controller.get_menu_start_end_on(LocationFactory.build())

        self.assertEqual(type(result), tuple)
        self.assertEqual(result[0].date(), datetime(2019, 2, 18).date())
        self.assertEqual(result[1].date(), datetime(2019, 2, 18).date())

    @patch('app.controllers.bot_controller.current_time_by_zone')
    def test_get_menu_start_end_on_friday(self, mock_get):
        mock_get.return_value = datetime.strptime('2019-02-15', '%Y-%m-%d')

        result = self.bot_controller.get_menu_start_end_on(LocationFactory.build())

        self.assertEqual(type(result), tuple)
        self.assertEqual(result[0], datetime(2019, 2, 18, 0, 0))
        self.assertEqual(result[1], datetime(2019, 2, 22, 0, 0))

    @patch('app.controllers.bot_controller.current_time_by_zone')
    def test_get_menu_start_end_on_saturday(self, mock_get):
        mock_get.return_value = datetime.strptime('2019-02-16 15:01', '%Y-%m-%d %H:%M')

        result = self.bot_controller.get_menu_start_end_on(LocationFactory.build())

        self.assertEqual(type(result), tuple)
        self.assertEqual(result[0].date(), datetime(2019, 2, 18).date())
        self.assertEqual(result[1].date(), datetime(2019, 2, 22).date())