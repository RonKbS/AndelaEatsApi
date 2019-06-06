from datetime import datetime, timedelta
from unittest.mock import patch, Mock
from app.repositories.menu_repo import MenuRepo
from app.models import Location
from app.repositories import VendorEngagementRepo
from tests.base_test_case import BaseTestCase
from factories import (
	VendorFactory,
	RoleFactory,
	UserRoleFactory,
	PermissionFactory,
	VendorEngagementFactory,
	LocationFactory
	)


class TestVendorEngagementEndpoints(BaseTestCase):

	def setUp(self):
		self.BaseSetUp()

	def test_create_vendor_engagement_endpoint(self):
		vendor = VendorFactory()
		engagement = VendorEngagementFactory.build()

		start_date = str(engagement.start_date)
		end_date = str(engagement.end_date)

		data = {'vendorId': vendor.id, 'startDate': start_date, 'endDate': end_date, 'status': 1,
				'terminationReason': engagement.termination_reason, 'location_id': engagement.location_id}
		response = self.client().post(self.make_url('/engagements/'), data=self.encode_to_json_string(data),
									  headers=self.headers())
		response_json = self.decode_from_json_string(response.data.decode('utf-8'))
		payload = response_json['payload']

		self.assertEqual(response.status_code, 201)
		self.assertJSONKeysPresent(payload, 'engagement')
		self.assertJSONKeysPresent(payload['engagement'], 'endDate', 'startDate', 'vendor', 'terminationReason',
								   'timestamps')

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
		location = LocationFactory(id=self.headers()['X-Location'])
		VendorEngagementFactory.create_batch(4, location_id=location.id)
		
		response = self.client().get(self.make_url('/engagements/'), headers=self.headers())
		response_json = self.decode_from_json_string(response.data.decode('utf-8'))
		payload = response_json['payload']

		self.assert200(response)
		self.assertEqual(len(payload['engagements']), 4)
		self.assertJSONKeysPresent(payload['engagements'][0], 'endDate', 'startDate', 'id', 'vendor',
								   'terminationReason', 'timestamps')

	def test_list_vendor_engagement_by_vendor_id(self):
		pass

	def test_list_vendor_engagement_by_deleted_vendor_id(self):
		pass

	def test_get_specific_vendor_engagement_endpoint(self):
		engagement = VendorEngagementFactory()

		start_date = str(engagement.start_date)
		end_date = str(engagement.end_date)

		response = self.client().get(self.make_url('/engagements/{}'.format(engagement.id)), headers=self.headers())
		response_json = self.decode_from_json_string(response.data.decode('utf-8'))
		payload = response_json['payload']

		self.assert200(response)
		self.assertJSONKeyPresent(payload, 'engagement')
		self.assertJSONKeysPresent(payload['engagement'], 'endDate', 'startDate', 'vendor', 'terminationReason',
								   'timestamps')
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

		data = {'vendorId': engagement.vendor_id, 'startDate': '2018-01-01', 'endDate': '2018-01-07',
				'terminationReason': 'Food Poisoning', 'status': 1}
		response = self.client().put(self.make_url('/engagements/{}'.format(engagement.id)),
									 data=self.encode_to_json_string(data), headers=self.headers())
		response_json = self.decode_from_json_string(response.data.decode('utf-8'))

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

	def test_delete_engagement_endpoint_with_right_permission(self):
		engagement = VendorEngagementFactory.create()

		role = RoleFactory.create(name='admin')
		user_id = BaseTestCase.user_id()
		PermissionFactory.create(keyword='delete_engagement', role_id=role.id)
		UserRoleFactory.create(user_id=user_id, role_id=role.id)

		response = self.client().delete(self.make_url(f'/engagements/{engagement.id}'), headers=self.headers())
		response_json = self.decode_from_json_string(response.data.decode('utf-8'))
		payload = response_json['payload']

		self.assert200(response)
		self.assertEqual(payload['status'], 'success')
		self.assertEqual(response_json['msg'], 'Engagement deleted')

	def test_delete_engagement_endpoint_without_right_permission(self):
		engagement = VendorEngagementFactory.create()

		role = RoleFactory.create(name='admin')
		user_id = BaseTestCase.user_id()
		PermissionFactory.create(keyword='delete_engagement', role_id=1000)
		UserRoleFactory.create(user_id=user_id, role_id=role.id)

		response = self.client().delete(self.make_url(f'/engagements/{engagement.id}'), headers=self.headers())
		response_json = self.decode_from_json_string(response.data.decode('utf-8'))
		self.assert400(response)
		self.assertEqual(response_json['msg'], 'Access Error - No Permission Granted')

	def test_delete_engagement_endpoint_with_wrong_vendor_id(self):
		VendorEngagementFactory.create()

		role = RoleFactory.create(name='admin')
		user_id = BaseTestCase.user_id()
		PermissionFactory.create(keyword='delete_engagement', role_id=role.id)
		UserRoleFactory.create(user_id=user_id, role_id=role.id)

		response = self.client().delete(self.make_url(f'/engagement/-576A'), headers=self.headers())

		self.assert404(response)

	def test_delete_engagement_with_associated_menus(self):
		datetime.now().date()
		engagement = VendorEngagementFactory.create()
		menu_repo = MenuRepo()
		menu_repo.new_menu(date='2018-10-15', meal_period='lunch', main_meal_id=1, allowed_side=1,
								  allowed_protein=1,
								  side_items=[2], protein_items=[3], vendor_engagement_id=engagement.id, location_id=1)

		role = RoleFactory.create(name='admin')
		user_id = BaseTestCase.user_id()
		PermissionFactory.create(keyword='delete_engagement', role_id=role.id)
		UserRoleFactory.create(user_id=user_id, role_id=role.id)

		response = self.client().delete(self.make_url(f'/engagements/{engagement.id}'), headers=self.headers())
		response_json = self.decode_from_json_string(response.data.decode('utf-8'))

		self.assert400(response)
		self.assertEqual(response_json['msg'], 'This engagement cannot be deleted because it has a child object')

	def test_list_engagements_by_vendor_endpoint(self):
		vendor = VendorFactory.create()
		VendorEngagementFactory.create(vendor=vendor)

		response = self.client().get(self.make_url(f'/engagements/vendor/{vendor.id}'), headers=self.headers())
		response_json = self.decode_from_json_string(response.data.decode('utf-8'))

		self.assert200(response)
		self.assertEqual(response_json['msg'], 'OK')
		self.assertEqual(response_json['payload']['engagements'][0]['vendor']['id'], vendor.id)

	def test_upcoming_engagements_endpoint(self):
		vendor = VendorFactory.create()
		VendorEngagementFactory.create(vendor=vendor)

		response = self.client().get(self.make_url(f'/engagements/upcoming'), headers=self.headers())
		response_json = self.decode_from_json_string(response.data.decode('utf-8'))

		self.assert200(response)
		self.assertEqual(response_json['msg'], 'OK')
		self.assertEqual(response_json['payload']['engagements'][0]['vendor']['id'], vendor.id)

	def test_immediate_past_engagement(self):

		location = LocationFactory()
		location.save()
		vendor = VendorFactory.create(location_id=location.id)
		vendor.save()
		engagement1 = VendorEngagementFactory.create(vendor_id=vendor.id, end_date=datetime.now()-timedelta(10), location_id=location.id)
		engagement2 = VendorEngagementFactory.create(vendor_id=vendor.id, end_date=datetime.now()-timedelta(14), location_id=location.id)
		engagement1.save()
		engagement2.save()

		response = self.client().get(self.make_url(f'/engagements/past/{location.id}'), headers=self.headers())
		response_json = self.decode_from_json_string(response.data.decode('utf-8'))

		self.assert200(response)
		self.assertEqual(response_json['msg'], 'OK')

	def test_immediate_past_engagement_no_past_engagement(self):

		location = LocationFactory()
		location.save()
		vendor = VendorFactory.create(location_id=location.id)
		vendor.save()
		engagement1 = VendorEngagementFactory.create(vendor_id=vendor.id, end_date=datetime.now()+timedelta(10), location_id=location.id)
		engagement2 = VendorEngagementFactory.create(vendor_id=vendor.id, end_date=datetime.now()+timedelta(14), location_id=location.id)
		engagement1.save()
		engagement2.save()

		response = self.client().get(self.make_url(f'/engagements/past/{location.id}'), headers=self.headers())
		response_json = self.decode_from_json_string(response.data.decode('utf-8'))

		self.assert404(response)
		self.assertEqual(response_json['msg'], 'No past engagement for this location')



