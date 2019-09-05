from marshmallow import Schema


class RatingSchema(Schema):
    """RatingSchema endpoint schema."""

    class Meta:  # noqa
        # Fields to expose
        fields = ("name", "comment")
