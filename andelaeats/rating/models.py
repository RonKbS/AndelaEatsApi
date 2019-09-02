# -*- coding: utf-8 -*-
"""Rating models."""
import enum
from uuid import uuid4

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

from andelaeats.database import db, Model, reference_col, SurrogatePK


class RatingType(SurrogatePK, Model):
    """RatingType model class.

    e.g 'meal', 'order', 'vendor_engagement', 'vendor'
    """

    __tablename__ = 'rating_type'

    name = db.Column(db.String(80), unique=True, nullable=False, index=True)


class Rating(SurrogatePK, Model):
    """Rating model class."""

    __tablename__ = 'rating'

    uuid = db.Column(
        UUID(as_uuid=True),
        default=uuid4,
        unique=True,
        index=True,
        nullable=False
    )
    name = db.Column(db.String(80), unique=True, nullable=False, index=True)
    comment = db.Column(db.Text(), nullable=True)
    rating = db.Column(db.Float(), nullable=True)
    user_id = reference_col('user', nullable=False)
    user = db.relationship('User', backref='rating')
    rating_type_id = reference_col('rating_type', nullable=False)
    rating_type = db.relationship('RatingType', backref='rating')
    # TODO: This needs to be a foreign key to vendor, meal, order or vendor_engagement
    source_id = reference_col('vendor', nullable=False)
    source = db.relationship('Vendor', backref='rating')

sa.Index(
    'rating_idx',
    Rating.user_id,
    Rating.rating_type_id,
    Rating.source_id
)
