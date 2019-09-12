from flask_marshmallow.sqla import ModelSchema

from .handled_errors import BaseModelValidationError


class BaseSchema(ModelSchema):
    pass
