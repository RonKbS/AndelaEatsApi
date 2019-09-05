# -*- coding: utf-8 -*-
"""Rating views."""
from flask import Blueprint, jsonify
from flask.views import MethodView

from .models import Rating
from .schema import RatingSchema

blueprint = Blueprint("rating", __name__, url_prefix="/ratings")


class RatingsView(MethodView):
    def get(self):
        ratings = Rating.query.all()
        schema = RatingSchema(many=True)
        return jsonify(schema.dump(ratings))


class RatingView(MethodView):
    def get(self, id):
        rating = Rating.get(id)
        schema = RatingSchema()
        return jsonify(schema.dump(rating))


blueprint.add_url_rule("/", view_func=RatingsView.as_view("ratings"))
blueprint.add_url_rule("/<id>", view_func=RatingView.as_view("rating"))
