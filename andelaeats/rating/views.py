# -*- coding: utf-8 -*-
"""Rating views."""
from flask import Blueprint, jsonify

blueprint = Blueprint("rating", __name__, url_prefix="/ratings")


@blueprint.route("/")
def rating():
    """List ratings."""
    return jsonify({"view": "Rating"})
