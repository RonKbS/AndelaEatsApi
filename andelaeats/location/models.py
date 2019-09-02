# -*- coding: utf-8 -*-
"""Location models."""
from uuid import uuid4

from sqlalchemy.dialects.postgresql import UUID

from andelaeats.database import db, Model, SurrogatePK


class City(SurrogatePK, Model):
    """A city location.

    e.g Lagos, Kampala, Accra, New York
    """

    __tablename__ = 'city'
    name = db.Column(db.String(80), unique=True, nullable=False, index=True)
    uuid = db.Column(
        UUID(as_uuid=True),
        default=uuid4,
        unique=True,
        index=True,
        nullable=False,
    )
    timezone = db.Column(db.String(80), nullable=False)

    def __init__(self, name, **kwargs):
        """Create instance."""
        db.Model.__init__(self, name=name, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return f'<City({self.name})>'
