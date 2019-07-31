from app.repositories.base_repo import BaseRepo
from app.models.meal_item import MealItem


class MealItemRepo(BaseRepo):

    def __init__(self):
        BaseRepo.__init__(self, MealItem)

    def new_meal_item(self, name, image, meal_type, location_id):
        meal_item = MealItem(meal_type=meal_type, name=name, image=image, location_id=location_id)
        meal_item.save()
        return meal_item

    def get_meal_items_by_ids(self, ids):
        return self._model.query.filter(MealItem.id.in_(ids)).all()
