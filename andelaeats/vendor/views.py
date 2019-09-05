# -*- coding: utf-8 -*-
"""Vendor views."""
from flask import Blueprint, jsonify

blueprint = Blueprint("vendor", __name__, url_prefix="/vendors")


@blueprint.route("/")
def vendor():
    """List vendor."""
    return jsonify({"view": "Vendor"})
