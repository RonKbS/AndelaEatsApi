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
    created = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)
    modified = db.Column(db.DateTime(), nullable=True, onupdate=datetime.utcnow)
    image_url = db.Column(db.String(255))

    def __init__(self, first_name, last_name, email, **kwargs):
        """Create instance."""
        db.Model.__init__(
            self, first_name=first_name, last_name=last_name, email=email, **kwargs
        )

    @property
    def fullname(self):
        """Full user name."""
        return f"{self.first_name} {self.last_name}"

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<User({self.fullname})>"


class Role(SurrogatePK, Model):
    """A role for a user.

    e.g admin, staff, dev, ops, vendor
    """

    __tablename__ = "role"
    name = db.Column(db.String(80), unique=True, nullable=False, index=True)

    description = db.Column(db.Text())

    def __init__(self, name, **kwargs):
        """Create instance."""
        db.Model.__init__(self, name=name, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<Role({self.name})>"


class Permission(SurrogatePK, Model):
    """Permissions for a user.

    e.g delete_user, create_meal, create_template, delete_template,
        create_vendor, view_meals, rate_meal
    """

    __tablename__ = "permission"
    name = db.Column(db.String(80), unique=True, nullable=False, index=True)

    description = db.Column(db.Text())

    def __init__(self, name, **kwargs):
        """Create instance."""
        db.Model.__init__(self, name=name, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<Permission({self.name})>"


class UserRole(SurrogatePK, Model):
    """User Role model class."""

    __tablename__ = "user_role"
    __table_args__ = (UniqueConstraint("user_id", "role_id"),)

    user_id = reference_col("user", nullable=False)
    user = db.relationship("User", backref="user_roles")
    role_id = reference_col("role", nullable=False)
    role = db.relationship("Role", backref="user_roles")


sa.Index("user_role_idx", UserRole.user_id, UserRole.role_id)


class RolePermission(SurrogatePK, Model):
    """Role Permission model class."""

    __tablename__ = "role_permission"
    __table_args__ = (UniqueConstraint("role_id", "permission_id"),)

    role_id = reference_col("role", nullable=False)
    role = db.relationship("Role", backref="role_permissions")
    permission_id = reference_col("permission", nullable=False)
    permission = db.relationship("Permission", backref="role_permissions")


sa.Index("role_permission_idx", RolePermission.role_id, RolePermission.permission_id)
