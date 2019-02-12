'''Module of integration tests for vendor rating endpoints'''
import factory
from tests.base_test_case import BaseTestCase
from datetime import datetime
from factories import VendorFactory, VendorRatingFactory, UserRoleFactory, RoleFactory, PermissionFactory, \
    VendorEngagementFactory, OrderFactory, MealItemFactory

from .user_role import create_user_role



class TestVendorRatingEndpoints(BaseTestCase):
    '''Test class for Vendor rating endpoints'''

    def setUp(self):
        self.BaseSetUp()

    def test_create_vendor_rating_endpoint_no_token(self):
        rating = VendorRatingFactory.build()
        order_id = OrderFactory.create().id
        vendor_id = VendorFactory.create().id
        engagement_id = VendorEngagementFactory.create().id
        main_meal_id = MealItemFactory.create().id
        data = {'mainMealId': main_meal_id, 'vendorId': vendor_id, 'engagementId': engagement_id, 'serviceDate': datetime.strftime(rating.service_date, '%Y-%m-%d'), 'ratingType': rating.rating_type, 'orderId': order_id, 'user_id': rating.user_id, 'rating': rating.rating, 'comment': rating.comment, 'channel': rating.channel}
        response = self.client().post(self.make_url('/ratings/order/'), data=self.encode_to_json_string(data), headers=self.headers_without_token())

        response_json = self.decode_from_json_string(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_json['msg'], 'Authorization Header is Expected')

    def test_create_vendor_rating_endpoint_invalid_token(self):
        rating = VendorRatingFactory.build()
        order_id = OrderFactory.create().id
        vendor_id = VendorFactory.create().id
        engagement_id = VendorEngagementFactory.create().id
        main_meal_id = MealItemFactory.create().id
        data = {'mainMealId': main_meal_id, 'vendorId': vendor_id, 'engagementId': engagement_id,
                'serviceDate': datetime.strftime(rating.service_date, '%Y-%m-%d'), 'ratingType': rating.rating_type,
                'orderId': order_id, 'user_id': rating.user_id, 'rating': rating.rating, 'comment': rating.comment,
                'channel': rating.channel}
        response = self.client().post(self.make_url('/ratings/order/'), data=self.encode_to_json_string(data),
                                      headers={
                                                'Content-Type': 'application/json',
                                                'X-Location': '1',
                                                'Authorization': 'Bearer vnvhnv.hhbhjvjvcbcgff.cggnncbnnf'
                                                })

        response_json = self.decode_from_json_string(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_json['msg'], 'Error Decoding')

    def test_create_vendor_rating_endpoint_invalid_auth_format(self):
        rating = VendorRatingFactory.build()
        order_id = OrderFactory.create().id
        vendor_id = VendorFactory.create().id
        engagement_id = VendorEngagementFactory.create().id
        main_meal_id = MealItemFactory.create().id
        data = {'mainMealId': main_meal_id, 'vendorId': vendor_id, 'engagementId': engagement_id,
                    'serviceDate': datetime.strftime(rating.service_date, '%Y-%m-%d'), 'ratingType': rating.rating_type,
                    'orderId': order_id, 'user_id': rating.user_id, 'rating': rating.rating, 'comment': rating.comment,
                    'channel': rating.channel}
        response = self.client().post(self.make_url('/ratings/order/'), data=self.encode_to_json_string(data),
                                          headers={
                                              'Content-Type': 'application/json',
                                              'X-Location': '1',
                                              'Authorization': 'Ebarer {}'.format(self.get_valid_token())
                                          })

        response_json = self.decode_from_json_string(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_json['msg'], 'Authorization Header Must Start With Bearer')


    def test_create_vendor_rating_endpoint_invalid_location_id(self):
        rating = VendorRatingFactory.build()
        order_id = OrderFactory.create().id
        vendor_id = VendorFactory.create().id
        engagement_id = VendorEngagementFactory.create().id
        main_meal_id = MealItemFactory.create().id
        data = {'mainMealId': main_meal_id, 'vendorId': vendor_id, 'engagementId': engagement_id,
                    'serviceDate': datetime.strftime(rating.service_date, '%Y-%m-%d'), 'ratingType': rating.rating_type,
                    'orderId': order_id, 'user_id': rating.user_id, 'rating': rating.rating, 'comment': rating.comment,
                    'channel': rating.channel}
        response = self.client().post(self.make_url('/ratings/order/'), data=self.encode_to_json_string(data),
                                          headers={
                                              'Content-Type': 'application/json',
                                              'X-Location': 'Z',
                                              'Authorization': 'Bearer {}'.format(self.get_valid_token())
                                          })

        response_json = self.decode_from_json_string(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_json['msg'], 'Location Header Value is Invalid')


    def test_create_vendor_rating_endpoint_invalid_auth(self):
        rating = VendorRatingFactory.build()
        order_id = OrderFactory.create().id
        vendor_id = VendorFactory.create().id
        engagement_id = VendorEngagementFactory.create().id
        main_meal_id = MealItemFactory.create().id
        data = {'mainMealId': main_meal_id, 'vendorId': vendor_id, 'engagementId': engagement_id,
                    'serviceDate': datetime.strftime(rating.service_date, '%Y-%m-%d'), 'ratingType': rating.rating_type,
                    'orderId': order_id, 'user_id': rating.user_id, 'rating': rating.rating, 'comment': rating.comment,
                    'channel': rating.channel}
        response = self.client().post(self.make_url('/ratings/order/'), data=self.encode_to_json_string(data),
                                          headers={
                                              'Content-Type': 'application/json',
                                              'X-Location': '1',
                                              'Authorization': 'Bearer'
                                          })

        response_json = self.decode_from_json_string(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_json['msg'], 'Internal Application Error')



    def test_create_order_rating_endpoint(self):
        rating = VendorRatingFactory.build()
        order_id = OrderFactory.create().id
        vendor_id = VendorFactory.create().id
        engagement_id = VendorEngagementFactory.create().id
        main_meal_id = MealItemFactory.create().id
        data = {'mainMealId': main_meal_id, 'vendorId': vendor_id, 'engagementId': engagement_id, 'serviceDate': datetime.strftime(rating.service_date, '%Y-%m-%d'), 'ratingType': rating.rating_type, 'orderId': order_id, 'user_id': rating.user_id, 'rating': rating.rating, 'comment': rating.comment, 'channel': rating.channel}
        response = self.client().post(self.make_url('/ratings/order/'), data=self.encode_to_json_string(data), headers=self.headers())

        response_json = self.decode_from_json_string(response.data.decode('utf-8'))

        payload = response_json['payload']


        self.assertEqual(response.status_code, 201)
        self.assertJSONKeyPresent(response_json, 'payload')
        self.assertEqual(payload['rating']['userId'], rating.user_id)
        self.assertEqual(payload['rating']['rating'], rating.rating)
        self.assertEqual(payload['rating']['comment'], rating.comment)
        self.assertEqual(payload['rating']['channel'], rating.channel)

    def test_get_single_rating(self):
        """Test that users with the right permission can see details of a single rating vendor rating"""

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

    def test_call_exempted_url(self):
        """Test that a call to '/apispec_1.json' does not require authentication"""

        response = self.client().get('/apispec_1.json')

        self.assert200(response)

    def test_get_single_rating_without_permission(self):
        """Test that users without the right permission cannot see details of a single rating vendor rating"""

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


        """Updating a non-existent rating should return 400 error"""
        response = self.client().patch(self.make_url(f'/ratings/777777777'), data=self.encode_to_json_string(data), headers=self.headers())
        self.assert404(response)

    def test_list_rating_endpoint(self):
        vendor = VendorFactory.create()

        engagement = VendorEngagementFactory.create(vendor=vendor)

        rating = VendorRatingFactory.create(engagement=engagement)

        create_user_role('view_ratings')

        response = self.client().get(self.make_url(f'/ratings/{rating.service_date.strftime("%Y-%m-%d")}'),
                                     headers=self.headers())
        response_json = self.decode_from_json_string(response.data.decode('utf-8'))

        self.assert404(response)
        self.assertEqual(response_json['msg'], 'No ratings for this date')

    def test_create_vendor_rating_endpoint(self):
        vendor  = VendorFactory.create()

        engagement = VendorEngagementFactory.create(vendor=vendor)
        engagement_rating = VendorRatingFactory.build(engagement_id=engagement.id)

        rating_data = {'rating': engagement_rating.rating, 'engagementId': engagement_rating.engagement_id,
                       'serviceDate': engagement_rating.service_date.strftime('%Y-%m-%d')}

        response = self.client().post(self.make_url(f'/ratings/'), data=self.encode_to_json_string(rating_data),
                                      headers=self.headers())
        response_json = self.decode_from_json_string(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response_json['msg'], 'Rating created')
        self.assertEqual(response_json['payload']['rating']['id'], engagement_rating.id)

