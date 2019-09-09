# -*- coding: utf-8 -*-
"""Rating views."""
from flask import Blueprint, jsonify, make_response, request
from flask.views import MethodView

from ..utils.view_utils import delete_by_id
from .models import City
from .schema import CitySchema

blueprint = Blueprint("location", __name__, url_prefix="/api/v1/locations")


class LocationsView(MethodView):
    def get(self):
        all_cities = City.query.all()
        schema = CitySchema(many=True)
        return {"locations": schema.dump(all_cities)}, 200

    def post(self):
        request_data = request.get_json()
        schema = CitySchema()
        city = schema.load(request_data)
        city.save()
        return make_response(jsonify({"location": schema.dump(city)}), 201)


class LocationView(MethodView):
    def get(self, id):
        city = City.get_or_404(id)
        schema = CitySchema()
        return make_response(jsonify({"location": schema.dump(city)}), 200)

    def put(self, id):
        city = City.get_or_404(id)
        request_data = request.get_json()
        schema = CitySchema()
        city = schema.load(request_data, instance=city, partial=True)
        return make_response(jsonify({"location": schema.dump(city)}), 200)

    def delete(self, id):
        return delete_by_id(City, id, "Location")


blueprint.add_url_rule("/", view_func=LocationsView.as_view("cities"))
blueprint.add_url_rule("/<id>", view_func=LocationView.as_view("city"))
