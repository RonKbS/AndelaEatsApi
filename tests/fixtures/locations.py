"""Fixtures for users"""
import pytest

from ..factories import LocationFactory


@pytest.fixture
def location(db):
    city = LocationFactory()
    db.session.commit()
    return city
