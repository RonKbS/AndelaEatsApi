# -*- coding: utf-8 -*-
"""Rating views."""
from flask import Blueprint, jsonify
from flask.views import MethodView

from .models import City
from .schema import CitySchema

blueprint = Blueprint("location", __name__, url_prefix="/locations")


class LocationsView(MethodView):
    def get(self):
        all_users = City.query.all()
        schema = CitySchema(many=True)
        return jsonify(schema.dump(all_cities))


class LocationView(MethodView):
    def get(self, id):
        city = City.get(id)
        schema = CitySchema()
        return jsonify(schema.dump(city))


blueprint.add_url_rule("/", view_func=LocationsView.as_view("cities"))
blueprint.add_url_rule("/<id>", view_func=LocationView.as_view("city"))
