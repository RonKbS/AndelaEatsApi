# -*- coding: utf-8 -*-
"""Meal models."""
import enum
from datetime import datetime

import sqlalchemy as sa

from andelaeats.database import db, Model, reference_col, SurrogatePK


class MealPeriods(enum.Enum):
    """MealPeriods."""

    breakfast = "breakfast"
    lunch = "lunch"
    dinner = "dinner"


class MealTypes(enum.Enum):
    """MealTypes."""

    main = "main"
    side = "side"
    dinner = "dinner"


class Meal(SurrogatePK, Model):
    """Meal model class."""

    __tablename__ = "meal"

    name = db.Column(db.String(80), unique=True, nullable=False, index=True)
    sides = db.Column(db.Integer(), unique=True, index=True)
    proteins = db.Column(db.Integer(), nullable=False)
    created = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)
    modified = db.Column(db.DateTime(), nullable=True, onupdate=datetime.utcnow)
    image_url = db.Column(db.String(255))

    def __init__(self, name, **kwargs):
        """Create instance."""
        db.Model.__init__(self, name=name, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<Meal({self.name})>"


sa.Index("meal_idx", Meal.name, Meal.sides, Meal.proteins)


class MealItem(SurrogatePK, Model):
    """MealItem model class.

    e.g Eba, Fried Rice, Spaghetti, Meat, Jollof rice, Fish
    """

    __tablename__ = "meal_item"

    name = db.Column(db.String(80), unique=True, nullable=False, index=True)
    meal_type = db.Column(db.Enum(MealTypes))

    def __init__(self, name, **kwargs):
        """Create instance."""
        db.Model.__init__(self, name=name, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<MealItem({self.name})>"


class MealItems(SurrogatePK, Model):
    """MealItems model class."""

    __tablename__ = "meal_items"

    meal_id = reference_col("meal", nullable=False)
    meal = db.relationship("Meal", backref="meal_items")
    meal_item_id = reference_col("meal_item", nullable=False)
    meal_item = db.relationship("MealItem", backref="meal_items")


sa.Index("meal_items_idx", MealItems.meal_id, MealItems.meal_item_id)


class MealVendorEngagement(SurrogatePK, Model):
    """MealVendorEngagement model class."""

    __tablename__ = "meal_vendor_engagement"

    meal_id = reference_col("meal", nullable=False)
    meal = db.relationship("Meal", backref="vendor_meal_items")
    vendor_engagement_id = reference_col("vendor_engagement", nullable=False)
    vendor_engagement = db.relationship(
        "VendorEngagement", backref="meal_vendor_engagements"
    )
    meal_period = db.Column(db.Enum(MealPeriods), nullable=False)
    date = db.Column(db.Date(), nullable=False)
    price = db.Column(db.Float(), nullable=False, default=0)


sa.Index(
    "meal_vendor_engagement_idx",
    MealVendorEngagement.meal_id,
    MealVendorEngagement.vendor_engagement_id,
    MealVendorEngagement.meal_period,
)


class MealGroup(SurrogatePK, Model):
    """MealGroup model class."""

    __tablename__ = "meal_group"

    name = db.Column(db.String(80), unique=True, nullable=False, index=True)


class MealGroupItem(SurrogatePK, Model):
    """MealGroupItem model class."""

    __tablename__ = "meal_group_item"

    meal_id = reference_col("meal", nullable=False)
    meal = db.relationship("Meal", backref="meal_items_group")
    group_id = reference_col("meal_group", nullable=False)
    group = db.relationship("MealGroup", backref="meal_group_items")


sa.Index("meal_group_item_idx", MealGroupItem.group_id, MealGroupItem.meal_id)


class MealService(SurrogatePK, Model):
    """MealService model class."""

    __tablename__ = "meal_service"

    meal_vendor_engagement_id = reference_col("meal_vendor_engagement", nullable=False)
    meal_vendor_engagement = db.relationship(
        "MealVendorEngagement", backref="meal_services"
    )
    user_id = reference_col("user", nullable=False)
    user = db.relationship("User", backref="meal_services")
    date = db.Column(db.Date(), default=datetime.utcnow)
    city_id = reference_col("city", nullable=False)
    city = db.relationship("City", backref="meal_services")


sa.Index(
    "meal_service_idx",
    MealService.user_id,
    MealService.city_id,
    MealService.meal_vendor_engagement_id,
)
