from marshmallow import Schema


class CitySchema(Schema):
    """CitySchema endpoint schema."""

    class Meta:  # noqa
        # Fields to expose
        fields = ("name",)
