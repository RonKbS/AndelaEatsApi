# -*- coding: utf-8 -*-
"""User views."""
from flask import Blueprint, jsonify
from flask.views import MethodView

from andelaeats.utils.mixins import (
    ModelListCreateMixin,
    ModelUpdateMixin,
    RetrieveDeleteMixin,
)

from .models import User
from .schema import UserSchema

blueprint = Blueprint(
    "user", __name__, url_prefix="/api/v1/users", static_folder="../static"
)


class UsersView(MethodView, ModelListCreateMixin):
    schema = UserSchema
    model = User


class SingleUserView(MethodView, RetrieveDeleteMixin, ModelUpdateMixin):
    schema = UserSchema
    model = User


blueprint.add_url_rule("/", view_func=UsersView.as_view("users"))
blueprint.add_url_rule("/<string:uuid>", view_func=SingleUserView.as_view("user"))
