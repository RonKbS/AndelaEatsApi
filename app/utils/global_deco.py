from functools import wraps
import traceback
from flask import jsonify, make_response


def error_wrapper(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception, err:

            traceback.print_exc()

            return make_response(jsonify({'msg': 'An error occurred while processing your request'})), 500
