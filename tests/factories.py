# -*- coding: utf-8 -*-
"""Factories to help in tests."""
from factory.alchemy import SQLAlchemyModelFactory

from andelaeats.database import db
from andelaeats.user.models import User


class BaseFactory(SQLAlchemyModelFactory):
    """Base factory."""

    class Meta:
        """Factory configuration."""

        abstract = True
        sqlalchemy_session = db.session


class UserFactory(BaseFactory):
    class Meta:
        """Factory configuration."""

        model = User
