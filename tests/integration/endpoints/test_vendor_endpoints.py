import datetime
from tests.base_test_case import BaseTestCase
from app.repositories.vendor_engagement_repo import VendorEngagementRepo
from factories import VendorFactory, PermissionFactory, RoleFactory, UserRoleFactory

class TestVendorEndpoints(BaseTestCase):

	def setUp(self):
		self.BaseSetUp()
	
	def test_create_vendor_endpoint(self):
		vendor = VendorFactory.build()
		data = {'name': vendor.name, 'address': vendor.address, 'tel': vendor.tel, 'contactPerson': vendor.contact_person}
		response = self.client().post(self.make_url('/vendors/'), data=self.encode_to_json_string(data), headers=self.headers())
		response_json = self.decode_from_json_string(response.data.decode('utf-8'))
		payload = response_json['payload']
		
		self.assert200(response)
		self.assertJSONKeyPresent(response_json, 'payload')
		self.assertEqual(payload['vendor']['name'], vendor.name)
		self.assertEqual(payload['vendor']['tel'], vendor.tel)
		self.assertEqual(payload['vendor']['contactPerson'], vendor.contact_person)
		self.assertEqual(payload['vendor']['address'], vendor.address)
		
	def test_list_vendors_endpoint(self):
		
		# Create Three Dummy Vendors
		VendorFactory.create_batch(3)
		page_id = 1
		response = self.client().get(self.make_url('/vendors/'), headers=self.headers())
		response_json = self.decode_from_json_string(response.data.decode('utf-8'))
		payload = response_json['payload']

		self.assert200(response)
		self.assertEqual(len(payload['vendors']), 3)
		self.assertJSONKeysPresent(payload['vendors'][0], 'name', 'tel', 'id', 'address', 'contactPerson','timestamps')
		
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
		data = {'name': 'Jays Place', 'address':'123 Awesome Ave', 'tel':'10101010101', 'contactPerson':'Joseph Cobhams'}
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
		vendor_engagement = vendor_engagement_repo.new_vendor_engagement(vendor_id=vendor.id, start_date=current_date)

		role = RoleFactory.create(name='admin')
		user_id = BaseTestCase.user_id()
		permission = PermissionFactory.create(keyword='delete_vendor', role_id=role.id)
		user_role = UserRoleFactory.create(user_id=user_id, role_id=role.id)

		response = self.client().delete(self.make_url(f'/vendors/{vendor.id}'), headers=self.headers())
		response_json = self.decode_from_json_string(response.data.decode('utf-8'))

		self.assert400(response)
		self.assertEqual(response_json['msg'], 'Vendor cannot be deleted because it has a child object')