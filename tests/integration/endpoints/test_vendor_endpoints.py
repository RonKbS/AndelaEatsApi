from tests.base_test_case import BaseTestCase
from factories.vendor_factory import VendorFactory

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
