from app.blueprints.base_blueprint import Blueprint, BaseBlueprint, request, Security
from app.controllers.location_controller import LocationController

url_prefix = '{}/locations'.format(BaseBlueprint.base_url_prefix)
location_blueprint = Blueprint('location', __name__, url_prefix=url_prefix)

location_controller = LocationController(request)

@location_blueprint.route('/', methods=['GET'])
def list_locations():
	return location_controller.list_locations()

@location_blueprint.route('/<int:location_id>', methods=['GET'])
def get_location(location_id):
	return location_controller.get_location(location_id)

@location_blueprint.route('/', methods=['POST'])
@Security.validator(['name|required'])
def create_location():
	return location_controller.create_location()

@location_blueprint.route('/<int:location_id>', methods=['PUT', 'PATCH'])
@Security.validator(['name|required'])
def update_location(location_id):
	return location_controller.update_location(location_id)

@location_blueprint.route('/<int:location_id>', methods=['GET'])
def delete_location(location_id):
	return location_controller.delete_location(location_id)