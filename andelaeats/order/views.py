# -*- coding: utf-8 -*-
"""Order views."""
from flask import Blueprint, jsonify

blueprint = Blueprint("order", __name__, url_prefix="/orders")


@blueprint.route("/")
def order():
    """List order."""
    return jsonify({"view": "Order"})
