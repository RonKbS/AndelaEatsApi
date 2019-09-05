# -*- coding: utf-8 -*-
"""Vendor views."""
from flask import Blueprint, jsonify
from flask.views import MethodView

from .models import Vendor, VendorEngagement
from .schema import VendorSchema

blueprint = Blueprint("vendor", __name__, url_prefix="/vendors")


class VendorsView(MethodView):
    def get(self):
        vendors = Vendor.query.all()
        schema = VendorSchema(many=True)
        return jsonify(schema.dump(vendors))


class VendorView(MethodView):
    def get(self, id):
        vendor = Vendor.get(id)
        schema = VendorSchema()
        return jsonify(schema.dump(vendor))


blueprint.add_url_rule("/", view_func=VendorsView.as_view("vendors"))
blueprint.add_url_rule("/<id>", view_func=VendorView.as_view("vendor"))
