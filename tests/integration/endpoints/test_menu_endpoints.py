from datetime import date, datetime, timedelta
from tests.base_test_case import BaseTestCase
from factories import (
    VendorFactory,
    RoleFactory,
    PermissionFactory,
    UserRoleFactory,
    MenuFactory,
    VendorEngagementFactory,
    MealItemFactory,
    LocationFactory
)
from app.utils import db
from app.models import MealItem, Menu
from app.repositories import MenuRepo, MealItemRepo
from app.utils.enums import MealPeriods


class MenuEndpoints(BaseTestCase):
    """A test class for menu endpoints"""

    def setUp(self):
        self.BaseSetUp()

    def tearDown(self):
        self.BaseTearDown()

    def test_create_menu_endpoint_with_wrong_permission(self):
        """ Test for creation of a new menu without permmission """
        role = RoleFactory.create(name='admin')
        user_id = BaseTestCase.user_id()
        PermissionFactory.create(keyword='delete_menu', role=role)
        UserRoleFactory.create(user_id=user_id, role=role)

        menu = MenuFactory.build()
        main_meal_item = MealItemFactory.build()
        side_meal_item = MealItemFactory.build()
        protein_meal_item = MealItemFactory.build()
        vendor = VendorFactory.build()
        vendor_engagement = VendorEngagementFactory.build(vendor_id=vendor.id)

        data = {
            'date': menu.date.strftime('%Y-%m-%d'), 'mealPeriod': menu.meal_period,
            'mainMealId': main_meal_item.id, 'allowedSide': menu.allowed_side,
            'allowedProtein': menu.allowed_protein,
            'sideItems': [side_meal_item.id],
            'proteinItems': [protein_meal_item.id],
            'vendorEngagementId': vendor_engagement.id
        }

        response = self.client().post(self.make_url('/admin/menus/'), \
                                      data=self.encode_to_json_string(data), headers=self.headers())

        self.assert400(response)

    def test_create_menu_endpoint_with_right_permission_and_input(self):
        """Test for creation of new menu"""
        location = LocationFactory()
        menu = MenuFactory.build()
        main_meal_item = MealItemFactory.create()
        side_meal_item = MealItemFactory.create()
        protein_meal_item = MealItemFactory.create()

        vendor = VendorFactory.build()
        vendor_engagement = VendorEngagementFactory.build(vendor=vendor)
        vendor_engagement.save()

        role = RoleFactory.create(name='admin')
        user_id = BaseTestCase.user_id()
        PermissionFactory.create(keyword='create_menu', role=role)
        UserRoleFactory.create(user_id=user_id, role=role)

        data = {
            'date': menu.date.strftime('%Y-%m-%d'), 'mealPeriod': menu.meal_period,
            'mainMealId': main_meal_item.id, 'allowedSide': menu.allowed_side,
            'allowedProtein': menu.allowed_protein,
            'sideItems': [side_meal_item.id],
            'proteinItems': [protein_meal_item.id],
            'vendorEngagementId': vendor_engagement.id
        }
        headers = self.headers()
        headers.update({'X-Location': location.id})

        response = self.client().post(self.make_url('/admin/menus/'), \
                                      data=self.encode_to_json_string(data), headers=headers)
        response_json = self.decode_from_json_string(response.data.decode('utf-8'))
        payload = response_json['payload']

        self.assertEqual(response.status_code, 201)
        self.assertJSONKeysPresent(payload, 'menu')
        self.assertJSONKeysPresent(payload['menu'], 'mainMeal',
                                   'proteinItems', 'sideItems', 'allowedProtein', 'allowedSide',
                                   'date', 'id', 'mealPeriod', 'timestamps', 'vendorEngagementId'
                                   )

        self.assertEqual(
            payload['menu']['vendorEngagementId'], vendor_engagement.id
        )
        self.assertEqual(payload['menu']['mealPeriod'], menu.meal_period)
        self.assertEqual(payload['menu']['mainMealId'], main_meal_item.id)
        self.assertEqual(payload['menu']['allowedSide'], menu.allowed_side)
        self.assertEqual(payload['menu']['allowedProtein'], menu.allowed_protein)

    def test_create_menu_endpoint_with_wrong_main_meal(self):
        """Test for creation of new menu with wrong main meal"""
        menu = MenuFactory.build()
        main_meal_item = MealItemFactory.create()
        side_meal_item = MealItemFactory.create()
        protein_meal_item = MealItemFactory.create()

        vendor = VendorFactory.build()
        vendor_engagement = VendorEngagementFactory.build(vendor_id=vendor.id)

        role = RoleFactory.create(name='admin')
        user_id = BaseTestCase.user_id()
        PermissionFactory.create(keyword='create_menu', role=role)
        UserRoleFactory.create(user_id=user_id, role=role)

        data = {
            'date': menu.date.strftime('%Y-%m-%d'), 'mealPeriod': menu.meal_period,
            'mainMealId': 100, 'allowedSide': menu.allowed_side,
            'allowedProtein': menu.allowed_protein,
            'sideItems': [side_meal_item.id],
            'proteinItems': [protein_meal_item.id],
            'vendorEngagementId': vendor_engagement.id
        }

        response = self.client().post(self.make_url('/admin/menus/'), \
                                      data=self.encode_to_json_string(data), headers=self.headers())
        response_json = self.decode_from_json_string(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_json['msg'], 'Bad Request - mainMealId contains invalid id(s) for meal_item table ')

    def test_create_menu_endpoint_with_wrong_side_item(self):
        """Test for creation of new menu with wrong side items"""
        menu = MenuFactory.build()
        main_meal_item = MealItemFactory.create()
        side_meal_item = MealItemFactory.create()
        protein_meal_item = MealItemFactory.create()

        vendor = VendorFactory.build()
        vendor_engagement = VendorEngagementFactory.build(vendor_id=vendor.id)

        role = RoleFactory.create(name='admin')
        user_id = BaseTestCase.user_id()
        PermissionFactory.create(keyword='create_menu', role=role)
        UserRoleFactory.create(user_id=user_id, role=role)

        data = {
            'date': menu.date.strftime('%Y-%m-%d'), 'mealPeriod': menu.meal_period,
            'mainMealId': main_meal_item.id, 'allowedSide': menu.allowed_side,
            'allowedProtein': menu.allowed_protein,
            'sideItems': [100],
            'proteinItems': [protein_meal_item.id],
            'vendorEngagementId': vendor_engagement.id
        }

        response = self.client().post(self.make_url('/admin/menus/'), \
                                      data=self.encode_to_json_string(data), headers=self.headers())
        response_json = self.decode_from_json_string(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_json['msg'], 'Bad Request - sideItems contains invalid id(s) for meal_item table ')

    def test_create_menu_endpoint_with_wrong_protein_items(self):
        """Test for creation of new menu with wrong protein items"""
        menu = MenuFactory.build()
        main_meal_item = MealItemFactory.create()
        side_meal_item = MealItemFactory.create()
        protein_meal_item = MealItemFactory.create()

        vendor = VendorFactory.build()
        vendor_engagement = VendorEngagementFactory.build(vendor_id=vendor.id)

        role = RoleFactory.create(name='admin')
        user_id = BaseTestCase.user_id()
        PermissionFactory.create(keyword='create_menu', role=role)
        UserRoleFactory.create(user_id=user_id, role=role)

        data = {
            'date': menu.date.strftime('%Y-%m-%d'), 'mealPeriod': menu.meal_period,
            'mainMealId': main_meal_item.id, 'allowedSide': menu.allowed_side,
            'allowedProtein': menu.allowed_protein,
            'sideItems': [side_meal_item.id],
            'proteinItems': [100],
            'vendorEngagementId': vendor_engagement.id
        }

        response = self.client().post(self.make_url('/admin/menus/'), \
                                      data=self.encode_to_json_string(data), headers=self.headers())
        response_json = self.decode_from_json_string(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_json['msg'], 'Bad Request - proteinItems contains invalid id(s) for meal_item table ')

    def test_create_menu_endpoint_with_existing_main_meal_item(self):
        """Multiple menus with same same main meal id should not exist on the same day"""
        location = LocationFactory.create()
        main_meal_item = MealItemFactory.create(location=location)
        side_meal_item = MealItemFactory.create(location=location)
        protein_meal_item = MealItemFactory.create(location=location)

        headers = self.headers()
        headers.update({'X-Location': location.id})

        menu = MenuFactory.build(location=location)
        menu.save()
        vendor = VendorFactory.build(location=location)
        vendor_engagement = VendorEngagementFactory.build(vendor=vendor, location=location)
        vendor_engagement.save()
        data = {
            'date': menu.date.strftime('%Y-%m-%d'), 'mealPeriod': menu.meal_period,
            'mainMealId': main_meal_item.id, 'allowedSide': menu.allowed_side,
            'allowedProtein': menu.allowed_protein,
            'sideItems': [side_meal_item.id],
            'proteinItems': [protein_meal_item.id],
            'vendorEngagementId': vendor_engagement.id, 'location_id': location.id
        }

        existing_menu = MenuRepo().new_menu(menu.date.strftime('%Y-%m-%d'), menu.meal_period, main_meal_item.id,
                                            menu.allowed_side,
                                            menu.allowed_protein, [side_meal_item.id], [protein_meal_item.id],
                                            vendor_engagement.id, location.id)

        role = RoleFactory.create(name='admin')
        user_id = BaseTestCase.user_id()
        PermissionFactory.create(keyword='create_menu', role=role)
        UserRoleFactory.create(user_id=user_id, role=role)

        response = self.client().post(self.make_url('/admin/menus/'), \
                                      data=self.encode_to_json_string(data), headers=headers)
        response_json = self.decode_from_json_string(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_json['msg'], 'You can\'t create multiple menus with same main item on the same day')

    def test_delete_menu_endpoint_with_right_permission(self):
        """Test that a user with permission to delete menu can successfully do so"""
        menu = MenuFactory.create()
        menu.save()

        role = RoleFactory.create(name='admin')
        user_id = BaseTestCase.user_id()
        PermissionFactory.create(keyword='delete_menu', role=role)
        UserRoleFactory.create(user_id=user_id, role=role)

        response = self.client().delete(self.make_url(f'/admin/menus/{menu.id}'), headers=self.headers())
        response_json = self.decode_from_json_string(response.data.decode('utf-8'))
        payload = response_json['payload']

        self.assert200(response)
        self.assertEqual(payload['status'], "success")

    def test_delete_menu_endpoint_without_right_permission(self):
        """Test that a user without permission to delete menu cannot successfully do so"""
        menu = MenuFactory.create()
        menu.save()

        role = RoleFactory.create(name='admin')
        user_id = BaseTestCase.user_id()
        PermissionFactory.create(keyword='delete_menu', role_id=100)
        UserRoleFactory.create(user_id=user_id, role=role)

        response = self.client().delete(self.make_url(f'/admin/menus/{menu.id}'), headers=self.headers())

        self.assert401(response)

    def test_delete_menu_endpoint_with_wrong_menu_id(self):
        """Test that a for unsuccessful delete of wrong menu id"""

        role = RoleFactory.create(name='admin')
        user_id = BaseTestCase.user_id()
        PermissionFactory.create(keyword='delete_menu', role=role)
        UserRoleFactory.create(user_id=user_id, role=role)

        response = self.client().delete(self.make_url(f'/admin/menus/1000'), headers=self.headers())
        response_json = self.decode_from_json_string(response.data.decode('utf-8'))

        self.assert400(response)
        self.assertEqual(response_json['msg'], 'Invalid or incorrect menu_id provided')

    def test_list_menu_endpoint_without_right_permission(self):
        """Test that users without the right permission cannot view list of menus"""

        role = RoleFactory.create(name='admin')
        user_id = BaseTestCase.user_id()
        PermissionFactory.create(keyword='view_menu', role_id=100)
        UserRoleFactory.create(user_id=user_id, role=role)
        current_date = datetime.now().date()

        MenuFactory.create_batch(5)
        Menu.query.all()

        response = self.client().get(self.make_url(f'/admin/menus/{MealPeriods.lunch}/{current_date}'),
                                     headers=self.headers())

        self.assert401(response)

    def test_list_menu_endpoint_with_right_permission(self):
        """Test that users with the right permission can view list of menus"""
        location = LocationFactory.create()
        meal_item_repo = MealItemRepo()
        role = RoleFactory.create(name='admin')
        user_id = BaseTestCase.user_id()
        PermissionFactory.create(keyword='view_menu', role=role)
        UserRoleFactory.create(user_id=user_id, role=role)
        the_date = datetime.now().date()
        current_date = the_date.strftime('%Y-%m-%d')

        side_meal_item = meal_item_repo.new_meal_item(name="side1",  image="image11",
                                                      meal_type="side", location_id=location.id)
        protein_meal_item = meal_item_repo.new_meal_item(name="protein1",  image="image12",
                                                         meal_type="protein", location_id=location.id)
        MenuFactory.create_batch(5, side_items=side_meal_item.id, protein_items=protein_meal_item.id, date=the_date)

        response = self.client().get(self.make_url(f'/admin/menus/{MealPeriods.lunch}/{current_date}'),
                                     headers=self.headers())

        self.assert200(response)

    def test_list_menu_range_endpoint_without_right_permission(self):
        """ Test that users without the right permission cannot view list of menus with date range """
        start_date = datetime.now().date()
        end_date = datetime.now().date() + timedelta(days=7)

        MenuFactory.create_batch(5)

        response = self.client().get(self.make_url(f'/admin/menus/{MealPeriods.lunch}/{start_date}/{end_date}'),
                                     headers=self.headers())

        self.assert401(response)

    def test_list_menu_range_endpoint_with_right_permission(self):
        """ Test that users with right permission can view list of menu with date range """
        location = LocationFactory.create()
        meal_item_repo = MealItemRepo()
        role = RoleFactory.create(name='admin')
        user_id = BaseTestCase.user_id()
        PermissionFactory.create(keyword='view_menu', role=role)
        UserRoleFactory.create(user_id=user_id, role=role)
        current_date = datetime.now().date()
        start_date = current_date.strftime('%Y-%m-%d')
        end_date = (datetime.now().date() + timedelta(days=7)).strftime('%Y-%m-%d')

        side_meal_item = meal_item_repo.new_meal_item(name="side1",  image="image11",
                                                      meal_type="side", location_id=location.id)
        protein_meal_item = meal_item_repo.new_meal_item(name="protein1",  image="image12",
                                                         meal_type="protein", location_id=location.id)
        MenuFactory.create_batch(5, side_items=side_meal_item.id, protein_items=protein_meal_item.id, location=location)

        response = self.client() \
            .get(self.make_url(f'/admin/menus/{MealPeriods.lunch}/{start_date}/{end_date}'), headers=self.headers())

        self.assert200(response)

    def test_list_menu_range_endpoint_with_right_permission_wrong_range(self):
        """ Test that users with right permission but wrong range cannot view """
        role = RoleFactory.create(name='admin')
        user_id = BaseTestCase.user_id()
        PermissionFactory.create(keyword='view_menu', role=role)
        UserRoleFactory.create(user_id=user_id, role=role)

        start_date = datetime.now().date()
        end_date = datetime.now().date() + timedelta(days=-7)

        MenuFactory.create_batch(5)

        response = self.client().get(self.make_url(f'/admin/menus/{MealPeriods.lunch}/{start_date}/{end_date}'),
                                     headers=self.headers())
        response_json = self.decode_from_json_string(response.data.decode('utf-8'))

        self.assert400(response)
        self.assertEqual(response_json['msg'], 'Provide valid date range. start_date cannot be greater than end_date')

    def test_list_menu_range_endpoint_with_right_permission_wrong_period(self):
        location = LocationFactory()
        meal_item_repo = MealItemRepo()
        role = RoleFactory.create(name='admin')
        user_id = BaseTestCase.user_id()
        PermissionFactory.create(keyword='view_menu', role=role)
        UserRoleFactory.create(user_id=user_id, role=role)
        current_date = datetime.now().date()
        start_date = current_date.strftime('%Y-%m-%d')
        end_date = (datetime.now().date() + timedelta(days=7)).strftime('%Y-%m-%d')

        side_meal_item = meal_item_repo.new_meal_item(name="side1",  image="image11",
                                                      meal_type="side", location_id=location.id)
        protein_meal_item = meal_item_repo.new_meal_item(name="protein1",  image="image12",
                                                         meal_type="protein", location_id=location.id)
        MenuFactory.create_batch(5, side_items=side_meal_item.id, protein_items=protein_meal_item.id)

        response = self.client() \
            .get(self.make_url(f'/admin/menus/wrong_period/{start_date}/{end_date}'), headers=self.headers())
        response_json = self.decode_from_json_string(response.data.decode('utf-8'))

        self.assert400(response)
        self.assertEqual(response_json['msg'], 'Provide valid meal period and date range')

    def test_update_menu_endpoint(self):
        """Test update of a menu"""
        location = LocationFactory()
        role = RoleFactory.create(name='admin')
        user_id = BaseTestCase.user_id()
        PermissionFactory.create(keyword='update_menu', role=role)
        UserRoleFactory.create(user_id=user_id, role=role)

        meal_item_repo = MealItemRepo()

        main_meal_item = meal_item_repo.new_meal_item(name="main1", image="image1",
                                                      meal_type="main", location_id=location.id)
        side_meal_item = meal_item_repo.new_meal_item(name="side1",  image="image11",
                                                      meal_type="side", location_id=location.id)
        protein_meal_item = meal_item_repo.new_meal_item(name="protein1",  image="image12",
                                                         meal_type="protein", location_id=location.id)
        vendor = VendorFactory.build()
        vendor_engagement = VendorEngagementFactory.build(vendor_id=vendor.id)
        vendor_engagement.save()
        menu = MenuFactory.create(main_meal_id=main_meal_item.id,
                                  side_items=side_meal_item.id, protein_items=protein_meal_item.id, location=location)
        menu.save()
        data = {
            'date': menu.date.strftime('%Y-%m-%d'), 'mealPeriod': menu.meal_period,
            'mainMealId': main_meal_item.id, 'allowedSide': 2,
            'allowedProtein': 2, 'sideItems': [side_meal_item.id],
            'proteinItems': [protein_meal_item.id], 'vendorEngagementId': vendor_engagement.id
        }

        response = self.client().put(self.make_url('/admin/menus/{}'.format(menu.id)),
                                     data=self.encode_to_json_string(data), headers=self.headers())
        response_json = self.decode_from_json_string(response.data.decode('utf-8'))
        payload = response_json['payload']

        self.assert200(response)
        self.assertEqual(payload['menu']['allowedProtein'], data['allowedProtein'])
        self.assertEqual(payload['menu']['allowedSide'], data['allowedSide'])

    def test_update_menu_endpoint_with_deleted_menu(self):
        """Test update of a menu"""
        location = LocationFactory.create()
        role = RoleFactory.create(name='admin')
        user_id = BaseTestCase.user_id()
        PermissionFactory.create(keyword='update_menu', role=role)
        UserRoleFactory.create(user_id=user_id, role=role)

        meal_item_repo = MealItemRepo()

        main_meal_item = meal_item_repo.new_meal_item(name="main1", image="image1",
                                                      meal_type="main", location_id=location.id)
        side_meal_item = meal_item_repo.new_meal_item(name="side1",  image="image11",
                                                      meal_type="side", location_id=location.id)
        protein_meal_item = meal_item_repo.new_meal_item(name="protein1",  image="image12",
                                                         meal_type="protein", location_id=location.id)
        vendor = VendorFactory.build()
        vendor_engagement = VendorEngagementFactory.build(vendor_id=vendor.id)
        vendor_engagement.save()
        menu = MenuFactory.create(main_meal_id=main_meal_item.id,
                                  side_items=side_meal_item.id, protein_items=protein_meal_item.id)
        menu.is_deleted = True
        menu.save()

        data = {
            'date': menu.date.strftime('%Y-%m-%d'), 'mealPeriod': menu.meal_period,
            'mainMealId': main_meal_item.id, 'allowedSide': 2,
            'allowedProtein': 2, 'sideItems': [side_meal_item.id],
            'proteinItems': [protein_meal_item.id], 'vendorEngagementId': vendor_engagement.id
        }

        response = self.client().put(self.make_url('/admin/menus/{}'.format(menu.id)),
                                     data=self.encode_to_json_string(data), headers=self.headers())
        response_json = self.decode_from_json_string(response.data.decode('utf-8'))

        self.assert400(response)
        self.assertEqual(response_json['msg'], 'This menu is already deleted')

    def test_update_menu_endpoint_with_wrong_main_meal_values(self):
        location = LocationFactory.create()
        role = RoleFactory.create(name='admin')
        user_id = BaseTestCase.user_id()
        PermissionFactory.create(keyword='update_menu', role=role)
        UserRoleFactory.create(user_id=user_id, role=role)

        meal_item_repo = MealItemRepo()

        main_meal_item = meal_item_repo.new_meal_item(name="main1", image="image1",
                                                      meal_type="main", location_id=location.id)
        side_meal_item = meal_item_repo.new_meal_item(name="side1",  image="image11",
                                                      meal_type="side", location_id=location.id)
        protein_meal_item = meal_item_repo.new_meal_item(name="protein1",  image="image12",
                                                         meal_type="protein", location_id=location.id)

        vendor = VendorFactory.build()
        vendor_engagement = VendorEngagementFactory.build(vendor_id=vendor.id)
        vendor_engagement.save()

        menu = MenuFactory.create(main_meal_id=main_meal_item.id,
                                  side_items=side_meal_item.id, protein_items=protein_meal_item.id)
        menu.vendor_engagement_id = vendor_engagement.id
        menu.save()

        data = {
            'date': menu.date.strftime('%Y-%m-%d'), 'mealPeriod': menu.meal_period,
            'mainMealId': 1000, 'allowedSide': 2,
            'allowedProtein': 2, 'sideItems': [side_meal_item.id],
            'proteinItems': [protein_meal_item.id], 'vendorEngagementId': vendor_engagement.id
        }

        response = self.client().put(self.make_url('/admin/menus/{}'.format(menu.id)),
                                     data=self.encode_to_json_string(data), headers=self.headers())
        response_json = self.decode_from_json_string(response.data.decode('utf-8'))

        self.assert400(response)
        self.assertEqual(response_json['msg'], 'Bad Request - mainMealId contains invalid id(s) for meal_item table ')

    def test_update_menu_endpoint_with_wrong_side_item_values(self):
        location = LocationFactory.create()
        role = RoleFactory.create(name='admin')
        user_id = BaseTestCase.user_id()
        PermissionFactory.create(keyword='update_menu', role=role)
        UserRoleFactory.create(user_id=user_id, role=role)

        meal_item_repo = MealItemRepo()

        main_meal_item = meal_item_repo.new_meal_item(name="main1",image="image1",
                                                      meal_type="main", location_id=location.id)
        side_meal_item = meal_item_repo.new_meal_item(name="side1", image="image11",
                                                      meal_type="side", location_id=location.id)
        protein_meal_item = meal_item_repo.new_meal_item(name="protein1",image="image12",
                                                         meal_type="protein", location_id=location.id)

        vendor = VendorFactory.build()
        vendor_engagement = VendorEngagementFactory.build(vendor_id=vendor.id)
        vendor_engagement.save()

        menu = MenuFactory.create(main_meal_id=main_meal_item.id,
                                  side_items=side_meal_item.id, protein_items=protein_meal_item.id)
        menu.vendor_engagement_id = vendor_engagement.id
        menu.save()

        data = {
            'date': menu.date.strftime('%Y-%m-%d'), 'mealPeriod': menu.meal_period,
            'mainMealId': main_meal_item.id, 'allowedSide': 2,
            'allowedProtein': 2, 'sideItems': [10000],
            'proteinItems': [protein_meal_item.id], 'vendorEngagementId': vendor_engagement.id
        }

        response = self.client().put(self.make_url('/admin/menus/{}'.format(menu.id)),
                                     data=self.encode_to_json_string(data), headers=self.headers())
        response_json = self.decode_from_json_string(response.data.decode('utf-8'))

        self.assert400(response)
        self.assertEqual(response_json['msg'], 'Bad Request - sideItems contains invalid id(s) for meal_item table ')

    def test_update_menu_endpoint_with_wrong_protein_item_values(self):
        location = LocationFactory.create()
        role = RoleFactory.create(name='admin')
        user_id = BaseTestCase.user_id()
        PermissionFactory.create(keyword='update_menu', role=role)
        UserRoleFactory.create(user_id=user_id, role=role)

        meal_item_repo = MealItemRepo()

        main_meal_item = meal_item_repo.new_meal_item(name="main1", image="image1",
                                                      meal_type="main", location_id=location.id)
        side_meal_item = meal_item_repo.new_meal_item(name="side1",  image="image11",
                                                      meal_type="side", location_id=location.id)
        protein_meal_item = meal_item_repo.new_meal_item(name="protein1",  image="image12",
                                                         meal_type="protein", location_id=location.id)

        vendor = VendorFactory.build()
        vendor_engagement = VendorEngagementFactory.build(vendor_id=vendor.id)
        vendor_engagement.save()

        menu = MenuFactory.create(main_meal_id=main_meal_item.id,
                                  side_items=side_meal_item.id, protein_items=protein_meal_item.id)
        menu.vendor_engagement_id = vendor_engagement.id
        menu.save()

        data = {
            'date': menu.date.strftime('%Y-%m-%d'), 'mealPeriod': menu.meal_period,
            'mainMealId': main_meal_item.id, 'allowedSide': 2,
            'allowedProtein': 2, 'sideItems': [side_meal_item.id],
            'proteinItems': [1000], 'vendorEngagementId': vendor_engagement.id
        }

        response = self.client().put(self.make_url('/admin/menus/{}'.format(menu.id)),
                                     data=self.encode_to_json_string(data), headers=self.headers())
        response_json = self.decode_from_json_string(response.data.decode('utf-8'))

        self.assert400(response)
        self.assertEqual(response_json['msg'], 'Bad Request - proteinItems contains invalid id(s) for meal_item table ')

    def test_update_menu_endpoint_with_wrong_permission(self):
        location = LocationFactory.create()
        role = RoleFactory.create(name='admin')
        user_id = BaseTestCase.user_id()
        PermissionFactory.create(keyword='wrong_permission', role=role)
        UserRoleFactory.create(user_id=user_id, role=role)

        meal_item_repo = MealItemRepo()

        main_meal_item = meal_item_repo.new_meal_item(name="main1", image="image1",
                                                      meal_type="main", location_id=location.id)
        side_meal_item = meal_item_repo.new_meal_item(name="side1",  image="image11",
                                                      meal_type="side", location_id=location.id)
        protein_meal_item = meal_item_repo.new_meal_item(name="protein1",  image="image12",
                                                         meal_type="protein", location_id=location.id)

        vendor = VendorFactory.build()
        vendor_engagement = VendorEngagementFactory.build(vendor_id=vendor.id)
        vendor_engagement.save()

        menu = MenuFactory.create(main_meal_id=main_meal_item.id,
                                  side_items=side_meal_item.id, protein_items=protein_meal_item.id)
        menu.vendor_engagement_id = vendor_engagement.id
        menu.save()

        data = {
            'date': menu.date.strftime('%Y-%m-%d'), 'mealPeriod': menu.meal_period,
            'mainMealId': 10000, 'allowedSide': 2,
            'allowedProtein': 2, 'sideItems': [side_meal_item.id],
            'proteinItems': [protein_meal_item.id], 'vendorEngagementId': vendor_engagement.id
        }

        response = self.client().put(self.make_url('/admin/menus/{}'.format(menu.id)),
                                     data=self.encode_to_json_string(data), headers=self.headers())
        response_json = self.decode_from_json_string(response.data.decode('utf-8'))

        self.assert401(response)
        self.assertEqual(response_json['msg'], 'Access Error - Permission Denied')

    def test_update_menu_endpoint_with_wrong_menu_id(self):
        location = LocationFactory.create()
        role = RoleFactory.create(name='admin')
        user_id = BaseTestCase.user_id()
        PermissionFactory.create(keyword='update_menu', role=role)
        UserRoleFactory.create(user_id=user_id, role=role)

        meal_item_repo = MealItemRepo()

        main_meal_item = meal_item_repo.new_meal_item(name="main1", image="image1",
                                                      meal_type="main", location_id=location.id)
        side_meal_item = meal_item_repo.new_meal_item(name="side1",  image="image11",
                                                      meal_type="side", location_id=location.id)
        protein_meal_item = meal_item_repo.new_meal_item(name="protein1",  image="image12",
                                                         meal_type="protein", location_id=location.id)

        vendor = VendorFactory.build()
        vendor_engagement = VendorEngagementFactory.build(vendor_id=vendor.id)

        menu = MenuFactory.create(main_meal_id=main_meal_item.id,
                                  side_items=side_meal_item.id, protein_items=protein_meal_item.id)
        menu.vendor_engagement_id = vendor_engagement.id

        data = {
            'date': menu.date.strftime('%Y-%m-%d'), 'mealPeriod': menu.meal_period,
            'mainMealId': main_meal_item.id, 'allowedSide': 2,
            'allowedProtein': 2, 'sideItems': [side_meal_item.id],
            'proteinItems': [protein_meal_item.id], 'vendorEngagementId': vendor_engagement.id
        }

        response = self.client().put(self.make_url('/admin/menus/1000'), data=self.encode_to_json_string(data),
                                     headers=self.headers())
        response_json = self.decode_from_json_string(response.data.decode('utf-8'))

        self.assert404(response)
        self.assertEqual(response_json['msg'], 'This menu_id does not exist')

    def test_list_menu_range_endpoint_succeeds(self):
        location = LocationFactory.create()
        meal_item_repo = MealItemRepo()

        main_meal_item = meal_item_repo.new_meal_item(name="main1", image="image1",
                                                      meal_type="main", location_id=location.id)
        side_meal_item = meal_item_repo.new_meal_item(name="side1",  image="image11",
                                                      meal_type="side", location_id=location.id)
        protein_meal_item = meal_item_repo.new_meal_item(name="protein1",  image="image12",
                                                         meal_type="protein", location_id=location.id)
        headers = self.headers()
        headers.update({'X-Location': location.id})
        menu = MenuFactory.create(main_meal_id=main_meal_item.id,
                                  side_items=str(side_meal_item.id), protein_items=str(protein_meal_item.id), location=location)
        menu.save()
        start_date = menu.vendor_engagement.start_date - timedelta(days=1)

        response = self.client().get(self.make_url(f'/menus/{menu.meal_period}/{start_date}/{menu.vendor_engagement.end_date}'),
                                     headers=headers)

        response_json = self.decode_from_json_string(response.data.decode('utf-8'))
        self.assertEqual(response_json['msg'], 'OK')
        self.assertEqual(response_json['payload']['menuList'][0]['menus'][0]['id'], menu.id)

    def test_list_menu_endpoint_with_invalid_date_fails(self):
        """Test that users with the wrong date fails"""
        meal_item_repo = MealItemRepo()
        location = LocationFactory.create()

        main_meal_item = meal_item_repo.new_meal_item(name="main1", image="image1",
                                                        meal_type="main", location_id=location.id)
        side_meal_item = meal_item_repo.new_meal_item(name="side1",  image="image11",
                                                        meal_type="side", location_id=location.id)
        protein_meal_item = meal_item_repo.new_meal_item(name="protein1",  image="image12",
                                                            meal_type="protein", location_id=location.id)

        menu = MenuFactory.create(main_meal_id=main_meal_item.id,
                                    side_items=str(side_meal_item.id), protein_items=str(protein_meal_item.id))

        date ='201502-24'

        response = self.client().get(self.make_url(f'/menus/{menu.meal_period}/{date}/{date}'),
                                        headers=self.headers())
        self.assert400(response)