from app.blueprints.base_blueprint import Blueprint, BaseBlueprint, Security, request
from app.controllers.order_controller import OrderController
from app.utils.auth import Auth
from flasgger import swag_from

url_prefix = '{}/orders'.format(BaseBlueprint.base_url_prefix)
order_blueprint = Blueprint('order', __name__, url_prefix=url_prefix)
order_controller = OrderController(request)


@order_blueprint.route('/', methods=['GET'])
@Auth.has_permission('view_orders')
@swag_from('documentation/get_all_orders.yml')
def list_order():
	return order_controller.list_orders()


@order_blueprint.route('/<start_date>', methods=['GET'])
@Auth.has_permission('view_orders')
@swag_from('documentation/get_orders_by_date.yml')
def list_orders_date(start_date):
	return order_controller.list_orders_date(start_date)


@order_blueprint.route('/<int:order_id>', methods=['GET'])
@swag_from('documentation/get_order_by_id.yml')
def get_order(order_id):
	return order_controller.get_order(order_id)


@order_blueprint.route('/user/<string:user_id>', methods=['GET'])
@swag_from('documentation/get_order_by_user_id.yml')
def get_order_by_user_id(user_id):
	return order_controller.get_order_by_user_id(user_id)


@order_blueprint.route('/user/<string:user_id>/<start_date>/<end_date>', methods=['GET'])
@swag_from('documentation/get_order_by_user_id_date_range.yml')
def get_order_by_user_id_date_range(user_id, start_date, end_date):
	return order_controller.get_order_by_user_id_date_range(user_id, start_date, end_date)


@order_blueprint.route('/check', methods=['POST'])
@Security.validator(['user_id|required:string', 'order_type|required:string', 'order_date|required:string'])
def check_order():
	return order_controller.check_order()


@order_blueprint.route('/collect', methods=['POST'])
@Security.validator(['user_id|required:string', 'order_type|required:string', 'order_date|required:string'])
def collect_order():
	return order_controller.collect_order()


@order_blueprint.route('/', methods=['POST'])
@Security.validator([
	'dateBookedFor|required:string', 'channel|required:string',
	'mealPeriod|required:string', 'mealItems|required:list_int'
])
@swag_from('documentation/create_order.yml')
def create_order():
	return order_controller.create_order()


@order_blueprint.route('/<int:order_id>', methods=['PUT'])
@Security.validator([
	'dateBookedFor|required:date', 'channel|string',
	'mealPeriod|required:string', 'mealItems|required:list_int'])
@swag_from('documentation/update_order.yml')
def update_order(order_id):
	return order_controller.update_order(order_id)


@order_blueprint.route('/<int:order_id>', methods=['DELETE'])
@swag_from('documentation/delete_single_order.yml')
def delete_order(order_id):
	return order_controller.delete_order(order_id)
