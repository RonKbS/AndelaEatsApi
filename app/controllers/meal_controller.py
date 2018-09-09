from app.controllers.base_controller import BaseController

class MealController(BaseController):
	
	def __init__(self, request):
		BaseController.__init__(self, request)
	
	def list_meals(self):
		return self.handle_response(msg='This is the meals endpoint')
	
	
	def get_meal(self, meal_id):
		if self.missing_required(['meal_id']):
			self.missing_response()
		return self.handle_response('This is the single meal endpoint. ID:{}'.format(meal_id))
	
	def create_meal(self):
		pass
	
	def update_meal(self, meal_id):
		pass
	
	def delete_meal(self, meal_id):
		pass