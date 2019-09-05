# -*- coding: utf-8 -*-
"""Rating views."""
from flask import Blueprint, jsonify

blueprint = Blueprint("location", __name__, url_prefix="/locations")


@blueprint.route("/")
def location():
    """List location."""
    return jsonify({"view": "Location"})
