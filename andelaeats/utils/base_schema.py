from flask_marshmallow.sqla import ModelSchema
from marshmallow import fields

from .handled_errors import BaseModelValidationError


class BaseSchema(ModelSchema):

    uuid = fields.UUID(dump_only=True)
    created_at = fields.DateTime(dump_only=True)

    def __init__(self, *args, **kwargs):
        self.opts.exclude += ("id",)
        super().__init__(*args, **kwargs)
