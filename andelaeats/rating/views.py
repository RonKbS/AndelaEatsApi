# -*- coding: utf-8 -*-
"""Rating views."""
from flask import Blueprint, jsonify
from flask.views import MethodView

from andelaeats.utils.mixins import (
    ModelListCreateMixin,
    ModelUpdateMixin,
    RetrieveDeleteMixin,
)

from .models import Rating
from .schema import RatingSchema

blueprint = Blueprint("rating", __name__, url_prefix="/ratings")


class RatingsView(MethodView, ModelListCreateMixin):
    model = Rating
    schema = RatingSchema


class RatingView(MethodView, RetrieveDeleteMixin, ModelUpdateMixin):
    model = Rating
    schema = RatingSchema


blueprint.add_url_rule("/", view_func=RatingsView.as_view("ratings"))
blueprint.add_url_rule("/<string:uuid>", view_func=RatingView.as_view("rating"))
