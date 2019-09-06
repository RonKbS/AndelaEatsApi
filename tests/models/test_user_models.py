# -*- coding: utf-8 -*-
"""Model unit tests."""
import datetime as dt

import pytest

from andelaeats.user.models import Role, User, UserRole

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

    def test_full_name(self, user):
        """User full name."""
        assert user.fullname == f"{user.first_name} {user.last_name}"

    def test_roles(self, user):
        """Add a role to a user."""
        role = Role(name="admin")
        role.save()
        user_role = UserRole(user_id=user.id, role_id=role.id)
        user_role.save()
        assert user_role in user.user_roles
