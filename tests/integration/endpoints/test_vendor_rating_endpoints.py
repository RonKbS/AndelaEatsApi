'''Module of integration tests for vendor rating endpoints'''
import factory
from tests.base_test_case import BaseTestCase
from factories import VendorFactory, VendorRatingFactory, UserRoleFactory, RoleFactory, PermissionFactory
from app.models import VendorRating

class TestVendorRatingEndpoints(BaseTestCase):
	'''Test class for Vendor rating endpoints'''

	def setUp(self):
		self.BaseSetUp()

	def test_create_vendor_rating_endpoint(self):
		rating = VendorRatingFactory.build()
		vendor_id = VendorFactory.create().id
		data = {'vendor_id': vendor_id, 'user_id': rating.user_id, 'rating': rating.rating, 'comment': rating.comment, 'channel': rating.channel}
		response = self.client().post(self.make_url('/ratings/'), data=self.encode_to_json_string(data), headers=self.headers())

		response_json = self.decode_from_json_string(response.data.decode('utf-8'))
		payload = response_json['payload']


		self.assertEqual(response.status_code, 201)
		self.assertJSONKeyPresent(response_json, 'payload')
		self.assertEqual(payload['rating']['vendorId'], vendor_id)
		self.assertEqual(payload['rating']['userId'], rating.user_id)
		self.assertEqual(payload['rating']['rating'], rating.rating)
		self.assertEqual(payload['rating']['comment'], rating.comment)
		self.assertEqual(payload['rating']['channel'], rating.channel)

	def test_list_vendor_ratings_endpoint(self):
		'''Test that users with the right permission can view list of vendor ratings'''

		role = RoleFactory.create(name='admin')
		user_id = BaseTestCase.user_id()
		vendor_id = VendorFactory.create().id
		permission = PermissionFactory.create(keyword='view_ratings', role_id=role.id)
		user_role = UserRoleFactory.create(user_id=user_id, role_id=role.id)

		for i in range(5):
			vendor_rating = VendorRating(vendor_id=vendor_id, user_id=user_id, comment=f'comment-{i}', rating=f'{i}', channel='slack')
			vendor_rating.save()

		response = self.client().get(self.make_url(f'/ratings/vendor/{vendor_id}'), headers=self.headers())
		response_json = self.decode_from_json_string(response.data.decode('utf-8'))

		payload = response_json['payload']

		self.assert200(response)
		self.assertEqual(len(payload['ratings']), 5)
		self.assertJSONKeysPresent(payload['ratings'][0], 'vendorId', 'userId', 'id', 'comment', 'rating','channel')

	def test_get_single_rating(self):
		'''Test that users with the right permission can see details of a single rating vendor rating'''

		rating = VendorRatingFactory.create()
		rating_id = rating.id
		role = RoleFactory.create(name='Admin')
		permission = PermissionFactory.create(keyword='view_ratings', role_id=role.id)
		user_role = UserRoleFactory.create(user_id=rating.user_id, role_id=role.id)

		response = self.client().get(self.make_url(f'/ratings/{rating_id}'), headers=self.headers())
		response_json = self.decode_from_json_string(response.data.decode('utf-8'))
		payload = response_json['payload']

		self.assert200(response)
		self.assertJSONKeyPresent(payload, 'rating')
		self.assertJSONKeysPresent(payload['rating'], 'vendorId', 'userId', 'id', 'comment', 'rating','channel')

		self.assertEqual(payload['rating']['id'], rating_id)
		self.assertEqual(payload['rating']['userId'], rating.user_id)
		self.assertEqual(payload['rating']['vendorId'], rating.vendor_id)
		self.assertEqual(payload['rating']['comment'], rating.comment)
		self.assertEqual(payload['rating']['rating'], rating.rating)


		'''Search for a non-existing rating returns 400 error'''
		response = self.client().get(self.make_url('/ratings/100'), headers=self.headers())
		self.assert400(response)

	def test_get_single_rating_without_permission(self):
		'''Test that users without the right permission cannot see details of a single rating vendor rating'''

		rating = VendorRatingFactory.create()
		rating_id = rating.id
		role = RoleFactory.create(name='Admin')
		permission = PermissionFactory.create(keyword='view_ratings', role_id=100)
		user_role = UserRoleFactory.create(user_id=rating.user_id, role_id=role.id)

		response = self.client().get(self.make_url(f'/ratings/{rating_id}'), headers=self.headers())

		self.assert400(response)

	def test_update_vendor_rating_endpoint(self):

		rating = VendorRatingFactory.create()

		data = {'comment': 'New comments'}
		response = self.client().put(self.make_url(f'/ratings/{rating.id}'), data=self.encode_to_json_string(data), headers=self.headers())
		response_json = self.decode_from_json_string(response.data.decode('utf-8'))
		payload = response_json['payload']

		self.assert200(response)
		self.assertEqual(payload['rating']['id'], rating.id)
		self.assertEqual(payload['rating']['userId'], rating.user_id)
		self.assertEqual(payload['rating']['vendorId'], rating.vendor_id)
		self.assertEqual(payload['rating']['comment'], rating.comment)
		self.assertEqual(payload['rating']['rating'], rating.rating)


		'''Updating a non-existent rating should return 400 error'''
		response = self.client().put(self.make_url(f'/ratings/ytg77'), data=self.encode_to_json_string(data), headers=self.headers())
		self.assert404(response)
