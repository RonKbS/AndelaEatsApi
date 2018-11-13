from app.blueprints.base_blueprint import Blueprint, BaseBlueprint, request, Security, Auth
from app.controllers.vendor_controller import VendorController
from app.utils.auth import Auth
from flasgger import swag_from

vendor_blueprint = Blueprint('vendor', __name__, url_prefix='{}/vendors'.format(BaseBlueprint.base_url_prefix))


vendor_controller = VendorController(request)


@vendor_blueprint.route('/<page_id>/<per_page>', methods=['GET'])
@swag_from('documentation/get_all_vendors_per_page.yml')
def list_vendors(page_id, per_page):
	return vendor_controller.list_vendors(page_id, per_page)


@vendor_blueprint.route('/<int:vendor_id>', methods=['GET'])
@swag_from('documentation/get_vendor_by_id.yml')
def get_vendor(vendor_id):
	return vendor_controller.get_vendor(vendor_id)


@vendor_blueprint.route('/', methods=['POST'])
@Security.validator(['name|required', 'address|required', 'tel|required:int', 'contactPerson|required'])
@swag_from('documentation/create_vendor.yml')
def create_vendor():
	return vendor_controller.create_vendor()


@vendor_blueprint.route('/<int:vendor_id>', methods=['PUT', 'PATCH'])
def update_vendor(vendor_id):
	return vendor_controller.update_vendor(vendor_id)


@vendor_blueprint.route('/<int:vendor_id>', methods=['DELETE'])
@Auth.has_permission('delete_vendor')
def delete_vendor(vendor_id):
	return vendor_controller.delete_vendor(vendor_id)
