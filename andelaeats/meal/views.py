# -*- coding: utf-8 -*-
"""Meal views."""
from flask import Blueprint, jsonify
from flask.views import MethodView

from .models import Meal
from .schema import MealSchema

blueprint = Blueprint("meal", __name__, url_prefix="/meals")


class MealsView(MethodView):
    def get(self):
        meals = City.query.all()
        schema = CitySchema(many=True)
        return jsonify(schema.dump(meals))


class MealView(MethodView):
    def get(self, id):
        city = City.get(id)
        schema = CitySchema()
        return jsonify(schema.dump(city))


blueprint.add_url_rule("/", view_func=MealsView.as_view("meals"))
blueprint.add_url_rule("/<id>", view_func=MealView.as_view("meal"))
