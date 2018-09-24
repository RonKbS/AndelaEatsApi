from app.blueprints.base_blueprint import Blueprint, BaseBlueprint, Security, request
from app.controllers.meal_controller import MealController

url_prefix = '{}/meal-items'.format(BaseBlueprint.base_url_prefix)
meal_blueprint = Blueprint('meal', __name__, url_prefix=url_prefix)
meal_controller = MealController(request)

@meal_blueprint.route('/', methods=['GET'])
def list_meals():
	return meal_controller.list_meals()

@meal_blueprint.route('/<int:meal_item_id>/', methods=['GET'])
def get_meal(meal_item_id):
	return meal_controller.get_meal(meal_item_id)

@meal_blueprint.route('/', methods=['POST'])
@Security.validator(['mealName|required:string', 'description|required:string', 'image|required', 'mealType|required'])
def create_meal():
	return meal_controller.create_meal()

@meal_blueprint.route('/<int:meal_item_id>/', methods=['PATCH', 'PUT'])
@Security.validator(['mealName|required:string', 'description|required:string', 'image|required', 'mealType|required'])
def update_meal(meal_item_id):
	return meal_controller.update_meal(meal_item_id)

@meal_blueprint.route('/<int:meal_item_id>/', methods=['DELETE'])
def delete_meal(meal_item_id):
	return meal_controller.delete_meal(meal_item_id)
