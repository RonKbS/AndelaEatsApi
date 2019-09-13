"""Rating views."""
from flask import Blueprint, jsonify, make_response, request
from flask.views import MethodView

from ..utils.mixins import (  # noqa
    ModelListCreateMixin,
    ModelUpdateMixin,
    RetrieveDeleteMixin,
)
from .models import Location
from .schema import LocationSchema

blueprint = Blueprint("location", __name__, url_prefix="/api/v1/locations")


class LocationsView(MethodView, ModelListCreateMixin):
    schema = LocationSchema
    model = Location


class LocationView(MethodView, RetrieveDeleteMixin, ModelUpdateMixin):
    schema = LocationSchema
    model = Location


blueprint.add_url_rule("/", view_func=LocationsView.as_view("locations"))
blueprint.add_url_rule("/<string:uuid>", view_func=LocationView.as_view("location"))
