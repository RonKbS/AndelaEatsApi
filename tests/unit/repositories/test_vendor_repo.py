from tests.base_test_case import BaseTestCase
from app.models import Vendor
from app.repositories import VendorRepo, VendorRatingRepo
from factories import VendorFactory, VendorRatingFactory


class TestVendorRepo(BaseTestCase):
	
	def setUp(self):
		self.BaseSetUp()
		self.repo = VendorRepo()
		self.rating_repo = VendorRatingRepo()
		
	def test_new_vendor_method_returns_new_vendor_object(self):
		vendor = VendorFactory.build()
		new_vendor = self.repo.new_vendor(vendor.name, vendor.address, vendor.tel, vendor.is_active, vendor.contact_person, vendor.location_id)
		
		self.assertIsInstance(new_vendor, Vendor)
		self.assertEqual(vendor.name, new_vendor.name)
		self.assertEqual(vendor.tel, new_vendor.tel)
		self.assertEqual(vendor.address, new_vendor.address)
		self.assertEqual(vendor.contact_person, new_vendor.contact_person)
		self.assertIsNot(new_vendor.id, 0)

	def test_update_vendor_rating(self):
		vendor = VendorFactory.build()
		new_vendor = self.repo.new_vendor(vendor.name, vendor.address, vendor.tel, vendor.is_active, vendor.contact_person, vendor.location_id)

		vendor_rating = VendorRatingFactory.build()
		self.rating_repo.new_rating(new_vendor.id, vendor_rating.user_id, 4,
												 vendor_rating.service_date, vendor_rating.rating_type,
												 vendor_rating.type_id, vendor_rating.engagement_id,
												 vendor_rating.channel, vendor_rating.comment)

		self.repo.update_vendor_average_rating(new_vendor.id)

		self.assertEqual(new_vendor.average_rating, 4)
