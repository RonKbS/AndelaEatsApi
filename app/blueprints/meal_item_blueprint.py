from app.blueprints.base_blueprint import Blueprint, BaseBlueprint, Security, request
from app.controllers.meal_item_controller import MealItemController
from flasgger import swag_from

url_prefix = '{}/meal-items'.format(BaseBlueprint.base_url_prefix)
meal_item_blueprint = Blueprint('meal_item', __name__, url_prefix=url_prefix)
meal_item_controller = MealItemController(request)

@meal_item_blueprint.route('/', methods=['GET'])
@swag_from('documentation/get_all_meal_items.yml')
def list_meals():
	return meal_item_controller.list_meals()


# @meal_item_blueprint.route('/page/<int:page_id>', methods=['GET'])
# @swag_from('documentation/get_all_meal_items_page.yml')
# def list_meals_page(page_id):
# 	meals_per_page = int(request.args.get('per_page')) if request.args.get('per_page') != None else 10
# 	return meal_item_controller.list_meals_page(page_id, meals_per_page)


@meal_item_blueprint.route('/<int:meal_item_id>', methods=['GET'])
@swag_from('documentation/get_single_meal_item.yml')
def get_meal(meal_item_id):
	return meal_item_controller.get_meal(meal_item_id)


@meal_item_blueprint.route('/', methods=['POST'])
@Security.validator(['mealName|required:string', 'description|required:string', 'image|required', 'mealType|required'])
@swag_from('documentation/create_single_meal_item.yml')
def create_meal():
	return meal_item_controller.create_meal()


@meal_item_blueprint.route('/<int:meal_item_id>', methods=['PATCH', 'PUT'])
@Security.validator(['mealName|required:string', 'description|required:string', 'image|required', 'mealType|required'])
@swag_from('documentation/update_single_meal_item.yml')
def update_meal(meal_item_id):
	return meal_item_controller.update_meal(meal_item_id)


@meal_item_blueprint.route('/<int:meal_item_id>', methods=['DELETE'])
@swag_from('documentation/delete_single_meal_item.yml')
def delete_meal(meal_item_id):
	return meal_item_controller.delete_meal(meal_item_id)
