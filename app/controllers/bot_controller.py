from app.controllers.base_controller import BaseController
from app.utils.slackhelper import SlackHelper
from datetime import datetime, timedelta
from app.utils import daterange


class BotController(BaseController):
	def __init__(self, request):
		BaseController.__init__(self, request)
		self.slackhelper = SlackHelper()

	def bot(self):
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
		
		actions = [{'name': 'menu_date', 'text': '{}, {}'.format(d.strftime('%a'), d.strftime('%b %-d')), 'type': "button", 'value': d.strftime('%Y-%m-%d')} for d in daterange(start_on, end_on) ]
		
		request_buttons = [
			{
				"text": "Select A Day To Book",
				"callback_id": "day_selector",
				"color": "#3AA3E3",
				"attachment_type": "default",
				"actions": actions
			}
		]
			
		return self.handle_response(slack_response={'text': f'Welcome To Andela Eats', 'attachments': request_buttons})

	def interactions(self):
		pass
