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
		end_date = str(engagement.end_date.strftime('%Y-%m-%d'))
		
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
		pass
	
	def test_update_vendor_engagement_endpoint(self):
		pass
		