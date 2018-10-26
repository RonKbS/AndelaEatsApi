from app.blueprints.base_blueprint import Blueprint, BaseBlueprint, request, Security, Auth
from app.controllers.vendor_controller import VendorController
from app.utils.auth import Auth

vendor_blueprint = Blueprint('vendor', __name__, url_prefix='{}/vendors'.format(BaseBlueprint.base_url_prefix))
engagement_blueprint = Blueprint('engagements', __name__, url_prefix='{}/engagements'.format(BaseBlueprint.base_url_prefix))
rating_blueprint = Blueprint('rating', __name__, url_prefix='{}/ratings'.format(BaseBlueprint.base_url_prefix))

vendor_controller = VendorController(request)

@vendor_blueprint.route('/', methods=['GET'])
def list_vendors():
	return vendor_controller.list_vendors()

@vendor_blueprint.route('/<int:vendor_id>', methods=['GET'])
def get_vendor(vendor_id):
	return vendor_controller.get_vendor(vendor_id)

@vendor_blueprint.route('/', methods=['POST'])
@Security.validator(['name|required', 'address|required', 'tel|required:int', 'contactPerson|required' ])
def create_vendor():
	return vendor_controller.create_vendor()

@vendor_blueprint.route('/<int:vendor_id>', methods=['PUT', 'PATCH'])
def update_vendor(vendor_id):
	return vendor_controller.update_vendor(vendor_id)

@vendor_blueprint.route('/<int:vendor_id>', methods=['DELETE'])
@Auth.has_permission('delete_vendor')
def delete_vendor(vendor_id):
	return vendor_controller.delete_vendor(vendor_id)
