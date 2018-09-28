from app.repositories.base_repo import BaseRepo
from app.models.menu import Menu
from app.repositories.meal_item_repo import MealItemRepo
from datetime import datetime


class MenuRepo(BaseRepo):

  def __init__(self):
    BaseRepo.__init__(self, Menu)
    self.meal_repo = MealItemRepo()

  def new_menu(self, date, meal_period, main_meal_id, allowed_side, allowed_protein,
    side_items, protein_items, vendor_engagement_id):
    date = datetime.strptime(date, '%Y-%m-%d')
    menu = Menu(
      date=date, meal_period=meal_period,
      main_meal_id=main_meal_id, allowed_side=allowed_side,
      allowed_protein=allowed_protein, side_items=','.join(str(item) for item in side_items),
      protein_items=','.join(str(item) for item in protein_items), vendor_engagement_id=vendor_engagement_id
    )
    menu.save()
    return menu

  def get_meal_items(self, meal_ids):
    meal_items = []
    for id in meal_ids:
      item = self.meal_repo.get(id).serialize()
      meal_items.append(item)
    return meal_items