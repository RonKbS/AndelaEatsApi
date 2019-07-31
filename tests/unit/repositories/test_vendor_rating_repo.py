'''A module of tests for vendor rating repository'''
from datetime import datetime
from tests.base_test_case import BaseTestCase
from app.models.vendor_rating import VendorRating
from app.repositories.vendor_rating_repo import VendorRatingRepo
from factories.vendor_rating_factory import VendorRatingFactory
from factories.vendor_factory import VendorFactory
from factories.location_factory import LocationFactory
from factories.vendor_engagement_factory import VendorEngagementFactory
from factories.meal_item_factory import MealItemFactory


class TestVendorRatingRepo(BaseTestCase):
    '''Test class for VendorRating Repo'''

    def setUp(self):
        self.BaseSetUp()
        self.repo = VendorRatingRepo()
        self.location = LocationFactory()
        self.vendor = VendorFactory()
        self.engagement = VendorEngagementFactory(
            location_id=self.location.id,
            vendor_id=self.vendor.id
        )

    def tearDown(self):
        self.BaseTearDown()

    def test_new_vendor_rating_method_returns_new_vendor_rating_object(self):
        vendor_rating = VendorRatingFactory.build(
            vendor_id=self.vendor.id,
            engagement_id=self.engagement.id
        )
        new_vendor_rating = self.repo.new_rating(vendor_rating.vendor_id, vendor_rating.user_id, vendor_rating.rating, vendor_rating.service_date, vendor_rating.rating_type, vendor_rating.type_id, vendor_rating.engagement_id, vendor_rating.main_meal_id, vendor_rating.channel, vendor_rating.comment)

        self.assertIsInstance(new_vendor_rating, VendorRating)
        self.assertEqual(vendor_rating.vendor_id, new_vendor_rating.vendor_id)
        self.assertEqual(vendor_rating.comment, new_vendor_rating.comment)
        self.assertEqual(vendor_rating.rating, new_vendor_rating.rating)
        self.assertIsNot(new_vendor_rating.id, 0)

    def test_meal_average_method_returns_meal_rating(self):
        vendor_rating = VendorRatingFactory.build(
            vendor_id=self.vendor.id,
            engagement_id=self.engagement.id
        )
        main_meal_id = MealItemFactory.create().id

        new_vendor_rating = self.repo.new_rating(
            vendor_rating.vendor_id, vendor_rating.user_id, vendor_rating.rating, vendor_rating.service_date,
            vendor_rating.rating_type, vendor_rating.type_id, vendor_rating.engagement_id,
            main_meal_id,
            vendor_rating.channel, vendor_rating.comment
        )

        average_rating = self.repo.meal_average(new_vendor_rating.main_meal_id, new_vendor_rating.service_date)

        self.assertEqual(average_rating, 4)

    def test_daily_average_rating(self):
        VendorRatingFactory.create_batch(3, rating=4, service_date=datetime.now().date())

        resp = self.repo.daily_average_rating(datetime.now().date())
        self.assertEqual(resp, 4)

