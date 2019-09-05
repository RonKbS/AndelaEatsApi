from marshmallow import Schema


class MealSchema(Schema):
    """MealSchema endpoint schema."""

    class Meta:  # noqa
        # Fields to expose
        fields = ("name", "sides", "protein", "image_url")
