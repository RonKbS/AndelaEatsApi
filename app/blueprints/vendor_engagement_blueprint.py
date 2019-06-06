from app.blueprints.base_blueprint import Blueprint, BaseBlueprint, request, Security, Auth
from app.controllers.vendor_engagement_controller import VendorEngagementController
from flasgger import swag_from

engagement_blueprint = Blueprint('engagements', __name__,
                                 url_prefix='{}/engagements'.format(BaseBlueprint.base_url_prefix))

vendor_engagement_controller = VendorEngagementController(request)


@engagement_blueprint.route('/', methods=['GET'])
@swag_from('documentation/get_all_vendor_engagements.yml')
def list_engagements():
    return vendor_engagement_controller.list_vendor_engagements()


@engagement_blueprint.route('/vendor/<int:vendor_id>', methods=['GET'])
@swag_from('documentation/get_all_vendor_engagements_by_vendor_id.yml')
def list_engagements_by_vendor(vendor_id):
    return vendor_engagement_controller.list_vendor_engagements_by_vendor(vendor_id)


@engagement_blueprint.route('/upcoming', methods=['GET'])
@swag_from('documentation/get_all_upcoming_vendor_engagement.yml')
def upcoming_engagements():
    return vendor_engagement_controller.upcoming_vendor_engagements()


@engagement_blueprint.route('/<int:engagement_id>', methods=['GET'])
@swag_from('documentation/get_vendor_engagement_by_id.yml')
def get_engagements(engagement_id):
    return vendor_engagement_controller.get_vendor_engagement(engagement_id)


@engagement_blueprint.route('/', methods=['POST'])
@Security.validator(['vendorId|required:int', 'startDate|required:date', 'endDate|required:date', 'status|int'])
@swag_from('documentation/create_engagement.yml')
def create_engagement():
    return vendor_engagement_controller.create_vendor_engagement()


@engagement_blueprint.route('/<int:engagement_id>', methods=['PUT', 'PATCH'])
@swag_from('documentation/update_engagement.yml')
def update_engagement(engagement_id):
    return vendor_engagement_controller.update_vendor_engagement(engagement_id)


@engagement_blueprint.route('/<int:engagement_id>', methods=['DELETE'])
@Auth.has_permission('delete_engagement')
@swag_from('documentation/delete_engagement.yml')
def delete_engagement(engagement_id):
    return vendor_engagement_controller.delete_engagement(engagement_id)


@engagement_blueprint.route('/past/<int:location_id>', methods=['GET'])
@swag_from('documentation/immediate_past_vendor.yml')
def immediate_past_engagements(location_id):
    return vendor_engagement_controller.immediate_past_engagement(location_id)
