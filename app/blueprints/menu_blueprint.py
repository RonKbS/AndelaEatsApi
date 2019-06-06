'''A module of menu blueprint'''
from app.blueprints.base_blueprint import Blueprint, BaseBlueprint, request, Security, Auth
from app.controllers.menu_controller import MenuController
from flasgger import swag_from

menu_blueprint = Blueprint('menu', __name__, url_prefix='{}/admin/menus'.format(BaseBlueprint.base_url_prefix))
user_menu_blueprint = Blueprint('user_menu', __name__, url_prefix='{}/menus'.format(BaseBlueprint.base_url_prefix))

menu_controller = MenuController(request)


"""Menu"""
@menu_blueprint.route('/', methods=['POST'])
@Security.validator([
	'date|required:date', 'mealPeriod|required',
	'mainMealId|required:int', 'allowedSide|required:int',
	'allowedProtein|required:int', 'sideItems|required:list_int',
	'proteinItems|required:list_int', 'vendorEngagementId|required:int',
	'sideItems|exists|meal_item|id', 'proteinItems|exists|meal_item|id',
	'mainMealId|exists|meal_item|id'
	])
@Auth.has_permission('create_menu')
@swag_from('documentation/create_menu.yml')
def create_menu():
	'''Blueprint function for creating a menu'''
	return menu_controller.create_menu()


@menu_blueprint.route('/<int:menu_id>', methods=['DELETE'])
@Auth.has_permission('delete_menu')
@swag_from('documentation/delete_menu.yml')
def delete_menu(menu_id):
	'''Blueprint function for deleting a menu'''
	return menu_controller.delete_menu(menu_id)


@menu_blueprint.route('/<meal_period>/<date:date>', methods=['GET'])
@Auth.has_permission('view_menu')
@swag_from('documentation/get_menu_period_single_date.yml')
def list_menu(meal_period, date):
	'''Blueprint function for fetching menus on a specific date'''
	return menu_controller.list_menus(meal_period, date)


@menu_blueprint.route('/<meal_period>/<date:start_date>/<date:end_date>', methods=['GET'])
@Auth.has_permission('view_menu')
@swag_from('documentation/get_admin_menu_period_date_range.yml')
def list_menu_range_admin(meal_period, start_date, end_date):
	"""Blueprint function for fetching paginated && unpaginated menu records between two dates for admin"""
	return menu_controller.list_menus_range_admin(meal_period, start_date, end_date)


@user_menu_blueprint.route('/<meal_period>/<date:start_date>/<date:end_date>', methods=['GET'])
@swag_from('documentation/get_menu_period_date_range.yml')
def list_menu_range(meal_period, start_date, end_date):
	"""Blueprint function for fetching paginated && unpaginated menu records between two dates for user"""
	return menu_controller.list_menus_range(meal_period, start_date, end_date)


@menu_blueprint.route('/<int:menu_id>', methods=['PATCH', 'PUT'])
@Auth.has_permission('update_menu')
@Security.validator([
	'sideItems|exists|meal_item|id',
	'proteinItems|exists|meal_item|id',
	'mainMealId|exists|meal_item|id'
	])
@swag_from('documentation/update_menu.yml')
def update_menu(menu_id):
	'''Blueprint function for updating a menu'''
	return menu_controller.update_menu(menu_id)
