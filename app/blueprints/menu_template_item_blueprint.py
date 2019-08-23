from app.blueprints.base_blueprint import (Auth, BaseBlueprint, Blueprint,
                                           request)
from app.controllers.menu_template_item_controller import MenuTemplateItemController
from app.utils.security import Security
from app.models import MenuTemplateItem
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
    'proteinItems|exists|meal_item|id|required', 'dayId|required'])
@swag_from('documentation/create_menu_template_item.yml', methods=['POST'])
def create_menu_template_item():
    return menu_template_item_controller.create()


@menu_template_item_blueprint.route('/', methods=['GET'])
@Security.validate_query_params(MenuTemplateItem)
@Auth.has_role('admin')
@swag_from('documentation/get_menu_template_items.yml', methods=['GET'])
def get_menu_template_items():
    return menu_template_item_controller.get_all()
@menu_template_item_blueprint.route('/<int:id>', methods=['DELETE'])
@Auth.has_role('admin')
@swag_from('documentation/delete_menu_template_item.yml')
def delete_menu(id):
    return menu_template_item_controller.delete(id)
