'''A module of menu blueprint'''
from app.blueprints.base_blueprint import Blueprint, BaseBlueprint, request, Security, Auth
from app.controllers.menu_controller import MenuController
from flasgger import swag_from

menu_blueprint = Blueprint('menu', __name__, url_prefix='{}/admin/menus'.format(BaseBlueprint.base_url_prefix))

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
@swag_from('test_create_menu.yml')
def create_menu():
	'''Blueprint function for creating a menu'''
	return menu_controller.create_menu()

@menu_blueprint.route('/<int:menu_id>', methods=['DELETE'])
@Auth.has_permission('delete_menu')
def delete_menu(menu_id):
	'''Blueprint function for deleting a menu'''
	return menu_controller.delete_menu(menu_id)


@menu_blueprint.route('/<meal_period>/<date>', methods=['GET'])
@Auth.has_permission('view_menu')
def list_menu(meal_period, date):
	'''Blueprint function for fetching menus on a specific date'''
	return menu_controller.list_menus(meal_period, date)


@menu_blueprint.route('/<meal_period>/<start_date>/<end_date>/page/<int:page_id>', methods=['GET'])
@Auth.has_permission('view_menu')
def list_menu_range_page(meal_period, start_date, end_date, page_id):
	'''Blueprint function for fetching paginated menu records between two dates'''
	meals_per_page = int(request.args.get('per_page')) if request.args.get('per_page') != None else 10
	return menu_controller.list_menus_range_page(meal_period, start_date, end_date, page_id, meals_per_page)

@menu_blueprint.route('/<meal_period>/<start_date>/<end_date>', methods=['GET'])
@Auth.has_permission('view_menu')
def list_menu_range(meal_period, start_date, end_date):
	'''Blueprint function for fetching unpaginated menu records between two dates'''
	return menu_controller.list_menus_range(meal_period, start_date, end_date)


@menu_blueprint.route('/<int:menu_id>/', methods=['PATCH', 'PUT'])
@Auth.has_permission('create_menu')
@Security.validator([
	'sideItems|exists|meal_item|id',
	'proteinItems|exists|meal_item|id',
	'mainMealId|exists|meal_item|id'
	])
def update_menu(menu_id):
	'''Blueprint function for updating a menu'''
	return menu_controller.update_menu(menu_id)
