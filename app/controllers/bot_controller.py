import json
import requests

from app.services.andela import AndelaService
from app.utils import daterange, current_time_by_zone
from app.utils.enums import RatingType
from datetime import datetime
from flask import make_response
from datetime import timedelta
from app.repositories import LocationRepo, MenuRepo, MealItemRepo, OrderRepo, VendorEngagementRepo, VendorRatingRepo
from app.utils.slackhelper import SlackHelper
from app.controllers.base_controller import BaseController


class BotController(BaseController):
    def __init__(self, request):
        BaseController.__init__(self, request)
        self.slackhelper = SlackHelper()
        self.menu_repo = MenuRepo()
        self.meal_repo = MealItemRepo()
        self.engagement_repo = VendorEngagementRepo()
        self.andela_service = AndelaService()
        self.vendor_rating_repo = VendorRatingRepo()

    def bot(self):
        locations = LocationRepo().fetch_all()
        location_buttons = [{'name': 'location', 'text': f'{location.name}', 'type': "button", 'value': location.id} for
                            location in locations.items]

        request_buttons = [
            {
                "text": "",
                "callback_id": "center_selector",
                "color": "#3AA3E3",
                "attachment_type": "default",
                "actions": location_buttons
            }
        ]

        return self.handle_response(slack_response={'text': f'Welcome To Andela Eats', 'attachments': request_buttons})

    def interactions(self):
        request_payload, trigger_id = self.post_params('payload', 'trigger_id')
        payload = json.loads(request_payload)

        webhook_url = payload["response_url"]
        slack_id = payload['user']['id']

        if payload['type'] == 'dialog_submission':
            slack_user_info = self.slackhelper.user_info(slack_id)
            slack_user_email = slack_user_info['user']['profile']['email']
            slack_user_fname = slack_user_info['user']['profile']['first_name']
            slack_user_lname = slack_user_info['user']['profile']['last_name']

            if payload['callback_id'] == 'location_period_selector':
                self.post_params('payload', 'trigger_id')

                location_id = int(payload['submission']['location'])
                meal_period = payload['submission']['meal_period']

                location = LocationRepo().get(location_id)
                menu_start_end_on = BotController.get_menu_start_end_on(location)
                start_on = menu_start_end_on[0]
                end_on = menu_start_end_on[1]

                date_options = [{
                    'label': '{}, {}'.format(day.strftime('%a'), day.strftime('%b %-d')),
                    'value': '{}_{}_{}'.format(day.strftime('%Y-%m-%d'), location.id, meal_period)} for day in
                    daterange(start_on, end_on)]

                dialog_element = [
                    {
                        "label": "Select Date",
                        "type": "select",
                        "name": "selected_date",
                        "options": date_options
                    },
                ]

                self.create_dialog(dialog_elem=dialog_element, trigger_id=trigger_id, title='Select Date',
                                   callback_id='date_selector')

            if payload['callback_id'] == 'final_selection':

                state = payload['state'].split('_')
                menu_id = state[0]
                meal_period = state[1]
                date_booked_for = state[2]
                location_id = state[4]
                submitted_values = payload['submission']
                meal_items = [int(v) for k, v in submitted_values.items()]
                meal_items.append(MenuRepo().get(menu_id).main_meal_id)
                meal_items = [meal for meal in MealItemRepo().get_meal_items_by_ids(meal_items)]
                channel = 'slack'

                # Retrieve User Object
                user = self.andela_service.get_user_by_email_or_id(slack_user_email)
                user_id = user['id']

                order = OrderRepo().create_order(
                    user_id=user_id, date_booked_for=date_booked_for, meal_items=meal_items, location_id=location_id,
                    menu_id=menu_id, channel=channel, meal_period=meal_period)

                if order:
                    slack_data = {'text': 'Booking Confirmed!'}
                    requests.post(webhook_url, data=json.dumps(slack_data),
                                  headers={'Content-Type': 'application/json'})
                else:
                    slack_data = {'text': 'Booking Failed. Please Retry'}
                    requests.post(webhook_url, data=json.dumps(slack_data),
                                  headers={'Content-Type': 'application/json'})

            if payload['callback_id'] == 'submit_rating':

                state = payload['state'].split('_')
                menu_id = state[0]
                menu = self.menu_repo.get(menu_id)
                service_date = menu.date
                rating_type = RatingType.meal
                type_id = menu.main_meal_id
                engagement_id = menu.vendor_engagement_id
                vendor_id = self.engagement_repo.get(engagement_id).vendor_id
                rating_value = payload['submission']['rating value']
                channel = 'slack'
                comment = payload['submission']['comment']

                # Retrieve User Object
                user = self.andela_service.get_user_by_email_or_id(slack_user_email)
                user_id = user['id']

                rating = self.vendor_rating_repo.new_rating(
                    vendor_id, user_id, rating_value, service_date, rating_type,
                    type_id, engagement_id, channel, comment, type_id
                )

                if rating:
                    slack_data = {'text': 'Rating Successful!'}
                    requests.post(webhook_url, data=json.dumps(slack_data),
                                  headers={'Content-Type': 'application/json'})
                else:
                    slack_data = {'text': 'Rating Failed. Please Retry'}
                    requests.post(webhook_url, data=json.dumps(slack_data),
                                  headers={'Content-Type': 'application/json'})

            return make_response('', 200)

        if payload['type'] == 'interactive_message' and payload['callback_id'] == 'center_selector':
            location_id = payload['actions'][0]['value']

            location = LocationRepo().get(location_id)
            menu_start_end_on = BotController.get_menu_start_end_on(location)
            start_on = menu_start_end_on[0]
            end_on = menu_start_end_on[1]

            date_buttons = [{
                'name': 'selected_date', 'type': 'button',
                'text': '{}, {}'.format(day.strftime('%a'), day.strftime('%b %-d')),
                'value': '{}_{}'.format(day.strftime('%Y-%m-%d'), location.id)} for day in daterange(start_on, end_on)]

            request_buttons = [
                {
                    "text": "",
                    "callback_id": "day_selector",
                    "color": "#3AA3E3",
                    "attachment_type": "default",
                    "actions": date_buttons
                }
            ]

            return self.handle_response(slack_response={'text': f'Select Date', 'attachments': request_buttons})

        if payload['type'] == 'interactive_message' and payload['callback_id'] == 'day_selector':
            payload_action_value = payload['actions'][0]['value']
            selected_date = payload_action_value.split('_')[0]
            location_id = payload_action_value.split('_')[1]

            period_buttons = [
                {'name': 'meal_period', 'type': 'button', 'text': 'Breakfast',
                 'value': 'breakfast_{}'.format(payload_action_value)},
                {'name': 'meal_period', 'type': 'button', 'text': 'Lunch',
                 'value': 'lunch_{}'.format(payload_action_value)}
            ]

            request_buttons = [
                {
                    "text": "",
                    "callback_id": "period_selector",
                    "color": "#3AA3E3",
                    "attachment_type": "default",
                    "actions": period_buttons
                }
            ]

            return self.handle_response(slack_response={'text': f'Select Meal Period', 'attachments': request_buttons})

        if payload['type'] == 'interactive_message' and payload['callback_id'] == 'period_selector':
            period = payload['actions'][0]['value'].split('_')[0]
            date = payload['actions'][0]['value'].split('_')[1]
            location_id = payload['actions'][0]['value'].split('_')[2]
            actions = {
                "attachments": [
                    {
                        "text": 'What do you want to do?',
                        "callback_id": "action_selector",
                        "color": "#3AA3E3",
                        "attachment_type": "default",
                        "actions": [
                            {
                                "name": "main meal",
                                "text": "View Menu List",
                                "type": "button",
                                "value": f'{period}_{date}_menu_{location_id}'
                            },
                            {
                                "name": "main meal",
                                "text": "Place order",
                                "type": "button",
                                "value": f'{period}_{date}_order_{location_id}'
                            }
                        ]
                    }
                ]
            }
            return self.handle_response(slack_response=actions)

        if payload['type'] == 'interactive_message' and payload['callback_id'] == 'action_selector':
            payload_action_value = payload['actions'][0]['value']
            if payload_action_value.split('_')[2] == 'menu':
                date = payload_action_value.split('_')[1]
                period = payload_action_value.split('_')[0]
                location_id = payload_action_value.split('_')[3]
                menus = self.menu_repo.get_unpaginated(date=date, meal_period=period,
                                                       is_deleted=False)
                if not menus:
                    #   No Menu for provided date
                    return self.handle_response(slack_response={
                        'text': f'Sorry No Menu found for Date: {date}, Meal Period: {period}'})
                text = ''

                for menu in menus:
                    side_items_list = menu.side_items.split(',')
                    protein_items_list = menu.protein_items.split(',')

                    main = self.meal_repo.get(menu.main_meal_id).name
                    sides = [side.name for side in self.meal_repo.get_meal_items_by_ids(side_items_list)]
                    proteins = [protein.name for protein in self.meal_repo.get_meal_items_by_ids(protein_items_list)]
                    menu_info = f'Main meal: *{main}*\n Side items: {", ".join(sides)}\nProtein items: {", ".join(proteins)}\n\n\n'
                    text += menu_info

                meals = {
                        "text": f'{period.upper()}',
                        "attachments": [
                    {
                        "text": text,
                        "callback_id": "after_menu_list",
                        "color": "#3AA3E3",
                        "attachment_type": "default",
                        "actions": [
                            {
                                "name": "main meal",
                                "text": "Rate meal",
                                "type": "button",
                                "value": f'{period}_{date}_rate_{location_id}_{location_id}'
                            },
                            {
                                "name": "main meal",
                                "text": "Place an order",
                                "type": "button",
                                "value": f'{period}_{date}_order_{location_id}_{location_id}'
                            }
                        ]}]}
                return self.handle_response(slack_response=meals)

        if (payload['type'] == 'interactive_message' and payload['callback_id'] == 'action_selector' and
            payload['actions'][0]['value'].split('_')[2] == 'order') or (payload['callback_id'] == 'after_menu_list' and payload['actions'][0]['value'].split('_')[2] == 'order'):

            payload_action_value = payload['actions'][0]['value']
            meal_period = payload_action_value.split('_')[0]
            selected_date = payload_action_value.split('_')[1]
            location_id = payload_action_value.split('_')[2]
            menus = self.menu_repo.get_unpaginated(date=selected_date, meal_period=meal_period,
                                                   is_deleted=False)
            if not menus:
                #   No Menu for provided date
                return self.handle_response(slack_response={
                    'text': f'Sorry No Menu found for Date: {selected_date}, Meal Period: {meal_period}'})

            meal_buttons = [
                {'name': 'main_meal', 'type': 'button', 'text': f'{menu.main_meal.name}',
                 'value': f'{menu.id}_{payload_action_value}'}
                for menu in menus
            ]

            request_buttons = [
                {
                    "text": "",
                    "callback_id": "meal_action_selector",
                    "color": "#3AA3E3",
                    "attachment_type": "default",
                    "actions": meal_buttons
                }
            ]

            return self.handle_response(
                slack_response={'text': 'Select Main Meal', 'attachments': request_buttons})

        if payload['type'] == 'interactive_message' and payload['callback_id'] == 'meal_action_selector':
            payload_action_value = payload['actions'][0]['value']
            if payload_action_value.find('order') > -1:
                menu_id = payload_action_value.split('_')[0]
                menu = self.menu_repo.get(menu_id)
                slack_id = payload['user']['id']
                slack_user_info = self.slackhelper.user_info(slack_id)
                slack_user_email = slack_user_info['user']['profile']['email']
                user = self.andela_service.get_user_by_email_or_id(slack_user_email)

                # check if user already has an order
                if OrderRepo().user_has_order(user['id'], menu.date.strftime('%Y-%m-%d'), menu.meal_period):
                    slack_data = {'text': 'You already have an order for this meal period.'}
                    requests.post(webhook_url, data=json.dumps(slack_data),
                                  headers={'Content-Type': 'application/json'})
                    return
                trigger_id = payload['trigger_id']

                side_items_list = menu.side_items.split(',')
                protein_items_list = menu.protein_items.split(',')

                side_items = self.meal_repo.get_meal_items_by_ids(side_items_list)
                protein_items = self.meal_repo.get_meal_items_by_ids(protein_items_list)

                request_dialog_element = []

                for i in range(1, menu.allowed_side + 1):
                    request_dialog_element.append({
                        'label': f'Select Side {i}',
                        'type': 'select',
                        'name': f'side_{i}',
                        'options': [{'label': f'{side.name}', 'value': f'{side.id}'} for side in side_items]
                    })

                for i in range(1, menu.allowed_protein + 1):
                    request_dialog_element.append({
                        'label': f'Select Protein {i}',
                        'type': 'select',
                        'name': f'protein_{i}',
                        'options': [{'label': f'{protein.name}', 'value': f'{protein.id}'} for protein in protein_items]
                    })

                state = f'{payload_action_value}'
                self.create_dialog(dialog_elem=request_dialog_element, trigger_id=trigger_id,
                                   title='Select Protein & Sides',
                                   callback_id='final_selection', state=state)

                return self.handle_response(slack_response={'text': 'Select Meal Protein and Sides'})

        if payload['callback_id'] == 'after_menu_list' and payload['actions'][0]['value'].split('_')[2] == 'rate':

            payload_action_value = payload['actions'][0]['value']
            meal_period = payload_action_value.split('_')[0]
            selected_date = payload_action_value.split('_')[1]
            location_id = payload_action_value.split('_')[2]
            menus = self.menu_repo.get_unpaginated(date=selected_date, meal_period=meal_period,
                                                   is_deleted=False)
            if not menus:
                #   No Menu for provided date
                return self.handle_response(slack_response={
                    'text': f'Sorry No Menu found for Date: {selected_date}, Meal Period: {meal_period}'})

            meal_buttons = [
                {'name': 'main_meal', 'type': 'button', 'text': f'{menu.main_meal.name}',
                 'value': f'{menu.id}_{payload_action_value}'}
                for menu in menus
            ]

            request_buttons = [
                {
                    "text": "",
                    "callback_id": "rating_selector",
                    "color": "#3AA3E3",
                    "attachment_type": "default",
                    "actions": meal_buttons
                }
            ]

            return self.handle_response(
                slack_response={'text': 'Select Main Meal', 'attachments': request_buttons})

        if payload['callback_id'] == 'rating_selector':

            menu_id = payload['actions'][0]['value'].split('_')[0]
            menu = self.menu_repo.get(menu_id)
            trigger_id = payload['trigger_id']
            main_meal = menu.main_meal_id

            request_dialog_element = [{
                'label': f'Rate meal: {self.meal_repo.get(main_meal).name}',
                'type': 'select',
                'name': 'rating value',
                'options': [{'label': f'{value}', 'value': f'{value}'} for value in range(1, 6)]
            },
                {
                    'label': 'Add a short comment',
                    'type': 'text',
                    'name': 'comment'

                }
            ]

            state = f'{payload["actions"][0]["value"]}'
            self.create_dialog(dialog_elem=request_dialog_element, trigger_id=trigger_id,
                               title='Rate a meal',
                               callback_id='submit_rating', state=state)

            return self.handle_response(slack_response={'text': 'Meal rating'})

    def create_dialog(self, dialog_elem, trigger_id, title, callback_id, state=None):
        dialog = {
            "title": title,
            "submit_label": "Submit",
            "callback_id": callback_id,
            "notify_on_cancel": True,
            "state": state,
            "elements": dialog_elem
        }
        return self.slackhelper.dialog(dialog=dialog, trigger_id=trigger_id)

    @staticmethod
    def get_menu_start_end_on(location):
        """This method takes a location id, and attempts to return a start date and an end date based on the conditions
        the application expects.

        Conditions:
            If current datetime is over 3PM , skip a day and return next days.
            If day is thursday and not yet 3PM, return only friday
            If current datetime is friday, saturday or sunday, return next week from monday till friday.
            If No conditions matches, return None for both dates.

        """
        start_on = end_on = None

        current_date = current_time_by_zone(location.zone)

        if current_date.strftime('%a') == 'Mon' and int(current_date.strftime('%H')) > 15:
            start_on = current_date + timedelta(days=2)
            end_on = start_on + timedelta(days=2)

        elif current_date.strftime('%a') == 'Tue' and int(current_date.strftime('%H')) > 15:
            start_on = current_date + timedelta(days=2)
            end_on = start_on + timedelta(days=1)

        elif current_date.strftime('%a') == 'Wed' and int(current_date.strftime('%H')) > 15:
            start_on = end_on = current_date + timedelta(days=2)

        elif current_date.strftime('%a') == 'Thu' and int(current_date.strftime('%H')) > 15:
            start_on = end_on = current_date + timedelta(days=4)

        else:

            start_on = current_date + timedelta(days=1)
            if current_date.strftime('%a') == 'Mon':
                end_on = start_on + timedelta(3)
            if current_date.strftime('%a') == 'Tue':
                end_on = start_on + timedelta(2)
            if current_date.strftime('%a') == 'Wed':
                end_on = start_on + timedelta(1)
            if current_date.strftime('%a') == 'Thu':
                end_on = start_on

            else:
                if current_date.strftime('%a') == 'Fri':
                    start_on = current_date + timedelta(days=3)
                    end_on = current_date + timedelta(days=7)

                if current_date.strftime('%a') == 'Sat':
                    start_on = current_date + timedelta(days=2)
                    end_on = current_date + timedelta(days=6)

                if current_date.strftime('%a') == 'Sun':
                    start_on = current_date + timedelta(days=1)
                    end_on = current_date + timedelta(days=5)

        return tuple((start_on, end_on))
