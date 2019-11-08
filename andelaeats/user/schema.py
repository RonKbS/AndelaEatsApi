# -*- coding: utf-8 -*-
"""User Schema."""
from marshmallow import fields, Schema, ValidationError

from andelaeats.constants import permissions, roles
from andelaeats.utils.base_schema import BaseSchema

from ..constants.success import messages
from .models import User


def validate_slack_id(value):
    validate_id(slack_id=value)


def validate_user_id(value):
    validate_id(user_id=value)


def validate_id(**kwargs):
    if User.query.filter_by(**kwargs).all():
        key_value = next(iter(kwargs.items()))
        raise ValidationError(
            messages["DUPLICATE_ID"].format("user", key_value[0], key_value[1])
        )


class UserSchema(BaseSchema):
    """User endpoint schema."""

    slack_id = fields.Str(validate=validate_slack_id)
    user_id = fields.Str(validate=validate_user_id)
    email = fields.Email()

    class Meta:
        model = User
        exclude = ("active", "modified")
