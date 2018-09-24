from datetime import date
from tests.base_test_case import BaseTestCase
from factories.vendor_factory import VendorFactory
from factories.vendor_engagement_factory import VendorEngagementFactory

class TestVendorEngagementEndpoints(BaseTestCase):

	def setUp(self):
		self.BaseSetUp()
		
	def test_create_vendor_engagement_endpoint(self):
		vendor = VendorFactory()
		engagement = VendorEngagementFactory.build()
		
		start_date = str(engagement.start_date)
		end_date = str(engagement.end_date)
		
		data = {'vendor_id': vendor.id, 'start_date': start_date, 'end_date': end_date, 'status': 1, 'termination_reason': engagement.termination_reason}
		response = self.client().post(self.make_url('/engagements/'), data=self.encode_to_json_string(data), headers=self.headers())
		response_json = self.decode_from_json_string(response.data.decode('utf-8'))
		payload = response_json['payload']
		
		self.assert200(response)
		self.assertJSONKeysPresent(payload, 'engagement')
		self.assertJSONKeysPresent(payload['engagement'], 'end_date', 'start_date', 'vendor', 'termination_reason', 'timestamps')
		
		self.assertEqual(payload['engagement']['vendor']['id'], vendor.id)
		self.assertEqual(payload['engagement']['vendor']['name'], vendor.name)
		self.assertEqual(payload['engagement']['vendor']['tel'], vendor.tel)
		
		# Assert The Year in engagement.start_date exists in the returned start_date response
		self.assertTrue(payload['engagement']['start_date'].find(start_date.split('-')[0]) > -1)
		self.assertTrue(payload['engagement']['start_date'].find(start_date.split('-')[2]) > -1)
		
		# Assert The Year in engagement.end_date exists in the returned end_date response
		self.assertTrue(payload['engagement']['end_date'].find(end_date.split('-')[0]) > -1)
		self.assertTrue(payload['engagement']['end_date'].find(end_date.split('-')[2]) > -1)
		
	def test_list_vendor_engagement_endpoint(self):
		VendorEngagementFactory.create_batch(4)
		
		response = self.client().get(self.make_url('/engagements/'), headers=self.headers())
		response_json = self.decode_from_json_string(response.data.decode('utf-8'))
		payload = response_json['payload']

		self.assert200(response)
		self.assertEqual(len(payload['engagements']), 4)
		self.assertJSONKeysPresent(payload['engagements'][0], 'end_date', 'start_date', 'id', 'vendor', 'termination_reason', 'timestamps')

	def test_get_specific_vendor_engagement_endpoint(self):
		engagement = VendorEngagementFactory()

		start_date = str(engagement.start_date)
		end_date = str(engagement.end_date)
		
		response = self.client().get(self.make_url('/engagements/{}'.format(engagement.id)), headers=self.headers())
		response_json = self.decode_from_json_string(response.data.decode('utf-8'))
		payload = response_json['payload']
		
		self.assert200(response)
		self.assertJSONKeyPresent(payload, 'engagement')
		self.assertJSONKeysPresent(payload['engagement'], 'end_date', 'start_date', 'vendor', 'termination_reason', 'timestamps')
		self.assertEqual(payload['engagement']['id'], engagement.id)
		self.assertEqual(payload['engagement']['vendor']['id'], engagement.vendor.id)
		self.assertEqual(payload['engagement']['vendor']['name'], engagement.vendor.name)
		self.assertEqual(payload['engagement']['vendor']['tel'], engagement.vendor.tel)
		
		# Assert The Year in engagement.start_date exists in the returned start_date response
		self.assertTrue(payload['engagement']['start_date'].find(start_date.split('-')[0]) > -1)
		self.assertTrue(payload['engagement']['start_date'].find(start_date.split('-')[2]) > -1)
		
		# Assert The Year in engagement.end_date exists in the returned end_date response
		self.assertTrue(payload['engagement']['end_date'].find(end_date.split('-')[0]) > -1)
		self.assertTrue(payload['engagement']['end_date'].find(end_date.split('-')[2]) > -1)
		
		'''Test invalid update request'''
		# User arbitrary value of 100 as the Vendor ID
		response = self.client().get(self.make_url('/engagements/100'), headers=self.headers())
		self.assert400(response)
	
	def test_update_vendor_engagement_endpoint(self):
		engagement = VendorEngagementFactory()

		data = {'vendor_id': engagement.vendor_id, 'start_date': '2018-01-01', 'end_date': '2018-01-07', 'termination_reason': 'Food Poisoning', 'status':1}
		response = self.client().put(self.make_url('/engagements/{}'.format(engagement.id)),
									 data=self.encode_to_json_string(data), headers=self.headers())
		response_json = self.decode_from_json_string(response.data.decode('utf-8'))
		payload = response_json['payload']
		
		self.assert200(response)
		self.assertEqual(payload['engagement']['id'], engagement.id)
		self.assertEqual(payload['engagement']['status'], data['status'])
		self.assertEqual(payload['engagement']['vendor_id'], data['vendor_id'])
		self.assertEqual(payload['engagement']['termination_reason'], data['termination_reason'])
		
		# Assert The Year in engagement.start_date exists in the returned start_date response
		self.assertTrue(payload['engagement']['start_date'].find(data['start_date'].split('-')[0]) > -1)
		self.assertTrue(payload['engagement']['start_date'].find(data['start_date'].split('-')[2]) > -1)
		
		# Assert The Year in engagement.end_date exists in the returned end_date response
		self.assertTrue(payload['engagement']['end_date'].find(data['end_date'].split('-')[0]) > -1)
		self.assertTrue(payload['engagement']['end_date'].find(data['end_date'].split('-')[2]) > -1)
		
		self.assertEqual(payload['engagement']['vendor']['name'], engagement.vendor.name)
		self.assertEqual(payload['engagement']['vendor']['address'], engagement.vendor.address)
		self.assertEqual(payload['engagement']['vendor']['contact_person'], engagement.vendor.contact_person)
		self.assertEqual(payload['engagement']['vendor']['tel'], engagement.vendor.tel)
		self.assertEqual(payload['engagement']['vendor']['id'], engagement.vendor.id)
		
		# '''Test invalid update request'''
		# User arbitrary value of 100 as the Vendor ID
		response = self.client().put(self.make_url('/engagements/100'), data=self.encode_to_json_string(data),
									 headers=self.headers())
		self.assert400(response)
