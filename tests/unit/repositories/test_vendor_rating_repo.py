'''A module of tests for vendor rating repository'''
from tests.base_test_case import BaseTestCase
from app.models.vendor_rating import VendorRating
from app.repositories.vendor_rating_repo import VendorRatingRepo
from factories.vendor_rating_factory import VendorRatingFactory


class TestVendorRatingRepo(BaseTestCase):
	'''Test class for VendorRating Repo'''

	def setUp(self):
		self.BaseSetUp()
		self.repo = VendorRatingRepo()

	def test_new_vendor_rating_method_returns_new_vendor_rating_object(self):
		vendor_rating = VendorRatingFactory.build()
		new_vendor_rating = self.repo.new_rating(vendor_rating.vendor_id, vendor_rating.user_id, vendor_rating.rating, vendor_rating.service_date, vendor_rating.rating_type, vendor_rating.type_id, vendor_rating.engagement_id, vendor_rating.channel, vendor_rating.comment)

		self.assertIsInstance(new_vendor_rating, VendorRating)
		self.assertEqual(vendor_rating.vendor_id, new_vendor_rating.vendor_id)
		self.assertEqual(vendor_rating.comment, new_vendor_rating.comment)
		self.assertEqual(vendor_rating.rating, new_vendor_rating.rating)
		self.assertIsNot(new_vendor_rating.id, 0)

	def test_meal_average_method_returns_meal_rating(self):
		vendor_rating = VendorRatingFactory.build()

		new_vendor_rating = self.repo.new_rating(
			vendor_rating.vendor_id, vendor_rating.user_id, vendor_rating.rating, vendor_rating.service_date,
			vendor_rating.rating_type, vendor_rating.type_id, vendor_rating.engagement_id,
			vendor_rating.channel, vendor_rating.comment
		)

		average_rating = self.repo.meal_average(new_vendor_rating.main_meal_id, new_vendor_rating.service_date)

		self.assertEqual(average_rating, 4)

