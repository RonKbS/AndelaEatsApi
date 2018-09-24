from app.blueprints.base_blueprint import Blueprint, BaseBlueprint, request, Security, Auth
from app.controllers.vendor_controller import VendorController
from app.utils.auth import Auth

vendor_blueprint = Blueprint('vendor', __name__, url_prefix='{}/vendors'.format(BaseBlueprint.base_url_prefix))
engagement_blueprint = Blueprint('engagements', __name__, url_prefix='{}/engagements'.format(BaseBlueprint.base_url_prefix))
rating_blueprint = Blueprint('rating', __name__, url_prefix='{}/ratings'.format(BaseBlueprint.base_url_prefix))

vendor_controller = VendorController(request)

'''VENDORS'''
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
@Security.validator(['name|required', 'address|required', 'tel|required:int', 'contactPerson|required' ])
def update_vendor(vendor_id):
	return vendor_controller.update_vendor(vendor_id)

@vendor_blueprint.route('/<int:vendor_id>', methods=['DELETE'])
def delete_vendor(vendor_id):
	return vendor_controller.delete_vendor(vendor_id)


'''VENDOR ENGAGEMENT'''
@engagement_blueprint.route('/', methods=['GET'])
def list_engagements():
	return vendor_controller.list_vendor_engagements()

@engagement_blueprint.route('/<int:engagement_id>', methods=['GET'])
def get_engagements(engagement_id):
	return vendor_controller.get_vendor_engagement(engagement_id)

@engagement_blueprint.route('/', methods=['POST'])
@Security.validator(['vendorId|required:int', 'startDate|required:date', 'endDate|required:date', 'status|int'])
def create_engagement():
	return vendor_controller.create_vendor_engagement()

@engagement_blueprint.route('/<int:engagement_id>', methods=['PUT', 'PATCH'])
@Security.validator(['vendorId|required:int', 'startDate|date', 'endDate|date', 'status|int', ])
def update_engagement(engagement_id):
	return vendor_controller.update_vendor_engagement(engagement_id)


'''VENDOR RATING'''
@rating_blueprint.route('/vendor/<int:vendor_id>', methods=['GET'])
@Auth.has_permission('view_ratings')
def list_ratings(vendor_id):
	'''Gets all the ratings for a given vendor'''
	return vendor_controller.list_ratings(vendor_id)


@rating_blueprint.route('/<int:rating_id>', methods=['GET'])
@Auth.has_permission('view_ratings')
def get_vendor_rating(rating_id):
	return vendor_controller.get_vendor_rating(rating_id)

@rating_blueprint.route('/', methods=['POST'])
@Security.validator(['vendor_id|required:int', 'rating|required:int'])
def create_vendor_rating():
	return vendor_controller.create_vendor_rating()

@rating_blueprint.route('/<int:rating_id>', methods=['PUT', 'PATCH'])
@Security.validator(['rating|int'])
def update_rating(rating_id):
	return vendor_controller.update_vendor_rating(rating_id)
