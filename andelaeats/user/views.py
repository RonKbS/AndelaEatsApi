# -*- coding: utf-8 -*-
"""User views."""
from flask import Blueprint, jsonify
from flask.views import MethodView

from .models import User
from .schema import UserSchema

blueprint = Blueprint(
    "user", __name__, url_prefix="/api/v1/users", static_folder="../static"
)


class UsersView(MethodView):
    def get(self):
        all_users = User.query.all()
        schema = UserSchema(many=True)
        return jsonify(schema.dump(all_users))


class SingleUserView(MethodView):
    def get(self, id):
        user = User.get(id)
        schema = UserSchema()
        return jsonify(schema.dump(user))


blueprint.add_url_rule("/", view_func=UsersView.as_view("users"))
blueprint.add_url_rule("/<id>", view_func=UsersView.as_view("user"))
