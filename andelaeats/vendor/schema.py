from marshmallow import Schema


class VendorSchema(Schema):
    """Vendor endpoint schema."""

    class Meta:
        # Fields to expose
        fields = ("name", "address", "telephone", "active", "image_url")
