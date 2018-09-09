from app.blueprints.base_blueprint import Blueprint, BaseBlueprint, request
from app.controllers.meal_controller import MealController

url_prefix = '{}/meals'.format(BaseBlueprint.base_url_prefix)
meal_blueprint = Blueprint('meal', __name__, url_prefix=url_prefix)
meal_controller = MealController(request)

@meal_blueprint.route('/', methods=['GET'])
def list_meals():
	return meal_controller.list_meals()

@meal_blueprint.route('/<int:meal_id>/', methods=['GET'])
def get_meal(meal_id):
	return meal_controller.get_meal(meal_id)

@meal_blueprint.route('/', methods=['POST'])
def create_meal():
	return meal_controller.create_meal()

@meal_blueprint.route('/<int:meal_id>/', methods=['PATCH', 'PUT'])
def update_meal(meal_id):
	return meal_controller.update_meal(meal_id)

@meal_blueprint.route('/<int:meal_id>/', methods=['DELETE'])
def delete_meal(meal_id):
	return meal_controller.delete_meal(meal_id)

