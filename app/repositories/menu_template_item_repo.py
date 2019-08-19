from app.models.menu_template import MenuTemplateItem, MenuTemplateWeekDay
from app.repositories import BaseRepo


class MenuTemplateItemRepo(BaseRepo):

    def __init__(self):
        BaseRepo.__init__(self, MenuTemplateItem)

    def create(self, *args):
        main_meal_id, allowed_side, allowed_protein, protein_items, side_items, day_id = args
        menu_template_item = MenuTemplateItem(
            main_meal_id=main_meal_id, allowed_side=allowed_side,
            allowed_protein=allowed_protein, protein_items=protein_items, 
            side_items=side_items, day_id=day_id)
        menu_template_item.save()
        return menu_template_item

    def get_menu_template_items_by_day(self, day_id):
        return self._model.query.filter_by(
            day_id=day_id
        ).paginate(error_out=False)
