from tests.base_test_case import BaseTestCase
from app.models.vendor import Vendor
from app.repositories.vendor_repo import VendorRepo
from factories.vendor_factory import VendorFactory


class TestVendorRepo(BaseTestCase):
	
	def setUp(self):
		self.BaseSetUp()
		self.repo = VendorRepo()
		
	def test_new_vendor_method_returns_new_vendor_object(self):
		vendor = VendorFactory.build()
		new_vendor = self.repo.new_vendor(vendor.name, vendor.address, vendor.tel, vendor.contact_person)
		
		self.assertIsInstance(new_vendor, Vendor)
		self.assertEqual(vendor.name, new_vendor.name)
		self.assertEqual(vendor.tel, new_vendor.tel)
		self.assertEqual(vendor.address, new_vendor.address)
		self.assertEqual(vendor.contact_person, new_vendor.contact_person)
		self.assertIsNot(new_vendor.id, 0)
		