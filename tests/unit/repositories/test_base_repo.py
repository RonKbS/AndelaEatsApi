from tests.base_test_case import BaseTestCase
from app.repositories.base_repo import BaseRepo
from factories.vendor_factory import VendorFactory
from app.models.vendor import Vendor # One Model is required to test the base repo. Using Vendor

class TestBaseRepository(BaseTestCase):

	def setUp(self):
		self.BaseSetUp()
		self.repo = BaseRepo(Vendor)
		
	def test_repo_get_method_returns_value_by_id(self):
		vendor = VendorFactory()
		vendor_ = self.repo.get(vendor.id)
		
		self.assertIsInstance(vendor_, Vendor)
		self.assertEqual(vendor.id, vendor_.id)
		self.assertEqual(vendor.tel, vendor_.tel)
		self.assertEqual(vendor.address, vendor_.address)
		
	def test_update_method_updates_model_values(self):
		vendor = VendorFactory()
		
		updates = {'name': 'Jays Place', 'tel': '09012343', 'contact_person': 'Joseph Cobhams'}
		vendor_ = self.repo.update(vendor, **updates)
		
		self.assertIsInstance(vendor_, Vendor)
		self.assertEqual(vendor_.name, updates['name'])
		self.assertEqual(vendor_.tel, updates['tel'])
		self.assertEqual(vendor_.contact_person, updates['contact_person'])
		
	def test_count_method_returns_correct_count_as_integer(self):
		VendorFactory.create_batch(10)
		count = self.repo.count()
		
		self.assertIsInstance(count, int)
		self.assertEqual(count, 10)
		
	def test_get_first_item_method_only_returns_that(self):
		vendor_1 = VendorFactory()
		vendor_2 = VendorFactory.create()
		
		vendor_ = self.repo.get_first_item()
		
		self.assertIsInstance(vendor_, Vendor)
		self.assertEqual(vendor_1.id, vendor_.id)
		self.assertEqual(vendor_1.tel, vendor_.tel)
		self.assertEqual(vendor_1.address, vendor_.address)
		
		self.assertNotEqual(vendor_2.id, vendor_.id)


		
		