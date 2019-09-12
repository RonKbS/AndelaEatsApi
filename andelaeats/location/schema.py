from marshmallow import fields, ValidationError

from andelaeats.utils.base_schema import BaseSchema

from .models import City


def validate_name(name):
    if City.query.filter_by(name=name).all():
        raise ValidationError(f"City with name '{name}' already exists")


class CitySchema(BaseSchema):
    name = fields.Str(validate=validate_name)

    class Meta:
        model = City
