# -*- coding: utf-8 -*-
"""User views."""
from flask import Blueprint, jsonify

# from flask_login import login_required
from .models import User
from .schema import UserSchema

blueprint = Blueprint("user", __name__, url_prefix="/users", static_folder="../static")


@blueprint.route("/")
# @login_required
def users():
    """List users."""
    all_users = User.query.all()
    schema = UserSchema(many=True)
    return jsonify(schema.dump(all_users))


@blueprint.route("/<id>")
def user(id):
    user = User.get(id)
    schema = UserSchema()
    return jsonify(schema.dump(user))
