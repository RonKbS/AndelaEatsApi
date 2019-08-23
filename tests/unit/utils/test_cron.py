from unittest.mock import patch
import pytz
from datetime import datetime, date, timedelta, time
from tests.base_test_case import BaseTestCase
from factories.vendor_engagement_factory import VendorEngagementFactory
from factories.location_factory import LocationFactory
from factories.meal_session_factory import MealSessionFactory
from app.repositories.vendor_engagement_repo import VendorEngagementRepo
from app.models.meal_session import MealSession
from app.models.location import Location
from app.repositories.meal_session_repo import MealSessionRepo
from app.utils.cron import Cron, MealSessionCron
from app.business_logic.meal_session.meal_session_logic import MealSessionLogic
from app.utils.redisset import RedisSet
from factories.user_role_factory import UserRoleFactory
from factories.location_factory import LocationFactory
from app.repositories.user_role_repo import UserRoleRepo
from factories.role_factory import RoleFactory


class TestCron(BaseTestCase):

    def setUp(self):
        self.BaseSetUp()
        self.redis_set = RedisSet()

    def tearDown(self):
        self.BaseTearDown()

    def test_run_24_hourly_method(self):

        end_date = (datetime.now() - timedelta(weeks=1)).date()

        new_engagement = VendorEngagementFactory.create(end_date=end_date)
        temp_engagement_id = new_engagement.id
        Cron(self.app).run_24_hourly()

        with self.app.app_context():
            engagement = VendorEngagementRepo().get(temp_engagement_id)

        self.assertEqual(engagement.status, 0)

    def test_job_to_schedule_method_creates_meal_sessions(self):
        location = LocationFactory.create(id=1, name="Lagos")
        location.save()

        with self.app.app_context():
            Cron(self.app).run_meal_session_cron()

            meal_sessions = MealSessionRepo().fetch_all().items

            assert meal_sessions[0].name == "breakfast"
            assert meal_sessions[1].name == "lunch"

    @patch.object(MealSessionCron, '_get_scheduler_current_date')
    @patch.object(MealSessionCron, '_get_location_current_date')
    def test_meal_session_cron_creates_meal_session_using_scheduler_date(
            self,
            mock_location_current_date,
            mock_scheduler_current_date,
    ):
        location = LocationFactory.create(id=1, name="Lagos")
        location.save()

        with self.app.app_context():
            mock_scheduler_current_date.return_value = datetime(
                year=2019, month=4, day=10, hour=0, minute=0, tzinfo=pytz.timezone("Africa/Lagos"))
            mock_location_current_date.return_value = datetime(
                year=2019, month=3, day=10, hour=11, minute=0, tzinfo=pytz.timezone("Africa/Dakar"))

            Cron(self.app).run_meal_session_cron()

            meal_sessions = MealSessionRepo().fetch_all().items

            assert meal_sessions[0].name == "breakfast"
            assert meal_sessions[0].date.month == 4
            assert meal_sessions[1].name == "lunch"
            assert meal_sessions[1].date.month == 4

    @patch.object(MealSessionLogic, 'validate_meal_session_times')
    @patch.object(MealSessionCron, '_get_scheduler_current_date')
    @patch.object(MealSessionCron, '_get_location_current_date')
    def test_meal_session_cron_does_not_create_meal_session_if_session_already_exists(
            self,
            mock_location_current_date,
            mock_scheduler_current_date,
            mock_validate_meal_session_times
    ):
        LocationFactory.create(id=1, name="Kampala")

        with self.app.app_context():
            mock_scheduler_current_date.return_value = datetime(
                year=2019, month=4, day=10, tzinfo=pytz.timezone("Africa/Lagos"))
            mock_location_current_date.return_value = datetime(
                year=2019, month=3, day=10, tzinfo=pytz.timezone("Africa/Dakar"))
            mock_validate_meal_session_times.return_value = "A meal session already exists"

            Cron(self.app).run_meal_session_cron()

            meal_sessions = MealSessionRepo().fetch_all().items
            assert len(meal_sessions) == 0

    def test_run_5_minute_method(self):
        role = RoleFactory.create()
        location = LocationFactory.create()
        user_role = UserRoleFactory.build(
            role_id=role.id,
            location=location
        )

        UserRoleRepo().new_user_role(
          user_role.role_id,
          user_role.user_id,
          user_role.location_id,
          user_role.email
        )

        Cron(self.app).run_5_minute()

        results = self.redis_set.get(user_role.email[0])
        self.assertEqual(user_role.email, results[0])

        results = self.redis_set.get(user_role.email[0:1])
        self.assertEqual(user_role.email, results[0])

        results = self.redis_set.get(user_role.email[0:2])
        self.assertEqual(user_role.email, results[0])
