from flasgger import swag_from

from app.blueprints.base_blueprint import Blueprint, BaseBlueprint, request, Security, Auth
from app.controllers.vendor_rating_controller import VendorRatingController
from app.utils.auth import Auth

rating_blueprint = Blueprint('rating', __name__, url_prefix='{}/ratings'.format(BaseBlueprint.base_url_prefix))

vendor_rating_controller = VendorRatingController(request)


@rating_blueprint.route('/<menu_date>', methods=['GET'])
@Auth.has_permission('view_ratings')
@swag_from('documentation/get_vendor_ratings.yml')
def list_ratings(menu_date):
    """Gets all the ratings"""
    return vendor_rating_controller.list_ratings(menu_date)


@rating_blueprint.route('/<int:rating_id>', methods=['GET'])
@Auth.has_permission('view_ratings')
@swag_from('documentation/get_vendor_rating_by_id.yml')
def get_vendor_rating(rating_id):
    return vendor_rating_controller.get_vendor_rating(rating_id)


@rating_blueprint.route('/', methods=['POST'])
@Security.validator(['rating|required:int', 'engagementId|required:int', 'serviceDate|required'])
@swag_from('documentation/create_vendor_rating.yml')
def create_vendor_rating():
    return vendor_rating_controller.create_vendor_rating()


@rating_blueprint.route('/order/', methods=['POST'])
@Security.validator(['rating|required:int', 'engagementId|required:int', 'mainMealId|required:int', 'serviceDate|required'])
@swag_from('documentation/create_order_rating.yml')
def create_order_rating():
    return vendor_rating_controller.create_order_rating()


@rating_blueprint.route('/<int:rating_id>', methods=['PUT', 'PATCH'])
@Security.validator(['rating|int'])
@swag_from('documentation/update_vendor_rating.yml')
def update_rating(rating_id):
    return vendor_rating_controller.update_vendor_rating(rating_id)
