# -*- coding: utf-8 -*-
"""Order views."""
from flask import Blueprint, jsonify
from flask.views import MethodView

from .models import Order
from .schema import OrderSchema

blueprint = Blueprint("order", __name__, url_prefix="/orders")


class OrdersView(MethodView):
    def get(self):
        orders = Order.query.all()
        schema = OrderSchema(many=True)
        return jsonify(schema.dump(orders))


class OrderView(MethodView):
    def get(self, id):
        order = Order.get(id)
        schema = OrderSchema()
        return jsonify(schema.dump(order))


blueprint.add_url_rule("/", view_func=OrdersView.as_view("orders"))
blueprint.add_url_rule("/<id>", view_func=OrderView.as_view("order"))
