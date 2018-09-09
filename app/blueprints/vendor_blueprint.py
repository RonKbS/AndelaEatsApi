from app.blueprints.base_blueprint import Blueprint, BaseBlueprint, request, Security
from app.controllers.vendor_controller import VendorController

vendor_blueprint = Blueprint('vendor', __name__, url_prefix='{}/vendors'.format(BaseBlueprint.base_url_prefix))
engagement_blueprint = Blueprint('engagements', __name__, url_prefix='{}/engagements'.format(BaseBlueprint.base_url_prefix))

vendor_controller = VendorController(request)

@vendor_blueprint.route('/', methods=['GET'])
def list_vendors():
	return vendor_controller.list_vendors()

@vendor_blueprint.route('/<int:vendor_id>', methods=['GET'])
def get_vendor(vendor_id):
	return vendor_controller.get_vendor(vendor_id)

@vendor_blueprint.route('/', methods=['POST'])
@Security.validator(['name|required', 'address|required', 'tel|required:int', 'contact_person|required' ])
def create_vendor():
	return vendor_controller.create_vendor()

@vendor_blueprint.route('/<int:vendor_id>', methods=['PUT', 'PATCH'])
@Security.validator(['name|required', 'address|required', 'tel|required:int', 'contact_person|required' ])
def update_vendor(vendor_id):
	return vendor_controller.update_vendor(vendor_id)

@vendor_blueprint.route('/<int:vendor_id>', methods=['DELETE'])
def delete_vendor(vendor_id):
	return vendor_controller.delete_vendor(vendor_id)



@engagement_blueprint.route('/', methods=['GET'])
def list_engagements():
	return vendor_controller.list_vendor_engagements()

@engagement_blueprint.route('/<int:engagement_id>', methods=['GET'])
def get_engagements(engagement_id):
	return vendor_controller.get_vendor_engagement(engagement_id)

@engagement_blueprint.route('/', methods=['POST'])
@Security.validator(['vendor_id|required:int', 'start_date|required:date', 'end_date|required:date', 'status|int'])
def create_engagement():
	return vendor_controller.create_vendor_engagement()

@engagement_blueprint.route('/<int:engagement_id>', methods=['PUT', 'PATCH'])
@Security.validator(['vendor_id|required:int', 'start_date|date', 'end_date|date', 'status|int', ])
def update_engagement(engagement_id):
	return vendor_controller.update_vendor_engagement(engagement_id)