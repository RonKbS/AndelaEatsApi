from flask import request
from sqlalchemy import event


from .location import Location
from .vendor import Vendor
from .vendor_engagement import VendorEngagement
from .role import Role
from .permission import Permission
from .user_role import UserRole
from .vendor_rating import VendorRating
from .menu import Menu
from .meal_item import MealItem
from .order import Order
from .activity import Activity
from .faq import Faq

from .listener_helpers import attach_listen_type

tables_logged_after_every_insert = [Vendor, VendorEngagement, MealItem, Menu, Faq,
                                    Role, Permission, UserRole, Location]
tables_logged_after_every_update = [Vendor, VendorEngagement, MealItem, Menu, Faq,
                                    Role, Permission, UserRole, Location]
tables_logged_after_every_delete = [Vendor, VendorEngagement, MealItem, Menu, Faq,
                                    Role, Permission, UserRole, Location, VendorRating]

# attach all listeners to each admin table
attach_listen_type(tables_logged_after_every_insert, 'after_insert')
attach_listen_type(tables_logged_after_every_update, 'after_update')
attach_listen_type(tables_logged_after_every_delete, 'after_delete')
