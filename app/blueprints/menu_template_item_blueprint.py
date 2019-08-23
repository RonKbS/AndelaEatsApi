from app.blueprints.base_blueprint import (Auth, BaseBlueprint, Blueprint,
                                           request)
from app.controllers.menu_template_item_controller import MenuTemplateItemController
from app.utils.security import Security
from flasgger import swag_from

url_prefix = '{}/menu_template_items'.format(BaseBlueprint.base_url_prefix)

menu_template_item_blueprint = Blueprint(
    'menu_template_item', __name__, url_prefix=url_prefix)
menu_template_item_controller = MenuTemplateItemController(request)


@menu_template_item_blueprint.route('/', methods=['POST'])
@Auth.has_role('admin')
@Security.validator([
    'mainMealId|required', 'allowedSide|required:int',
    'allowedProtein|required', 'sideItems|exists|meal_item|id|required',
    'proteinItems|exists|meal_item|id|required','dayId|required'])
@swag_from('documentation/create_menu_template_item.yml')
def create_menu_template_item():
    return menu_template_item_controller.create()
