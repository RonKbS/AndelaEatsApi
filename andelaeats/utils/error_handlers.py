import logging
import os
import traceback

import rollbar
from flask import jsonify, make_response
from marshmallow.exceptions import ValidationError
from werkzeug.exceptions import HTTPException

error_logger = logging.getLogger(__name__)
error_logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler("errors.log")
file_handler.setLevel(logging.ERROR)
file_handler.setFormatter(logging.Formatter("%(asctime)s:%(name)s:%(message)s"))

error_logger.addHandler(file_handler)


def handle_exception(error):
    """Error handler called when a ValidationError is raised"""
    response = {
        "msg": "An error occurred while processing your request. Please contact Admin."
    }
    if isinstance(error, HTTPException):
        return make_response(jsonify({"msg": error.description}), error.code)

    if isinstance(error, ValidationError):
        return make_response(jsonify({"error": error.messages}), 400)

    traceback.print_exc()
    error_logger.exception(str(error))

    if os.getenv("APP_ENV") in ["staging", "production"]:
        rollbar.report_exc_info()

    return make_response(jsonify(response)), 500
