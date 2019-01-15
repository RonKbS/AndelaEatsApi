from app import Auth
from app.controllers.base_controller import BaseController
from app.repositories.meal_item_repo import MealItemRepo
from app.utils.enums import MealTypes


class MealItemController(BaseController):
    
    def __init__(self, request):
        BaseController.__init__(self, request)
        self.meal_repo = MealItemRepo()
    
    def list_meals(self):
        location_id = Auth.get_location()
        meals = self.meal_repo.get_unpaginated(is_deleted=False, location_id=location_id)
        meals_list = [meal.serialize() for meal in meals]
        return self.handle_response('OK', payload={'mealItems': meals_list})

    def list_meals_page(self, page_id, meals_per_page):
        location_id = Auth.get_location()
        meals = self.meal_repo.filter_by(page=page_id, per_page=meals_per_page, location_id=location_id)
        meals_list = [meal.serialize() for meal in meals.items]
        return self.handle_response('OK', payload={'mealItems': meals_list, 'meta': self.pagination_meta(meals)})
    
    def get_meal(self, meal_id):
        meal = self.meal_repo.get(meal_id)
        if meal:
            if meal.is_deleted:
                return self.handle_response('Bad Request. This meal item is deleted', status_code=400)
            meal = meal.serialize()
            return self.handle_response('OK', payload={'mealItem': meal})
        else:
            return self.handle_response('Bad Request. This meal id does not exist', status_code=400)
    
    def create_meal(self):
        """
        Creates a new meal item
        """
        location_id = Auth.get_location()
        name, description, image_url, meal_type = self.request_params('mealName', 'description', 'image', 'mealType')
        if self.meal_repo.get_unpaginated(name=name, location_id=location_id):
            return self.handle_response('Meal item with this name already exists', status_code=400)
        if MealTypes.has_value(meal_type):
            new_meal_item = self.meal_repo.new_meal_item(name, description, image_url, meal_type, location_id).serialize()
        
            return self.handle_response('OK', payload={'mealItem': new_meal_item}, status_code=201)
        return self.handle_response('Invalid meal type. Must be main, protein or side', status_code=400)
        

    def update_meal(self, meal_id):
        name, description, image_url, meal_type = self.request_params('mealName', 'description', 'image', 'mealType')

        meal = self.meal_repo.get(meal_id)
        if meal:
            if meal.is_deleted:
                return self.handle_response('Bad Request. This meal item is deleted', status_code=400)

            updates = {}
            if name:
                if self.meal_repo.get_unpaginated(name=name):
                    return self.handle_response('Meal item with this name already exists', status_code=400)
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
            if meal.is_deleted:
                return self.handle_response('Bad Request. This meal item is deleted', status_code=400)
            updates['is_deleted'] = True

            self.meal_repo.update(meal, **updates)
            return self.handle_response('OK', payload={"status": "success"})
        return self.handle_response('Invalid or incorrect meal_id provided', status_code=400)