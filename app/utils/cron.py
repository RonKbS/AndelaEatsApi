'''A module of application cron jobs'''
import datetime
import pytz
from apscheduler.schedulers.background import BackgroundScheduler
from app.models import VendorEngagement, Location, MealSession


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
				'start_time': datetime.time(hour=7, minute=0),
				'stop_time': datetime.time(hour=10, minute=0)
			},
			'lunch': {
				'name': 'lunch',
				'start_time': datetime.time(hour=12, minute=0),
				'stop_time': datetime.time(hour=15, minute=0)
			}
		}

	@staticmethod
	def _background_scheduler_with_time_zone(_timezone):
		"""
		Return a scheduler that is time aware

		:param _timezone(string): A string representing the time zone ie. Africa/Lagos
		:return: A background scheduler instance
		"""
		return BackgroundScheduler(timezone=_timezone)

	def _return_meal_sessions_with_locations(self):
		"""
		Generate Dummy meal sessions containing the existing locations

		:return (List): List of meal sessions
		"""
		meal_sessions_with_locations = []
		locations = self._extract_current_locations()
		for location in locations:
			meal_sessions = self._meal_session_static_data()
			meal_sessions['breakfast']['location_id'] = location.id
			meal_sessions['lunch']['location_id'] = location.id

			meal_sessions_with_locations.append(meal_sessions)

		return meal_sessions_with_locations

	def _generate_callable_to_schedule(self, meal_sessions):
		"""
		Generate a closure to be used for the various cron jobs

		:param meal_sessions(dict): A dictionary containing meal sessions with their current times
		:return (closure): A function ready to be called
		"""
		def dynamic_callable():
			with self.app.app_context():
				location_name = Location.query.filter_by(id=meal_sessions.get('breakfast')['location_id']).first().name

				for meal_session in meal_sessions.values():
					current_date = datetime.datetime.now(pytz.timezone('Africa/' + location_name))
					meal_session['date'] = current_date
					new_meal_session = MealSession(**meal_session)
					new_meal_session.save()
					print("A meal session has been created")

		return dynamic_callable

	def run_meal_session_cron(self):
		"""
		Generate schedulers and start them for each meal sessions in each different location

		:return (None):
		"""

		un_started_schedulers = []
		meal_sessions = self._return_meal_sessions_with_locations()
		locations = {location.id: location.name for location in self._extract_current_locations()}

		for meal_session in meal_sessions:
			location_name = locations.get(meal_session.get('breakfast').get('location_id'))

			job = self._generate_callable_to_schedule(meal_session)

			try:
				scheduler = self._background_scheduler_with_time_zone("Africa/" + location_name)
			except Exception:
				scheduler = BackgroundScheduler()
			scheduler.add_job(job, trigger='interval', seconds=40)

			# attach schedulers
			un_started_schedulers.append(scheduler)

		# Start Schedulers
		for scheduler in un_started_schedulers:
			scheduler.start()


class Cron:

	def __init__(self, app):
		self.app = app

	def run_24_hourly(self):
		self.update_engagement_status()

	def update_engagement_status(self):
		'''A cron job that periodically update an engagement status'''
		with self.app.app_context():
			active_engagements = VendorEngagement.query.filter_by(status=1)

			for engagement in active_engagements:
				if engagement.end_date < datetime.now().date():
					engagement.status = 0
					engagement.save()

	def register_and_start_cron_jobs(self):
		scheduler = BackgroundScheduler()
		# in your case you could change seconds to hours
		scheduler.add_job(self.update_engagement_status, trigger='interval', hours=24)
		scheduler.start()

		meal_session_cron = MealSessionCron(self.app)

		meal_session_cron.run_meal_session_cron()
