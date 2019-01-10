'''A module of application cron jobs'''
from datetime import datetime
from app.models import VendorEngagement

class Cron:

	def __init__(self, app):
		self.app = app

	def run_24_hourly(self):
		self.update_engagement_status()

	def run_12_hourly(self):
		pass

	def run_6_hourly(self):
		pass

	
	def update_engagement_status(self):

		'''A cron job that periodically update an engagement status'''
		with self.app.app_context():
			active_engagements = VendorEngagement.query.filter_by(status=1)

			for engagement in active_engagements:
				if engagement.end_date < datetime.now().date():
					engagement.status = 0
					engagement.save()
