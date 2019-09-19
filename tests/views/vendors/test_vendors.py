import json

import pytest

from andelaeats.constants.errors import jwt_errors
from andelaeats.constants.success import messages
from andelaeats.vendor.models import Vendor
from andelaeats.vendor.schema import VendorSchema

from ...factories import VendorFactory
from ..generator import ViewTestsMeta

api_version = "api/v1"


@pytest.mark.usefixtures("db")
class TestVendorEndpoints(metaclass=ViewTestsMeta):
    """Vendors tests."""

    url = "vendors.vendors"
    schema = VendorSchema
    factory = VendorFactory
    model = Vendor
