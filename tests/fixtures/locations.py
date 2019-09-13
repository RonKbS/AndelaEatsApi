"""Fixtures for users"""
import pytest

from ..factories import LocationFactory


@pytest.fixture
def location(db):
    location = LocationFactory()
    db.session.commit()
    return location
