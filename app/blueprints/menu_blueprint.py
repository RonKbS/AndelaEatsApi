from app.blueprints.base_blueprint import Blueprint, BaseBlueprint, request, Security, Auth
from app.controllers.menu_controller import MenuController
from app.utils.auth import Auth



menu_blueprint = Blueprint('menu', __name__, url_prefix='{}/admin/menu'.format(BaseBlueprint.base_url_prefix))

menu_controller = MenuController(request)


"""Menu"""
@menu_blueprint.route('/', methods=['POST'])
@Security.validator([
	'date|required:date', 'mealPeriod|required',
	'mainMealId|required:int', 'allowedSide|required:int',
	'allowedProtein|required:int', 'sideItems|required:list',
	'proteinItems|required:list', 'vendorEngagementId|required:int'
	])
def create_menu():
	return menu_controller.create_menu()

@menu_blueprint.route('/<int:menu_id>', methods=['DELETE'])
@Auth.has_permission('delete_menu')
def delete_menu(menu_id):
	return menu_controller.delete_menu(menu_id)
