from app.controllers.base_controller import BaseController
from app.repositories import LocationRepo
from app.utils.slackhelper import SlackHelper
from datetime import datetime, timedelta
from app.utils import daterange
import json


class BotController(BaseController):
	def __init__(self, request):
		BaseController.__init__(self, request)
		self.slackhelper = SlackHelper()

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
			
		return self.handle_response(slack_response={'text': f'Select Center', 'attachments': request_buttons})

	def interactions(self):
		request_payload, = self.post_params('payload')
		payload = json.loads(request_payload)
		
		webhook_url = payload["response_url"]
		slack_id = payload['user']['id']
		
		if payload['type'] == "interactive_message" and payload['callback_id'] == 'center_selector':
			payload_action_name = payload['actions'][0]['name']
			payload_action_value = payload['actions'][0]['value']
			
			current_date = datetime.now()
			
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
			
			actions = [
				{'name': 'menu_date', 'text': '{}, {}'.format(d.strftime('%a'), d.strftime('%b %-d')), 'type': "button",
				 'value': d.strftime('%Y-%m-%d')} for d in daterange(start_on, end_on)]
			
			request_buttons = [
				{
					"text": "",
					"callback_id": "day_selector",
					"color": "#3AA3E3",
					"attachment_type": "default",
					"actions": actions
				}
			]
			
			return self.handle_response(
				slack_response={'text': f'Select A Day To Book', 'attachments': request_buttons})

		
		
