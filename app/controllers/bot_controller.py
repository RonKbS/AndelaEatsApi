import json
from datetime import timedelta, datetime

import requests
from flask import make_response

from app.controllers.base_controller import BaseController
from app.repositories import LocationRepo
from app.repositories import MealItemRepo
from app.repositories import MenuRepo
from app.repositories import OrderRepo
from app.repositories import VendorEngagementRepo
from app.repositories import VendorRatingRepo
from app.services.andela import AndelaService
from app.utils import daterange, current_time_by_zone
from app.utils.enums import RatingType
from app.utils.slackhelper import SlackHelper
from app.repositories.meal_session_repo import MealSessionRepo
from typing import List
from app.models.meal_item import MealItem
from app.factories.slack_response import SlackResponseFactory


class BotController(BaseController):
    def __init__(self, request):
        BaseController.__init__(self, request)
        self.slackhelper = SlackHelper()
        self.menu_repo = MenuRepo()
        self.meal_repo = MealItemRepo()
        self.engagement_repo = VendorEngagementRepo()
        self.andela_service = AndelaService()
        self.vendor_rating_repo = VendorRatingRepo()

    def _get_meal_items_by_ids(self, meal_item_ids: List) -> List[MealItem]:
        """
        Get meal items given a list of IDs.

        Args:
            meal_item_ids (list): List of IDs as strings.

        Returns:
            List[MealItem]: List of meal items.
        """
        return [meal_item.name for meal_item in
                self.meal_repo.get_meal_items_by_ids(meal_item_ids)]

    def bot(self):
        locations = LocationRepo().fetch_all()
        page = SlackResponseFactory().create_response('landing')\
                                     .build_page(locations=locations)

        return self.handle_response(slack_response=page)

    def handle_center_selection(self, payload):
        location = LocationRepo().get(payload['actions'][0]['value'])
        menu_start_end_on = BotController.get_menu_start_end_on(location)
        page = SlackResponseFactory().create_response('center_selection')\
                                     .build_page(location=location,
                                                 menu_period=menu_start_end_on)

        return self.handle_response(slack_response=page)
    
    def handle_day_selection(self, payload):
        payload_action_value = payload['actions'][0]['value']
        selected_date = payload_action_value.split('_')[0]
        location_id = payload_action_value.split('_')[1]
        day_meal_sessions = MealSessionRepo().get_by_date_location(
            meal_date=datetime.strptime(selected_date, '%Y-%m-%d').date(),
            location_id=location_id)

        page = SlackResponseFactory().create_response('day_selection')\
                                     .build_page(meals=day_meal_sessions,
                                                 payload=payload_action_value)

        return self.handle_response(slack_response=page)
    
    def handle_period_selection(self, payload):
        page = SlackResponseFactory().create_response('period_selection')\
                                     .build_page(payload=payload)

        return self.handle_response(slack_response=page)
    
    def handle_action_selection(self, payload):
        payload_action_value = payload['actions'][0]['value']
        if payload_action_value.split('_')[2] == 'menu':
            date = payload_action_value.split('_')[1]
            period = payload_action_value.split('_')[0]
            location_id = payload_action_value.split('_')[3]
            menus = self.menu_repo.get_unpaginated(date=date,
                                                   meal_period=period,
                                                   is_deleted=False)
            if not menus:
                #   No Menu for provided date
                back_buttons = [{'name': 'back',
                                 'text': 'Back',
                                 'type': 'button',
                                 'value': location_id}]
                request_buttons = [
                    {
                        "text": "",
                        "callback_id": "center_selector",
                        "color": "#3AA3E3",
                        "attachment_type": "default",
                        "actions": back_buttons
                    }
                ]
                return self.handle_response(slack_response={
                    'text': f'Sorry no menu found for date: {date}, '
                    f'meal period: {period}',
                    'attachments': request_buttons})
            text = ''

            for menu in menus:
                side_items_list = menu.side_items.split(',')
                protein_items_list = menu.protein_items.split(',')

                main = self.meal_repo.get(menu.main_meal_id).name
                sides = self._get_meal_items_by_ids(side_items_list)
                proteins = self._get_meal_items_by_ids(protein_items_list)
                menu_info = f'Main meal: *{main}*\n ' \
                    f'Side items: {", ".join(sides)}\n' \
                    f'Protein items: {", ".join(proteins)}\n\n\n'
                text += menu_info

            rate_value = f'{period}_{date}_rate_{location_id}_{location_id}'
            order_value = f'{period}_{date}_order_{location_id}_{location_id}'
            meals = {
                "text": f'{period.upper()}',
                "attachments": [{
                    "text": text,
                    "callback_id": "after_menu_list",
                    "color": "#3AA3E3",
                    "attachment_type": "default",
                    "actions": [
                        {
                            "name": "main meal",
                            "text": "Rate meal",
                            "type": "button",
                            "value": rate_value
                        },
                        {
                            "name": "main meal",
                            "text": "Place an order",
                            "type": "button",
                            "value": order_value
                        }
                    ]}]}
            return self.handle_response(slack_response=meals)
    
    def handle_placing_order(self, payload):
        payload_action_value = payload['actions'][0]['value']
        meal_period = payload_action_value.split('_')[0]
        selected_date = payload_action_value.split('_')[1]
        location_id = payload_action_value.split('_')[3]
        menus = self.menu_repo.get_unpaginated(date=selected_date,
                                               meal_period=meal_period,
                                               is_deleted=False)
        if not menus:
            #   No Menu for provided date
            back_buttons = [
                {'name': 'back',
                 'text': 'Back',
                 'type': 'button',
                 'value': location_id}
            ]

            request_buttons = [
                {
                    "text": "",
                    "callback_id": "center_selector",
                    "color": "#3AA3E3",
                    "attachment_type": "default",
                    "actions": back_buttons
                }
            ]
            return self.handle_response(slack_response={
                'text': f'Sorry No Menu found for Date: {selected_date},'
                f'Meal Period: {meal_period}',
                'attachments': request_buttons})

        meal_buttons = [
            {'name': 'main_meal',
             'type': 'button',
             'text': f'{menu.main_meal.name}',
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
    
    def handle_meal_action_selection(self, payload, webhook_url):
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
                return self.handle_response(status_code=400)
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
    
    def handle_rating(self, payload):
        payload_action_value = payload['actions'][0]['value']
        meal_period = payload_action_value.split('_')[0]
        selected_date = payload_action_value.split('_')[1]
        location_id = payload_action_value.split('_')[2]
        menus = self.menu_repo.get_unpaginated(date=selected_date, meal_period=meal_period,
                                                is_deleted=False)
        if not menus:
            #   No Menu for provided date
            back_buttons = [{'name': 'back', 'text': 'Back', 'type': "button", 'value': location_id}]

            request_buttons = [
                {
                    "text": "",
                    "callback_id": "center_selector",
                    "color": "#3AA3E3",
                    "attachment_type": "default",
                    "actions": back_buttons
                }
            ]
            return self.handle_response(slack_response={
                'text': f'Sorry No Menu found forr Date: {selected_date}, Meal Period: {meal_period}', 'attachments': request_buttons})

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
        
    def handle_rating_selection(self, payload):
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
    
    def handle_dialog_submission(self, payload, slack_id, webhook_url):
        slack_user_info = self.slackhelper.user_info(slack_id)
        slack_user_email = slack_user_info['user']['profile']['email']

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
                type_id, engagement_id, menu_id, channel, comment
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

    def interactions(self):
        request_payload, trigger_id = self.post_params('payload', 'trigger_id')
        payload = json.loads(request_payload)

        webhook_url = payload["response_url"]
        slack_id = payload['user']['id']

        if payload['type'] == 'dialog_submission':
            return self.handle_dialog_submission(payload, slack_id, webhook_url)

        if payload['type'] == 'interactive_message'\
                and payload['callback_id'] == 'center_selector':
            return self.handle_center_selection(payload)

        if payload['type'] == 'interactive_message'\
                and payload['callback_id'] == 'day_selector':
            return self.handle_day_selection(payload)

        if payload['type'] == 'interactive_message'\
                and payload['callback_id'] == 'period_selector':
            return self.handle_period_selection(payload)

        if (payload['type'] == 'interactive_message'and payload['callback_id'] == 'action_selector' and
            payload['actions'][0]['value'].split('_')[2] == 'order') or (payload['callback_id'] == 'after_menu_list' and payload['actions'][0]['value'].split('_')[2] == 'order'):
            return self.handle_placing_order(payload)

        if payload['type'] == 'interactive_message'\
                and payload['callback_id'] == 'action_selector':
            return self.handle_action_selection(payload)

        if payload['type'] == 'interactive_message' and payload['callback_id'] == 'meal_action_selector':
            return self.handle_meal_action_selection(payload, webhook_url)

        if payload['callback_id'] == 'after_menu_list' and payload['actions'][0]['value'].split('_')[2] == 'rate':
            return self.handle_rating(payload)

        if payload['callback_id'] == 'rating_selector':
            return self.handle_rating_selection(payload)

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

        if current_date.strftime('%a') == 'Mon' and int(current_date.strftime('%H')) >= 15:
            start_on = current_date + timedelta(days=2)
            end_on = start_on + timedelta(days=2)

        elif current_date.strftime('%a') == 'Tue' and int(current_date.strftime('%H')) >= 15:
            start_on = current_date + timedelta(days=2)
            end_on = start_on + timedelta(days=1)

        elif current_date.strftime('%a') == 'Wed' and int(current_date.strftime('%H')) >= 15:
            start_on = end_on = current_date + timedelta(days=2)

        elif current_date.strftime('%a') == 'Thu' and int(current_date.strftime('%H')) >= 15:
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
                    next_day = 1 if int(current_date.strftime('%H')) < 15 else 2
                    start_on = current_date + timedelta(days=next_day)
                    end_on = current_date + timedelta(days=5)

        return tuple((start_on, end_on))
