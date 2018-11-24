from app.blueprints.base_blueprint import Blueprint, BaseBlueprint, request, Security, Auth
from app.controllers.vendor_controller import VendorController
from app.utils.auth import Auth
from flasgger import swag_from

vendor_blueprint = Blueprint('vendor', __name__, url_prefix='{}/vendors'.format(BaseBlueprint.base_url_prefix))


vendor_controller = VendorController(request)


@vendor_blueprint.route('/', methods=['GET'])
@swag_from('documentation/get_all_vendors_per_page.yml')
def list_vendors():
	return vendor_controller.list_vendors()


@vendor_blueprint.route('/deleted/', methods=['GET'])
@swag_from('documentation/get_deleted_vendors_per_page.yml')
def list_deleted_vendors():
	return vendor_controller.list_deleted_vendors()


@vendor_blueprint.route('/suspended/', methods=['GET'])
@swag_from('documentation/get_suspended_vendors_per_page.yml')
def list_suspended_vendors():
	return vendor_controller.list_suspended_vendors()


@vendor_blueprint.route('/<int:vendor_id>', methods=['GET'])
@swag_from('documentation/get_vendor_by_id.yml')
def get_vendor(vendor_id):
	return vendor_controller.get_vendor(vendor_id)


@vendor_blueprint.route('/', methods=['POST'])
@Security.validator([
	'name|required', 'address|required', 'tel|required:int', 'isActive|required:boolean', 'contactPerson|required'])
@swag_from('documentation/create_vendor.yml')
def create_vendor():
	return vendor_controller.create_vendor()


@vendor_blueprint.route('/<int:vendor_id>', methods=['PUT', 'PATCH'])
@Security.validator([
	'name|required', 'address|required', 'tel|required:int', 'isActive|required:boolean', 'contactPerson|required'])
@swag_from('documentation/update_vendor.yml')
def update_vendor(vendor_id):
	return vendor_controller.update_vendor(vendor_id)


@vendor_blueprint.route('/un_suspend/<int:vendor_id>', methods=['PUT', 'PATCH'])
@swag_from('documentation/un_suspend_vendor.yml')
def un_suspend_vendor(vendor_id):
	return vendor_controller.un_suspend_vendor(vendor_id)


@vendor_blueprint.route('/suspend/<int:vendor_id>', methods=['PUT', 'PATCH'])
@swag_from('documentation/suspend_vendor.yml')
def suspend_vendor(vendor_id):
	return vendor_controller.suspend_vendor(vendor_id)


@vendor_blueprint.route('/<int:vendor_id>', methods=['DELETE'])
@Auth.has_permission('delete_vendor')
@swag_from('documentation/delete_vendor.yml')
def delete_vendor(vendor_id):
	return vendor_controller.delete_vendor(vendor_id)
