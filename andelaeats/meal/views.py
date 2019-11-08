# -*- coding: utf-8 -*-
"""Meal views."""
from flask import Blueprint
from flask.views import MethodView

from ..utils.mixins import ModelListCreateMixin, RetrieveDeleteMixin
from .models import Meal
from .schema import MealSchema

blueprint = Blueprint("meal", __name__, url_prefix="/meals")


class MealsView(MethodView, ModelListCreateMixin):
    model = Meal
    schema = MealSchema


class MealView(MethodView, RetrieveDeleteMixin):
    model = Meal
    schema = MealSchema


blueprint.add_url_rule("/", view_func=MealsView.as_view("meals"))
blueprint.add_url_rule("/<string:uuid>", view_func=MealView.as_view("meal"))
