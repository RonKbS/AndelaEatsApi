# -*- coding: utf-8 -*-
"""Model unit tests."""
import datetime as dt

import pytest

from andelaeats.user.models import User

from ..factories import UserFactory


@pytest.mark.usefixtures("db")
class TestUser:
    """User tests."""

    def test_get_by_id(self, user):
        """Get user by ID."""
        retrieved = User.get_by_id(user.id)
        assert retrieved == user

    def test_created_at_defaults_to_datetime(self, user):
        """Test creation date."""
        assert bool(user.created_at)
        assert isinstance(user.created_at, dt.datetime)

    def test_representation(self, user):
        """User full name and __repr__"""
        assert user.fullname == f"{user.first_name} {user.last_name}"
        assert user.__repr__() == f"<User({user.fullname})>"

    def test_roles(self, user):
        """Add a role to a user."""
        roles = {"roles": {"admin": ["create_user"]}}
        user.update(**roles)
        assert "admin" in user.roles
        assert user.has_role_or_permission(permission="create_user") is True
