from app.repositories.base_repo import BaseRepo
from app.models.meal import MealItem


class MealItemRepo(BaseRepo):
	
	def __init__(self):
		BaseRepo.__init__(self, MealItem)
	
	def new_meal_item(self, name, description, image, meal_type):
		meal_item = MealItem(meal_type=meal_type, name=name, description=description, image=image)
		meal_item.save()
		return meal_item

