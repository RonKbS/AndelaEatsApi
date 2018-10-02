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
			updates['is_deleted'] = True

			self.meal_repo.update(menu, **updates)
			return self.handle_response('OK', payload={"status": "success"})
		return self.handle_response('Invalid or incorrect menu_id provided', status_code=400)

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
