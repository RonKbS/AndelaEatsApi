# -*- coding: utf-8 -*-
"""User Schema."""
from marshmallow import fields, Schema, ValidationError

from andelaeats.constants import permissions, roles


def validate_roles(role):
    if role not in roles:
        raise ValidationError(f"Role '{role}' is invalid!")


def validate_permissions(permission):
    if permission not in permissions:
        raise ValidationError(f"Permission '{permission}' is invalid!")


class RoleSchema(Schema):
    role_name = fields.List(fields.Str(validate=validate_permissions))


class UserSchema(Schema):
    """User endpoint schema."""

    roles = fields.Nested(RoleSchema, validate=validate_roles)

    class Meta:  # noqa
        # Fields to expose
        fields = ("email", "slack_id", "first_name", "last_name", "image_url")
