'''A module of application cron jobs'''
from datetime import datetime, time, date
import pytz
from app.models import VendorEngagement, Location, MealSession
from app.business_logic.meal_session.meal_session_logic import MealSessionLogic


class MealSessionCron(object):
	def __init__(self, app):
		self.app = app

	def _extract_current_locations(self):
		"""
		Return currently existing locations in the Database

		:return: A locations object
		"""
		with self.app.app_context():
			locations = Location.query.all()
			return locations

	@staticmethod
	def _meal_session_static_data():
		"""
		Return a dictionary instance to be populated dynamically

		:return: A dictionary Instance
		"""
		return {
			'breakfast': {
				'name': 'breakfast',
				'start_time': time(hour=7, minute=0),
				'stop_time': time(hour=10, minute=0)
			},
			'lunch': {
				'name': 'lunch',
				'start_time': time(hour=12, minute=0),
				'stop_time': time(hour=15, minute=0)
			}
		}

	def _complete_meal_session_construction_and_save(self, meal_sessions, date_time_to_use):
		"""
		Complete the contruction of the meal sessions
		and save if they do not already exist

		:param meal_sessions (dict): A dictionary with incomplete meal session data
		:param date_time_to_use (datetime): A datetime object to use
		:return:
		"""
		meal_session_date = date(year=date_time_to_use.year,
								 month=date_time_to_use.month,
								 day=date_time_to_use.day)
		meal_sessions['breakfast']['date'] = meal_session_date
		meal_sessions['lunch']['date'] = meal_session_date

		for meal_session in meal_sessions.values():
			# Ignore creation of meal session if one with in the specified
			# time already exists
			if MealSessionLogic.validate_meal_session_times(
				**{
					"name": meal_session.get('name'),
					"date_sent": meal_session.get('date'),
					"location_id": meal_session.get('location_id'),
					"start_time": meal_session.get('start_time'),
					"end_time": meal_session.get('stop_time'),
				}
			):
				continue

			MealSession(**meal_session).save()

	@staticmethod
	def _get_scheduler_current_date():
		return datetime.now(tz=pytz.timezone("Africa/Lagos"))

	@staticmethod
	def _get_location_current_date(city):
		return datetime.now(tz=pytz.timezone("Africa/" + city))

	def job_to_schedule(self):
		"""
		Auto populate the meal session table at a specified time interval

		:return (None):
		"""
		with self.app.app_context():
			scheduler_datetime = self._get_scheduler_current_date()

			locations = self._extract_current_locations()
			location_names = {location.id: location.name for location in locations}
			for location in locations:
				meal_sessions = self._meal_session_static_data()
				meal_sessions['breakfast']['location_id'] = location.id
				meal_sessions['lunch']['location_id'] = location.id
				location_name = location_names.get(location.id)
				# location_datetime = datetime.now(tz=pytz.timezone("Africa/" + location_name))
				location_datetime = self._get_location_current_date(location_name)
				if any([scheduler_datetime.year > location_datetime.year,
					   scheduler_datetime.month > location_datetime.month,
					   scheduler_datetime.day > location_datetime.day]):
					self._complete_meal_session_construction_and_save(meal_sessions, scheduler_datetime)
				else:
					self._complete_meal_session_construction_and_save(meal_sessions, location_datetime)

			print("    *** Meal session Cron Completed last run at: ", str(scheduler_datetime))



class Cron:

	def __init__(self, app):
		self.app = app
		self.meal_session_cron = MealSessionCron(app)

	def run_24_hourly(self):
		self.update_engagement_status()

	def run_meal_session_cron(self):
		self.meal_session_cron.job_to_schedule()

	def update_engagement_status(self):
		'''A cron job that periodically update an engagement status'''
		with self.app.app_context():
			active_engagements = VendorEngagement.query.filter_by(status=1)

			for engagement in active_engagements:
				if engagement.end_date < datetime.now().date():
					engagement.status = 0
					engagement.save()
