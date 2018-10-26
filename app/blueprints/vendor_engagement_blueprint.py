from app.blueprints.base_blueprint import Blueprint, BaseBlueprint, request, Security, Auth
from app.controllers.vendor_engagement_controller import VendorEngagementController

engagement_blueprint = Blueprint('engagements', __name__, url_prefix='{}/engagements'.format(BaseBlueprint.base_url_prefix))


vendor_engagement_controller = VendorEngagementController(request)

@engagement_blueprint.route('/', methods=['GET'])
def list_engagements():
	return vendor_engagement_controller.list_vendor_engagements()

@engagement_blueprint.route('/upcoming', methods=['GET'])
def upcoming_engagements():
	return vendor_engagement_controller.upcoming_vendor_engagements()

@engagement_blueprint.route('/<int:engagement_id>', methods=['GET'])
def get_engagements(engagement_id):
	return vendor_engagement_controller.get_vendor_engagement(engagement_id)

@engagement_blueprint.route('/', methods=['POST'])
@Security.validator(['vendorId|required:int', 'startDate|required:date', 'endDate|required:date', 'status|int'])
def create_engagement():
	return vendor_engagement_controller.create_vendor_engagement()

@engagement_blueprint.route('/<int:engagement_id>', methods=['PUT', 'PATCH'])
def update_engagement(engagement_id):
	return vendor_engagement_controller.update_vendor_engagement(engagement_id)

@engagement_blueprint.route('/<int:engagement_id>', methods=['DELETE'])
@Auth.has_permission('delete_engagement')
def delete_engagement(engagement_id):
	return vendor_engagement_controller.delete_engagement(engagement_id)
