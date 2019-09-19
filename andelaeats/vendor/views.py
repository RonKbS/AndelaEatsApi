# -*- coding: utf-8 -*-
"""Vendor views."""
from flask import Blueprint, jsonify
from flask.views import MethodView

from andelaeats.utils.mixins import (
    ModelListCreateMixin,
    ModelUpdateMixin,
    RetrieveDeleteMixin,
)

from .models import Vendor, VendorEngagement
from .schema import VendorSchema

blueprint = Blueprint("vendors", __name__, url_prefix="/api/v1/vendors")


class VendorsView(MethodView, ModelListCreateMixin):
    schema = VendorSchema
    model = Vendor


class VendorView(MethodView, RetrieveDeleteMixin, ModelUpdateMixin):
    schema = VendorSchema
    model = Vendor


blueprint.add_url_rule("/", view_func=VendorsView.as_view("vendors"))
blueprint.add_url_rule("/<string:uuid>", view_func=VendorView.as_view("vendor"))
