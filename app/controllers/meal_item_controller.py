from app.controllers.base_controller import BaseController
from app.repositories.meal_item_repo import MealItemRepo


class MealItemController(BaseController):
	
	def __init__(self, request):
		BaseController.__init__(self, request)
		self.meal_repo = MealItemRepo()
	
	def list_meals(self):
		meals = self.meal_repo.filter_by(is_deleted=False)
		meals_list = [meal.serialize() for meal in meals.items]
		return self.handle_response('OK', payload={'mealItems': meals_list, 'meta': self.pagination_meta(meals)})
	
	def get_meal(self, meal_id):
		meal = self.meal_repo.get(meal_id)
		if meal:
			meal = meal.serialize()
			return self.handle_response('OK', payload={'mealItem': meal})
		else:
			return self.handle_response('Bad Request', status_code=400)
	
	def create_meal(self):
		"""
		Creates a new meal item
		"""
		
		name, description, image_url, meal_type = self.request_params('mealName', 'description', 'image', 'mealType')

		new_meal_item = self.meal_repo.new_meal_item(name, description, image_url, meal_type).serialize()
		
		return self.handle_response('OK', payload={'mealItem': new_meal_item})
		

	def update_meal(self, meal_id):
		name, description, image_url, meal_type = self.request_params('mealName', 'description', 'image', 'mealType')

		meal = self.meal_repo.get(meal_id)
		if meal:
			updates = {}
			if name:
				updates['name'] = name
			if description:
				updates['description'] = description
			if image_url:
				updates['image'] = image_url
			if meal_type:
				updates['meal_type'] = meal_type
				
			self.meal_repo.update(meal, **updates)
			return self.handle_response('OK', payload={'mealItem': meal.serialize()})
		
		return self.handle_response('Invalid or incorrect meal_id provided', status_code=400)

	
	def delete_meal(self, meal_id):
		meal = self.meal_repo.get(meal_id)
		updates = {}
		if meal:
			updates['is_deleted'] = True
				
			self.meal_repo.update(meal, **updates)
			return self.handle_response('OK', payload={"status": "success"})
		return self.handle_response('Invalid or incorrect meal_id provided', status_code=400)