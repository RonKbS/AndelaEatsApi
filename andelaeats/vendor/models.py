# -*- coding: utf-8 -*-
"""User models."""
import enum
from datetime import datetime

from andelaeats.database import db, Model, reference_col, SurrogatePK


class EngagementStatus(enum.Enum):
    """EngagementStatus states."""

    active = "active"
    inactive = "inactive"
    terminated = "terminated"


class Vendor(SurrogatePK, Model):
    """Vendor model class."""

    __tablename__ = "vendor"
    name = db.Column(db.String(30), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    telephone = db.Column(db.String(30), nullable=False)
    contact_id = reference_col("user", nullable=False)
    contact = db.relationship("User", backref="vendors")
    active = db.Column(db.Boolean(), default=True, nullable=False)
    modified = db.Column(db.DateTime(), nullable=True, onupdate=datetime.utcnow)
    image_url = db.Column(db.String(255))

    def __init__(self, **kwargs):
        """Create instance."""
        db.Model.__init__(self, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<Vendor({self.name})>"


class VendorEngagement(SurrogatePK, Model):
    """VendorEngagement model class."""

    __tablename__ = "vendor_engagement"

    vendor_id = reference_col("vendor", nullable=False)
    vendor = db.relationship("Vendor", backref="vendor_engagements")
    start_date = db.Column(db.Date(), nullable=False, default=datetime.utcnow)
    finish_date = db.Column(db.Date(), nullable=True)
    status = db.Column(
        db.Enum(EngagementStatus), nullable=False, default=EngagementStatus.active
    )
    termination_reason = db.Column(db.Text(), nullable=True)
