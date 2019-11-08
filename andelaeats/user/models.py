# -*- coding: utf-8 -*-
"""User models."""
from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.schema import UniqueConstraint

from andelaeats.database import db, Model, reference_col, SurrogatePK


class User(SurrogatePK, Model):
    """User model class."""

    __tablename__ = "user"

    email = db.Column(db.String(80), unique=True, nullable=False, index=True)
    slack_id = db.Column(db.String(255), unique=True, index=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)
    modified = db.Column(db.DateTime(), nullable=True, onupdate=datetime.utcnow)
    image_url = db.Column(db.String(255))

    # id provided by the andela API
    user_id = db.Column(db.String(30), unique=True, index=True)

    def __init__(self, first_name, last_name, email, **kwargs):
        """Create instance."""
        db.Model.__init__(
            self, first_name=first_name, last_name=last_name, email=email, **kwargs
        )

    def has_role_or_permission(self, permission=None, role=None):
        """check that user has given permission or role"""

        if role:
            roles = self.roles.keys()
            return role in roles
        elif permission:
            permissions = set(*self.roles.values())
            return permission in permissions

    @property
    def fullname(self):
        """Full user name."""
        return f"{self.first_name} {self.last_name}"

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<User({self.fullname})>"
