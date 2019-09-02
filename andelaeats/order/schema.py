from marshmallow import Schema


class OrderSchema(Schema):
    """OrderSchema endpoint schema."""

    class Meta: # noqa
        # Fields to expose
        fields = ('status', 'channel')
