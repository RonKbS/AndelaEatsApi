from app.blueprints.base_blueprint import Blueprint, BaseBlueprint, request, Security, Auth
from app.controllers.vendor_rating_controller import VendorRatingController
from app.utils.auth import Auth

rating_blueprint = Blueprint('rating', __name__, url_prefix='{}/ratings'.format(BaseBlueprint.base_url_prefix))

vendor_rating_controller = VendorRatingController(request)

@rating_blueprint.route('/vendor/<int:vendor_id>', methods=['GET'])
@Auth.has_permission('view_ratings')
def list_ratings(vendor_id):
	'''Gets all the ratings for a given vendor'''
	return vendor_rating_controller.list_ratings(vendor_id)


@rating_blueprint.route('/<int:rating_id>', methods=['GET'])
@Auth.has_permission('view_ratings')
def get_vendor_rating(rating_id):
	return vendor_rating_controller.get_vendor_rating(rating_id)

@rating_blueprint.route('/', methods=['POST'])
@Security.validator(['vendor_id|required:int', 'rating|required:int'])
def create_vendor_rating():
	return vendor_rating_controller.create_vendor_rating()

@rating_blueprint.route('/<int:rating_id>', methods=['PUT', 'PATCH'])
@Security.validator(['rating|int'])
def update_rating(rating_id):
	return vendor_rating_controller.update_vendor_rating(rating_id)