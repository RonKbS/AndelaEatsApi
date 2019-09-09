from flask import request

from andelaeats.constants.errors import serialization_errors
from andelaeats.constants.methods import unsafe_methods
from andelaeats.utils.handled_errors import BaseModelValidationError


def json_validator():
    if request.method in unsafe_methods:
        try:
            request.get_json()
        except Exception:
            raise BaseModelValidationError(serialization_errors["INVALID_JSON"])
