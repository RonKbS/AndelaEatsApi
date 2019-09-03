from app.models.menu_template import MenuTemplate
from app.repositories import BaseRepo


class MenuTemplateRepo(BaseRepo):

    _model = MenuTemplate

    def create(self, name, location_id, meal_period, description):
        menu_template = MenuTemplate(
            name=name, location_id=location_id, meal_period=meal_period, description=description)
        menu_template.save()
        return menu_template
