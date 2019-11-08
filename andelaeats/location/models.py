# -*- coding: utf-8 -*-
"""Location models."""
from andelaeats.database import db, Model, SurrogatePK


class Location(SurrogatePK, Model):
    """A location location.

    e.g Lagos, Kampala, Accra, New York
    """

    __tablename__ = "location"
    name = db.Column(db.String(80), unique=True, nullable=False, index=True)
    timezone = db.Column(db.String(80), nullable=False)

    def __init__(self, name, **kwargs):
        """Create instance."""
        db.Model.__init__(self, name=name, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<Location({self.name})>"
