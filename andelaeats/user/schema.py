from marshmallow import Schema


class UserSchema(Schema):
    """User endpoint schema."""

    class Meta:  # noqa
        # Fields to expose
        fields = ("email", "slack_id", "first_name", "last_name", "image_url")
