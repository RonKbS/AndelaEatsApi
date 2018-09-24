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
		
		data = {'vendorId': vendor.id, 'startDate': start_date, 'endDate': end_date, 'status': 1, 'terminationReason': engagement.termination_reason}
		response = self.client().post(self.make_url('/engagements/'), data=self.encode_to_json_string(data), headers=self.headers())
		response_json = self.decode_from_json_string(response.data.decode('utf-8'))
		payload = response_json['payload']
		
		self.assert200(response)
		self.assertJSONKeysPresent(payload, 'engagement')
		self.assertJSONKeysPresent(payload['engagement'], 'endDate', 'startDate', 'vendor', 'terminationReason', 'timestamps')
		
		self.assertEqual(payload['engagement']['vendor']['id'], vendor.id)
		self.assertEqual(payload['engagement']['vendor']['name'], vendor.name)
		self.assertEqual(payload['engagement']['vendor']['tel'], vendor.tel)
		
		# Assert The Year in engagement.start_date exists in the returned start_date response
		self.assertTrue(payload['engagement']['startDate'].find(start_date.split('-')[0]) > -1)
		self.assertTrue(payload['engagement']['startDate'].find(start_date.split('-')[2]) > -1)
		
		# Assert The Year in engagement.end_date exists in the returned end_date response
		self.assertTrue(payload['engagement']['endDate'].find(end_date.split('-')[0]) > -1)
		self.assertTrue(payload['engagement']['endDate'].find(end_date.split('-')[2]) > -1)
		
	def test_list_vendor_engagement_endpoint(self):
		VendorEngagementFactory.create_batch(4)
		
		response = self.client().get(self.make_url('/engagements/'), headers=self.headers())
		response_json = self.decode_from_json_string(response.data.decode('utf-8'))
		payload = response_json['payload']

		self.assert200(response)
		self.assertEqual(len(payload['engagements']), 4)
		self.assertJSONKeysPresent(payload['engagements'][0], 'endDate', 'startDate', 'id', 'vendor', 'terminationReason', 'timestamps')

	def test_get_specific_vendor_engagement_endpoint(self):
		engagement = VendorEngagementFactory()

		start_date = str(engagement.start_date)
		end_date = str(engagement.end_date)
		
		response = self.client().get(self.make_url('/engagements/{}'.format(engagement.id)), headers=self.headers())
		response_json = self.decode_from_json_string(response.data.decode('utf-8'))
		payload = response_json['payload']
		
		self.assert200(response)
		self.assertJSONKeyPresent(payload, 'engagement')
		self.assertJSONKeysPresent(payload['engagement'], 'endDate', 'startDate', 'vendor', 'terminationReason', 'timestamps')
		self.assertEqual(payload['engagement']['id'], engagement.id)
		self.assertEqual(payload['engagement']['vendor']['id'], engagement.vendor.id)
		self.assertEqual(payload['engagement']['vendor']['name'], engagement.vendor.name)
		self.assertEqual(payload['engagement']['vendor']['tel'], engagement.vendor.tel)
		
		# Assert The Year in engagement.start_date exists in the returned start_date response
		self.assertTrue(payload['engagement']['startDate'].find(start_date.split('-')[0]) > -1)
		self.assertTrue(payload['engagement']['startDate'].find(start_date.split('-')[2]) > -1)
		
		# Assert The Year in engagement.end_date exists in the returned end_date response
		self.assertTrue(payload['engagement']['endDate'].find(end_date.split('-')[0]) > -1)
		self.assertTrue(payload['engagement']['endDate'].find(end_date.split('-')[2]) > -1)
		
		'''Test invalid update request'''
		# User arbitrary value of 100 as the Vendor ID
		response = self.client().get(self.make_url('/engagements/100'), headers=self.headers())
		self.assert400(response)
	
	def test_update_vendor_engagement_endpoint(self):
		engagement = VendorEngagementFactory()

		data = {'vendorId': engagement.vendor_id, 'startDate': '2018-01-01', 'endDate': '2018-01-07', 'terminationReason': 'Food Poisoning', 'status':1}
		response = self.client().put(self.make_url('/engagements/{}'.format(engagement.id)),
									 data=self.encode_to_json_string(data), headers=self.headers())
		response_json = self.decode_from_json_string(response.data.decode('utf-8'))
		
		# print(response_json)
		
		# assert False
		payload = response_json['payload']
		
		self.assert200(response)
		self.assertEqual(payload['engagement']['id'], engagement.id)
		self.assertEqual(payload['engagement']['status'], data['status'])
		self.assertEqual(payload['engagement']['vendorId'], data['vendorId'])
		self.assertEqual(payload['engagement']['terminationReason'], data['terminationReason'])
		
		# Assert The Year in engagement.start_date exists in the returned start_date response
		self.assertTrue(payload['engagement']['startDate'].find(data['startDate'].split('-')[0]) > -1)
		self.assertTrue(payload['engagement']['startDate'].find(data['startDate'].split('-')[2]) > -1)
		
		# Assert The Year in engagement.end_date exists in the returned end_date response
		self.assertTrue(payload['engagement']['endDate'].find(data['endDate'].split('-')[0]) > -1)
		self.assertTrue(payload['engagement']['endDate'].find(data['endDate'].split('-')[2]) > -1)
		
		self.assertEqual(payload['engagement']['vendor']['name'], engagement.vendor.name)
		self.assertEqual(payload['engagement']['vendor']['address'], engagement.vendor.address)
		self.assertEqual(payload['engagement']['vendor']['contactPerson'], engagement.vendor.contact_person)
		self.assertEqual(payload['engagement']['vendor']['tel'], engagement.vendor.tel)
		self.assertEqual(payload['engagement']['vendor']['id'], engagement.vendor.id)
		
		# '''Test invalid update request'''
		# User arbitrary value of 100 as the Vendor ID
		response = self.client().put(self.make_url('/engagements/100'), data=self.encode_to_json_string(data),
									 headers=self.headers())
		self.assert400(response)
