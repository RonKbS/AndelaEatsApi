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

	def test_get_unpaginated_asc_orders_ascending(self):
		vendor_1 = VendorFactory.create()
		vendor_2 = VendorFactory.create()

		vendor_names = sorted([vendor.name for vendor in [vendor_1, vendor_2]])

		results = self.repo.get_unpaginated_asc(Vendor.name)

		self.assertEqual(vendor_names[0], results[0].name)
		self.assertEqual(vendor_names[1], results[1].name)

	def test_get_unpaginated_desc_orders_ascending(self):
		vendor_1 = VendorFactory.create()
		vendor_2 = VendorFactory.create()

		vendor_names = sorted(
			[vendor.name for vendor in [vendor_1, vendor_2]],
			reverse=True
		)

		results = self.repo.get_unpaginated_desc(Vendor.name)

		self.assertEqual(vendor_names[0], results[0].name)
		self.assertEqual(vendor_names[1], results[1].name)
		
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

	def test_fetch_all_method_returns_paginated_results(self):
		vendor_1 = VendorFactory.create()
		vendor_2 = VendorFactory.create()

		paginated_result = self.repo.fetch_all()

		self.assertEqual(len(paginated_result.items), 2)
		self.assertEqual(paginated_result.items[0], vendor_1)
		self.assertEqual(paginated_result.items[1], vendor_2)

	def test_filter_all_method_returns_paginated_results(self):
		vendor_1 = VendorFactory.create()
		vendor_2 = VendorFactory.create()

		paginated_result = self.repo.filter_all()

		self.assertEqual(len(paginated_result.items), 2)
		self.assertEqual(paginated_result.items[0], vendor_1)
		self.assertEqual(paginated_result.items[1], vendor_2)

	def test_filter_and_count_method_returns_correct_count(self):
		vendor_1 = VendorFactory.create()
		vendor_2 = VendorFactory.create()

		result = self.repo.filter_and_count()

		self.assertEqual(result, 2)

	def test_filter_and_order_method_returns_correct_order(self):
		vendor_1 = VendorFactory.create()
		vendor_2 = VendorFactory.create()

		result = self.repo.filter_and_order('created_at')

		self.assertEqual(result.count(), 2)
		self.assertNotEqual(result.first(), vendor_2)


	def test_order_by_method_returns_correct_order(self):
		vendor_1 = VendorFactory.create()
		vendor_2 = VendorFactory.create()

		result = self.repo.order_by('created_at')

		self.assertEqual(result.count(), 2)
		self.assertNotEqual(result.first(), vendor_2)

	def test_paginate_method_returns_paginated_results(self):
		vendor_1 = VendorFactory.create()
		vendor_2 = VendorFactory.create()

		paginated_result = self.repo.paginate()

		self.assertEqual(len(paginated_result.items), 2)
		self.assertEqual(paginated_result.items[0], vendor_1)
		self.assertEqual(paginated_result.items[1], vendor_2)

	def test_filter_method_returns_paginated_results(self):
		vendor_1 = VendorFactory.create()
		vendor_2 = VendorFactory.create()

		paginated_result = self.repo.filter()

		self.assertEqual(len(paginated_result.items), 2)
		self.assertEqual(paginated_result.items[0], vendor_1)
		self.assertEqual(paginated_result.items[1], vendor_2)

	def test_filter_by_asc_method_returns_ascending_ordered_results(self):
		vendor_1 = VendorFactory.create()
		vendor_2 = VendorFactory.create()

		vendor_names = sorted([vendor.name for vendor in [vendor_1, vendor_2]])

		results = self.repo.filter_by_asc(Vendor.name)

		self.assertEqual(vendor_names[0], results.items[0].name)
		self.assertEqual(vendor_names[1], results.items[1].name)

	def test_filter_by_desc_method_returns_descending_ordered_results(self):
		vendor_1 = VendorFactory.create()
		vendor_2 = VendorFactory.create()

		vendor_names = sorted(
			[vendor.name for vendor in [vendor_1, vendor_2]],
			reverse=True
		)

		results = self.repo.filter_by_desc(Vendor.name)
		self.assertEqual(vendor_names[0], results.items[0].name)
		self.assertEqual(vendor_names[1], results.items[1].name)






		
		