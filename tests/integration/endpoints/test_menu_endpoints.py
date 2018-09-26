from tests.base_test_case import BaseTestCase
from factories.menu_factory import MenuFactory
from factories.meal_item_factory import MealItemFactory
from factories.vendor_engagement_factory import VendorEngagementFactory
from factories.vendor_factory import VendorFactory
from app.utils import db


class MenuEndpoints(BaseTestCase):

  def setUp(self):
    self.BaseSetUp()

  def test_create_menu_endpoint(self):
    menu = MenuFactory.build()
    main_meal_item = MealItemFactory.build()
    side_meal_item = MealItemFactory.build()
    protein_meal_item = MealItemFactory.build()
    vendor = VendorFactory.build()
    db.session.add(vendor)
    db.session.commit()
    vendor_engagement = VendorEngagementFactory.build(vendor_id=vendor.id)
    db.session.add(vendor_engagement)
    db.session.add(main_meal_item)
    db.session.add(side_meal_item)
    db.session.add(protein_meal_item)
    db.session.commit()

    data = {
      'date': menu.date, 'mealPeriod': menu.meal_period,
      'mainMealId': main_meal_item.id, 'allowedSide': menu.allowed_side,
      'allowedProtein': menu.allowed_protein, 'sideItems': [side_meal_item.id],
      'proteinItems': [protein_meal_item.id], 'vendorEngagementId': vendor_engagement.id
    }

    response = self.client().post(self.make_url('/admin/menu/'), data=self.encode_to_json_string(data), headers=self.headers())
    response_json = self.decode_from_json_string(response.data.decode('utf-8'))
    payload = response_json['payload']

    self.assertEqual(response.status_code, 201)
    self.assertJSONKeysPresent(payload, 'menu')
    self.assertJSONKeysPresent(payload['menu'], 'mainMeal', 'proteinItems', 'sideItems', 'allowedProtein', 'allowedSide',
      'date', 'id', 'mealPeriod', 'timestamps', 'vendorEngagementId'
    )

    self.assertEqual(payload['menu']['vendorEngagementId'], vendor_engagement.id)
    self.assertEqual(payload['menu']['mealPeriod'], menu.meal_period)
    self.assertEqual(payload['menu']['mainMealId'], main_meal_item.id)
    self.assertEqual(payload['menu']['allowedSide'], menu.allowed_side)
    self.assertEqual(payload['menu']['allowedProtein'], menu.allowed_protein)