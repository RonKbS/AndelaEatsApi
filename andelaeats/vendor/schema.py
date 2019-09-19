from marshmallow import fields, ValidationError

from andelaeats.utils.base_schema import BaseSchema

from ..constants.success import messages
from ..user.models import User
from .models import Vendor


def validate_contact_id(uuid):
    if not User.query.filter_by(id=uuid).first():
        raise ValidationError(messages["NOT_FOUND"].format("contact_id", "id", uuid))


class VendorSchema(BaseSchema):
    """Vendor endpoint schema."""

    contact_id = fields.Integer(validate=validate_contact_id, required=True)

    class Meta:
        model = Vendor
        exclude = ("active", "modified")
