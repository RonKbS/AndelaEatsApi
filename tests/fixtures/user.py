"""Fixtures for users"""
import pytest

from ..factories import UserFactory


@pytest.fixture
def user(db):
    """Create user for the tests."""
    user = UserFactory()
    db.session.commit()
    return user
