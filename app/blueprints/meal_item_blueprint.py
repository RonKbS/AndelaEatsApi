from app.blueprints.base_blueprint import Blueprint, BaseBlueprint, Security, request
from app.controllers.meal_item_controller import MealItemController

url_prefix = '{}/meal-items'.format(BaseBlueprint.base_url_prefix)
meal_item_blueprint = Blueprint('meal_item', __name__, url_prefix=url_prefix)
meal_item_controller = MealItemController(request)

@meal_item_blueprint.route('/', methods=['GET'])
def list_meals():
	return meal_item_controller.list_meals()

@meal_item_blueprint.route('/page/<int:page_id>', methods=['GET'])
def list_meals_page(page_id):
	meals_per_page = int(request.args.get('per_page')) if request.args.get('per_page') != None else 10
	return meal_item_controller.list_meals_page(page_id, meals_per_page)

@meal_item_blueprint.route('/<int:meal_item_id>/', methods=['GET'])
def get_meal(meal_item_id):
	return meal_item_controller.get_meal(meal_item_id)

@meal_item_blueprint.route('/', methods=['POST'])
@Security.validator(['mealName|required:string', 'description|required:string', 'image|required', 'mealType|required'])
def create_meal():
	return meal_item_controller.create_meal()

@meal_item_blueprint.route('/<int:meal_item_id>/', methods=['PATCH', 'PUT'])
@Security.validator(['mealName|required:string', 'description|required:string', 'image|required', 'mealType|required'])
def update_meal(meal_item_id):
	return meal_item_controller.update_meal(meal_item_id)

@meal_item_blueprint.route('/<int:meal_item_id>/', methods=['DELETE'])
def delete_meal(meal_item_id):
	return meal_item_controller.delete_meal(meal_item_id)
