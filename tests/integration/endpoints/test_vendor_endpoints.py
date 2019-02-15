import datetime
from tests.base_test_case import BaseTestCase
from app.repositories.vendor_engagement_repo import VendorEngagementRepo
from app.utils.auth import Auth
from app import db
from factories import VendorFactory, PermissionFactory, RoleFactory, UserRoleFactory, LocationFactory

class TestVendorEndpoints(BaseTestCase):

	def setUp(self):
		self.BaseSetUp()
	
	def test_create_vendor_endpoint(self):
		vendor = VendorFactory.build()
		data = {'name': vendor.name, 'address': vendor.address, 'tel': vendor.tel, 'isActive': vendor.is_active, 'contactPerson': vendor.contact_person}
		response = self.client().post(self.make_url('/vendors/'), data=self.encode_to_json_string(data), headers=self.headers())
		response_json = self.decode_from_json_string(response.data.decode('utf-8'))
		payload = response_json['payload']
		
		self.assertEqual(response.status_code, 201)
		self.assertJSONKeyPresent(response_json, 'payload')
		self.assertEqual(payload['vendor']['name'], vendor.name)
		self.assertEqual(payload['vendor']['tel'], vendor.tel)
		self.assertEqual(payload['vendor']['contactPerson'], vendor.contact_person)
		self.assertEqual(payload['vendor']['address'], vendor.address)
		
	def test_list_vendors_endpoint(self):
		location = LocationFactory(id=self.headers()['X-Location'])
		# Create Three Dummy Vendors
		vendors = VendorFactory.create_batch(3, location_id=location.id)

		page_id = 1
		response = self.client().get(self.make_url('/vendors/'), headers=self.headers())
		response_json = self.decode_from_json_string(response.data.decode('utf-8'))
		payload = response_json['payload']
		
		self.assert200(response)
		self.assertEqual(len(payload['vendors']), 3)
		self.assertJSONKeysPresent(payload['vendors'][0], 'name', 'tel', 'id', 'address', 'contactPerson','timestamps')

	def test_list_vendors_endpoint_returns_data_sorted_by_name(self):
		location = LocationFactory(id=self.headers()['X-Location'])
		# Create Three Dummy Vendors
		vendors = VendorFactory.create_batch(3, location_id=location.id)

		response = self.client().get(self.make_url('/vendors/'), headers=self.headers())
		response_json = self.decode_from_json_string(response.data.decode('utf-8'))
		payload = response_json['payload']

		sorted_vendor_names = sorted([vendor.name for vendor in vendors])
		vendors = payload['vendors']

		self.assert200(response)
		self.assertEqual(len(payload['vendors']), 3)
		self.assertEqual(sorted_vendor_names[0], vendors[0].get('name'))
		self.assertEqual(sorted_vendor_names[1], vendors[1].get('name'))
		self.assertEqual(sorted_vendor_names[2], vendors[2].get('name'))

	def test_get_specific_vendor_enpoint(self):
		vendor = VendorFactory.create()
		response = self.client().get(self.make_url('/vendors/{}'.format(vendor.id)), headers=self.headers())
		response_json = self.decode_from_json_string(response.data.decode('utf-8'))
		payload = response_json['payload']

		self.assert200(response)
		self.assertJSONKeyPresent(payload, 'vendor')
		self.assertJSONKeysPresent(payload['vendor'], 'name', 'tel', 'id', 'address', 'contactPerson', 'timestamps')
		self.assertEqual(payload['vendor']['id'], vendor.id)
		self.assertEqual(payload['vendor']['name'], vendor.name)
		self.assertEqual(payload['vendor']['address'], vendor.address)
		self.assertEqual(payload['vendor']['tel'], vendor.tel)
		

		'''Test invalid update request'''
		# User arbitrary value of 100 as the Vendor ID
		response = self.client().get(self.make_url('/vendors/100'), headers=self.headers())
		self.assert400(response)
		
	def test_update_vendors_endpoint(self):
		
		vendor = VendorFactory.create()
		data = {'name': 'Jays Place', 'address':'123 Awesome Ave', 'tel':'10101010101', 'isActive': True, 'contactPerson':'Joseph Cobhams'}
		response = self.client().put(self.make_url('/vendors/{}'.format(vendor.id)), data=self.encode_to_json_string(data), headers=self.headers())
		response_json = self.decode_from_json_string(response.data.decode('utf-8'))
		payload = response_json['payload']
		
		self.assert200(response)
		self.assertEqual(payload['vendor']['name'], data['name'])
		self.assertEqual(payload['vendor']['address'], data['address'])
		self.assertEqual(payload['vendor']['tel'], data['tel'])
		self.assertEqual(payload['vendor']['contactPerson'], data['contactPerson'])
		
		'''Test invalid update request'''
		# User arbitrary value of 100 as the Vendor ID
		response = self.client().put(self.make_url('/vendors/100'), data=self.encode_to_json_string(data), headers=self.headers())
		self.assert400(response)

	def test_delete_vendor_endpoint_with_right_permission(self):
		vendor = VendorFactory.create()

		role = RoleFactory.create(name='admin')
		user_id = BaseTestCase.user_id()
		permission = PermissionFactory.create(keyword='delete_vendor', role_id=role.id)
		user_role = UserRoleFactory.create(user_id=user_id, role_id=role.id)

		response = self.client().delete(self.make_url(f'/vendors/{vendor.id}'), headers=self.headers())
		response_json = self.decode_from_json_string(response.data.decode('utf-8'))
		payload = response_json['payload']

		self.assert200(response)
		self.assertEqual(payload['status'], 'success')
		self.assertEqual(response_json['msg'], 'Vendor deleted')

	def test_delete_vendor_endpoint_without_right_permission(self):
		vendor = VendorFactory.create()

		role = RoleFactory.create(name='admin')
		user_id = BaseTestCase.user_id()
		permission = PermissionFactory.create(keyword='delete_vendor', role_id=100)
		user_role = UserRoleFactory.create(user_id=user_id, role_id=role.id)

		response = self.client().delete(self.make_url(f'/vendors/{vendor.id}'), headers=self.headers())
		response_json = self.decode_from_json_string(response.data.decode('utf-8'))

		self.assert400(response)
		self.assertEqual(response_json['msg'], 'Access Error - No Permission Granted')

	def test_delete_vendor_endpoint_with_wrong_vendor_id(self):
		vendor = VendorFactory.create()

		role = RoleFactory.create(name='admin')
		user_id = BaseTestCase.user_id()
		permission = PermissionFactory.create(keyword='delete_vendor', role_id=role.id)
		user_role = UserRoleFactory.create(user_id=user_id, role_id=role.id)

		response = self.client().delete(self.make_url(f'/vendors/-576A'), headers=self.headers())

		self.assert404(response)

	def test_delete_vendor_with_associated_engagement(self):
		current_date = datetime.datetime.now().date()
		vendor = VendorFactory.create()
		vendor_engagement_repo = VendorEngagementRepo()
		vendor_engagement = vendor_engagement_repo.new_vendor_engagement(vendor_id=vendor.id, start_date=current_date, location_id=self.headers()['X-Location'])

		role = RoleFactory.create(name='admin')
		user_id = BaseTestCase.user_id()
		permission = PermissionFactory.create(keyword='delete_vendor', role_id=role.id)
		user_role = UserRoleFactory.create(user_id=user_id, role_id=role.id)

		response = self.client().delete(self.make_url(f'/vendors/{vendor.id}'), headers=self.headers())
		response_json = self.decode_from_json_string(response.data.decode('utf-8'))

		self.assert400(response)
		self.assertEqual(response_json['msg'], 'Vendor cannot be deleted because it has a child object')

	def test_delete_vendor_deletes_vendor_engagement(self):
		pass

	def test_suspend_vendor(self):
		vendor = VendorFactory.create()

		response = self.client().put(self.make_url(f'/vendors/suspend/{vendor.id}'), headers=self.headers())
		response_json = self.decode_from_json_string(response.data.decode('utf-8'))
		payload = response_json['payload']

		self.assert200(response)
		self.assertEqual(payload['vendor']['isActive'], False)

	def test_un_suspend_vendor(self):
		vendor = VendorFactory.create(is_active=False)

		response = self.client().put(self.make_url(f'/vendors/un_suspend/{vendor.id}'), headers=self.headers())
		response_json = self.decode_from_json_string(response.data.decode('utf-8'))
		payload = response_json['payload']

		self.assert200(response)
		self.assertEqual(payload['vendor']['isActive'], True)

	def test_list_suspended_vendors(self):

		vendors = VendorFactory.create_batch(3, is_active=True)
		vendors = VendorFactory.create_batch(4, is_active=False)

		response = self.client().get(self.make_url('/vendors/suspended/'), headers=self.headers())
		response_json = self.decode_from_json_string(response.data.decode('utf-8'))
		payload = response_json['payload']
		
		self.assert200(response)
		self.assertEqual(len(payload['vendors']), 4)
		self.assertEqual(payload['vendors'][0]['isActive'], False)		

	def test_list_deleted_vendors(self):
		vendors = VendorFactory.create_batch(4, is_deleted=True)
		vendors = VendorFactory.create_batch(3, is_deleted=False)

		response = self.client().get(self.make_url('/vendors/deleted/'), headers=self.headers())
		response_json = self.decode_from_json_string(response.data.decode('utf-8'))
		payload = response_json['payload']
		
		self.assert200(response)
		self.assertEqual(len(payload['vendors']), 4)
		self.assertEqual(payload['vendors'][0]['isDeleted'], True)
