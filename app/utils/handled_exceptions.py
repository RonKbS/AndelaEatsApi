class BaseModelValidationError(Exception):

    def __init__(self, msg, status_code=400):
        Exception.__init__(self)
        self.msg = msg
        self.status_code = status_code
