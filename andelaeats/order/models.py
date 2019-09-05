# -*- coding: utf-8 -*-
"""Order models."""
import enum

import sqlalchemy as sa

from andelaeats.database import db, Model, reference_col, SurrogatePK


class OrderStatus(enum.Enum):
    """OrderStatus."""

    booked = "booked"
    collected = "collected"
    cancelled = "cancelled"


class Channels(enum.Enum):
    """Channels."""

    web = "web"
    slack = "slack"
    mobile = "mobile"


class Order(SurrogatePK, Model):
    """Order model class."""

    __tablename__ = "order"

    user_id = reference_col("user", nullable=False)
    user = db.relationship("User", backref="order")
    meal_vendor_engagement_id = reference_col("meal_vendor_engagement", nullable=False)
    meal_vendor_engagement = db.relationship("MealVendorEngagement", backref="orders")
    city_id = reference_col("city", nullable=False)
    city = db.relationship("City", backref="orders")
    date = db.Column(db.DateTime(), nullable=False)
    status = db.Column(db.Enum(OrderStatus))
    channel = db.Column(db.Enum(Channels))


sa.Index(
    "order_idx",
    Order.user_id,
    Order.meal_vendor_engagement_id,
    Order.city_id,
    Order.status,
)
