from app.blueprints.base_blueprint import Blueprint, BaseBlueprint, request, Security
from app.controllers.location_controller import LocationController
from flasgger import swag_from

url_prefix = '{}/locations'.format(BaseBlueprint.base_url_prefix)
location_blueprint = Blueprint('location', __name__, url_prefix=url_prefix)

location_controller = LocationController(request)


@location_blueprint.route('/', methods=['GET'])
@swag_from('documentation/get_all_locations.yml')
def list_locations():
	return location_controller.list_locations()


@location_blueprint.route('/<int:location_id>', methods=['GET'])
@swag_from('documentation/get_single_location.yml')
def get_location(location_id):
	return location_controller.get_location(location_id)


@location_blueprint.route('/', methods=['POST'])
@Security.validator(['name|required', 'zone|required'])
@swag_from('documentation/create_location.yml')
def create_location():
	return location_controller.create_location()


@location_blueprint.route('/<int:location_id>', methods=['PUT', 'PATCH'])
@Security.validator(['name|required', 'zone|required'])
@swag_from('documentation/update_location.yml')
def update_location(location_id):
	return location_controller.update_location(location_id)


@location_blueprint.route('/<int:location_id>', methods=['DELETE'])
@swag_from('documentation/delete_location.yml')
def delete_location(location_id):
	return location_controller.delete_location(location_id)