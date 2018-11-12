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

@order_blueprint.route('/<int:order_id>', methods=['GET'])
def get_order(order_id):
    return order_controller.get_order(order_id)

@order_blueprint.route('/', methods=['POST'])
@Security.validator(['dateBookedFor|required:string', 'channel|string', 'mealItems|required:list_int'])
@swag_from('documentation/create_order.yml')
def create_order():
    return order_controller.create_order()

@order_blueprint.route('/<int:order_id>', methods=['PUT'])
@Security.validator(['dateBookedFor|required:date', 'channel|string', 'mealItems|required:list_int'])
def update_order(order_id):
    return order_controller.update_order(order_id)

@order_blueprint.route('/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    return order_controller.delete_order(order_id)
