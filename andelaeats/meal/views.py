# -*- coding: utf-8 -*-
"""Meal views."""
from flask import Blueprint, jsonify

blueprint = Blueprint('meal', __name__, url_prefix='/meals')


@blueprint.route('/')
def meal():
    """List meal."""
    return jsonify({'view': 'Meal'})
