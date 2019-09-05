from werkzeug.exceptions import HTTPException


class BaseModelValidationError(HTTPException):
    def __init__(self, msg, status_code=400):
        Exception.__init__(self)
        self.description = msg
        self.code = status_code
