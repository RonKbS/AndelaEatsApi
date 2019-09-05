# -*- coding: utf-8 -*-
"""Model unit tests."""
import datetime as dt

import pytest

from andelaeats.user.models import Role, User, UserRole

from .factories import UserFactory


@pytest.mark.usefixtures("db")
class TestUser:
    """User tests."""

    def test_get_by_id(self):
        """Get user by ID."""
        user = User("firstname", "lastname", "foo@bar.com")
        user.save()
        retrieved = User.get_by_id(user.id)
        assert retrieved == user

    def test_created_at_defaults_to_datetime(self):
        """Test creation date."""
        user = User("firstname", "lastname", "foo@bar.com")
        user.save()
        assert bool(user.created_at)
        assert isinstance(user.created_at, dt.datetime)

    def test_full_name(self):
        """User full name."""
        user = UserFactory(first_name="Foo", last_name="Bar")
        assert user.fullname == "Foo Bar"

    def test_roles(self):
        """Add a role to a user."""
        role = Role(name="admin")
        role.save()
        user = UserFactory()
        user.save()
        user_role = UserRole(user_id=user.id, role_id=role.id)
        user_role.save()
        assert user_role in user.user_roles
