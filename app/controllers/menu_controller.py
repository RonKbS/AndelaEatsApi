from app.controllers.base_controller import BaseController
from app.repositories.menu_repo import MenuRepo
from app.repositories.meal_item_repo import MealItemRepo
from datetime import datetime


class MenuController(BaseController):
	def __init__(self, request):
		BaseController.__init__(self, request)
		self.menu_repo = MenuRepo()
		self.meal_repo = MealItemRepo()
    
	def create_menu(self):
		date, meal_period, main_meal_id, allowed_side, allowed_protein, side_items, protein_items, vendor_engagement_id = self.request_params(
			'date', 'mealPeriod', 'mainMealId', 'allowedSide',
			'allowedProtein', 'sideItems', 'proteinItems', 'vendorEngagementId'
		)
		menu = self.menu_repo.new_menu(
			date, meal_period, main_meal_id, allowed_side,
			allowed_protein, side_items, protein_items, vendor_engagement_id
		).serialize()
		menu['mainMeal'] = self.meal_repo.get(main_meal_id).serialize()
		menu['proteinItems'] = self.menu_repo.get_meal_items(protein_items)
		menu['sideItems'] = self.menu_repo.get_meal_items(side_items)
		return self.handle_response('OK', payload={'menu': menu}, status_code=201)

	def delete_menu(self, menu_id):
		menu = self.menu_repo.get(menu_id)
		updates = {}
		if menu:
			if menu.is_deleted:
				return self.handle_response('Menu has already been deleted', status_code=400)

			updates['is_deleted'] = True

			self.meal_repo.update(menu, **updates)
			return self.handle_response('Menu deleted', payload={"status": "success"})
		return self.handle_response('Invalid or incorrect menu_id provided', status_code=400)


	def list_menus(self, menu_period, menu_date):
		'''retrieves a list of menus for a specific date for a specific meal period.
		date fornat: "YYYY-MM-DD"
		'''
		menus = self.menu_repo.filter_by(date=menu_date, meal_period=menu_period)

		if menus:
			menu_list = []
			for menu in menus.items:
				serialised_menu = menu.serialize()
				proteins = self.menu_repo.get_meal_items(menu.protein_items)
				sides = self.menu_repo.get_meal_items(menu.side_items)

				serialised_menu['mainMeal'] = self.meal_repo.get(menu.main_meal_id).serialize()['name']
				serialised_menu['proteinItems'] = [protein['name'] for protein in proteins]
				serialised_menu['sideItems'] = [side['name'] for side in sides]		
				menu_list.append(serialised_menu)

			return self.handle_response('OK', payload={'dateOfMeal': menu_date, 'mealPeriod': menu_period, 'menuList': menu_list, 'meta': self.pagination_meta(menus)})

		return self.handle_response('Provide valid meal period and date')

	def update_menu(self, menu_id):
		date, meal_period, main_meal_id, allowed_side, allowed_protein, side_items, protein_items, vendor_engagement_id = self.request_params(
			'date', 'mealPeriod', 'mainMealId', 'allowedSide',
			'allowedProtein', 'sideItems', 'proteinItems', 'vendorEngagementId'
		)

		menu = self.menu_repo.get(menu_id)

		if menu:
			updates = {}
			updates['date'] = datetime.strptime(date, '%Y-%m-%d')
			updates['meal_period'] = meal_period
			updates['main_meal_id'] = main_meal_id
			updates['allowed_side'] = allowed_side
			updates['allowed_protein'] = allowed_protein
			updates['side_items'] = ','.join(str(item) for item in side_items)
			updates['protein_items'] = ','.join(str(item) for item in protein_items)
			updates['vendor_engagement_id'] = vendor_engagement_id

			self.menu_repo.update(menu, **updates)

			menu = menu.serialize()
			menu['mainMeal'] = self.meal_repo.get(main_meal_id).serialize()
			menu['proteinItems'] = self.menu_repo.get_meal_items(protein_items)
			menu['sideItems'] = self.menu_repo.get_meal_items(side_items)
			return self.handle_response('OK', payload={'menu': menu}, status_code=200)
    
		return self.handle_response('This menu_id does not exist', status_code=404)

