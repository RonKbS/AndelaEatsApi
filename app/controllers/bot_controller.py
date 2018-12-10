import json
import requests

from app.services.andela import AndelaService
from app.utils import daterange, current_time_by_zone
from config import get_env
from flask import make_response
from datetime import datetime, timedelta
from app.repositories import LocationRepo, MenuRepo, MealItemRepo, OrderRepo
from app.utils.slackhelper import SlackHelper
from app.controllers.base_controller import BaseController


class BotController(BaseController):
	def __init__(self, request):
		BaseController.__init__(self, request)
		self.slackhelper = SlackHelper()
		self.menu_repo = MenuRepo()
		self.meal_repo = MealItemRepo()
		self.andela_service = AndelaService()

	def bot(self):
		locations = LocationRepo().fetch_all()
		location_buttons = [{'name': 'location', 'text': f'{location.name}', 'type': "button", 'value': location.id} for location in locations.items ]
		
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
				
				self.create_dialog(dialog_elem=dialog_element, trigger_id=trigger_id, title='Select Date', callback_id='date_selector')
			
			if payload['callback_id'] == 'final_selection':
				
				state = payload['state'].split('_')
				menu_id = state[0]
				meal_period = state[1]
				date_booked_for = state[2]
				location_id = state[3]
				submitted_values = payload['submission']
				meal_items = [int(v) for k, v in submitted_values.items()]
				meal_items.append(MenuRepo().get(menu_id).main_meal_id)
				meal_items = [meal for meal in MealItemRepo().get_meal_items_by_ids(meal_items)]
				channel = 'slack'
				
				# Retrieve User Object
				user = self.andela_service.get_user_by_email_or_id(slack_user_email)
				user_id = user['id']
				order = OrderRepo().create_order(
					user_id=user_id, date_booked_for=date_booked_for, meal_items=meal_items, location_id=location_id, menu_id=menu_id,
					channel=channel, meal_period=meal_period)
	
				if order:
					slack_data = {'text': 'Booking Confirmed!'}
					requests.post(webhook_url, data=json.dumps(slack_data), headers={'Content-Type': 'application/json'})
				else:
					slack_data = {'text': 'Booking Failed. Please Retry'}
					requests.post(webhook_url, data=json.dumps(slack_data), headers={'Content-Type': 'application/json'})
					
			return make_response('', 200)
		
		if payload['type'] == 'interactive_message' and payload['callback_id'] == 'center_selector':
			location_id = payload['actions'][0]['value']
			
			location = LocationRepo().get(location_id)
			menu_start_end_on = BotController.get_menu_start_end_on(location)
			start_on = menu_start_end_on[0]
			end_on = menu_start_end_on[1]
			
			date_buttons = [{
				'name': 'selected_date', 'type': 'button', 'text': '{}, {}'.format(day.strftime('%a'), day.strftime('%b %-d')),
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
				{'name': 'meal_period', 'type': 'button', 'text': 'Breakfast', 'value': 'breakfast_{}'.format(payload_action_value)},
				{'name': 'meal_period', 'type': 'button', 'text': 'Lunch', 'value': 'lunch_{}'.format(payload_action_value)}
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
			payload_action_value = payload['actions'][0]['value']
			
			meal_period = payload_action_value.split('_')[0]
			selected_date = payload_action_value.split('_')[1]
			location_id = payload_action_value.split('_')[2]
			
			menus = self.menu_repo.get_unpaginated(date=selected_date, meal_period=meal_period, is_deleted=False)
			
			if len(menus) == 0:
				# 	No Menu for provided date
				return self.handle_response(slack_response={'text': f'Sorry No Menu found for Date: {selected_date}, Meal Period: {meal_period}'})
			
			meal_buttons = [
				{'name': 'main_meal', 'type': 'button', 'text': f'{menu.main_meal.name}', 'value': f'{menu.id}_{payload_action_value}'}
				for menu in menus
			]

			request_buttons = [
				{
					"text": "",
					"callback_id": "main_meal_selector",
					"color": "#3AA3E3",
					"attachment_type": "default",
					"actions": meal_buttons
				}
			]

			return self.handle_response(slack_response={'text': 'Select Main Meal', 'attachments': request_buttons})
		
		if payload['type'] == 'interactive_message' and payload['callback_id'] == 'main_meal_selector':
			trigger_id = payload['trigger_id']
			
			payload_action_value = payload['actions'][0]['value']
			menu_id = payload_action_value.split('_')[0]
			meal_period = payload_action_value.split('_')[1]
			selected_date = payload_action_value.split('_')[2]
			location_id = payload_action_value.split('_')[3]
			
			menu = self.menu_repo.get(menu_id)
			side_items_list = menu.side_items.split(',')
			protein_items_list = menu.protein_items.split(',')
			
			side_items = self.meal_repo.get_meal_items_by_ids(side_items_list)
			protein_items = self.meal_repo.get_meal_items_by_ids(protein_items_list)
			
			request_dialog_element = []
			
			for i in range(1, menu.allowed_side+1):
				request_dialog_element.append({
					'label': f'Select Side {i}',
					'type': 'select',
					'name': f'side_{i}',
					'options': [{'label': f'{side.name}', 'value': f'{side.id}'} for side in side_items]
				})
				
			for i in range(1, menu.allowed_protein+1):
				request_dialog_element.append({
					'label': f'Select Protein {i}',
					'type': 'select',
					'name': f'protein_{i}',
					'options': [{'label': f'{protein.name}', 'value': f'{protein.id}'} for protein in protein_items]
				})
				
			state = f'{payload_action_value}'
			self.create_dialog(dialog_elem=request_dialog_element, trigger_id=trigger_id, title='Select Protein & Sides', callback_id='final_selection', state=state)
			
			return self.handle_response(slack_response={'text': 'Select Meal Protein and Sides'})
	
	def create_dialog(self, dialog_elem, trigger_id, title, callback_id, state=None):
		dialog = {
			"title": title,
			"submit_label": "Submit",
			"callback_id": callback_id,
			"notify_on_cancel": True,
			"state":state,
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
