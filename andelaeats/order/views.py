# -*- coding: utf-8 -*-
"""Order views."""
from flask import Blueprint, jsonify
from flask.views import MethodView

from ..utils.mixins import ModelListCreateMixin, RetrieveDeleteMixin
from .models import Order
from .schema import OrderSchema

blueprint = Blueprint("order", __name__, url_prefix="/orders")


class OrdersView(MethodView, ModelListCreateMixin):
    model = Order
    schema = OrderSchema


class OrderView(MethodView, RetrieveDeleteMixin):
    model = Order
    schema = OrderSchema


blueprint.add_url_rule("/", view_func=OrdersView.as_view("orders"))
blueprint.add_url_rule("/<string:uuid>", view_func=OrderView.as_view("order"))
