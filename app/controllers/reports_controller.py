"""A controller module for report-related activities
"""
from datetime import datetime, timedelta
import pandas as pd
from app.controllers.base_controller import BaseController
from app.repositories import OrderRepo, VendorRatingRepo, VendorEngagementRepo
from app.models import Order


class ReportsController(BaseController):
    def __init__(self, request):
        BaseController.__init__(self, request)
        self.rating_repo = VendorRatingRepo()
        self.order_repo = OrderRepo()
        self.engagement_repo = VendorEngagementRepo()

    def dashboard_summary(self):
        params = self.get_params_dict()
        period = int(params.get('period', 14))
        last_date = datetime.now().date() - timedelta(period)

        orders = Order.query.filter(Order.date_booked_for >= last_date)
        orders_collected = [order for order in orders if order.order_status == 'collected']
        orders_cancelled = [order for order in orders if order.order_status == 'cancelled']
        orders_uncollected = [order for order in orders if order.order_status == 'booked']
        dates = [date.date() for date in pd.bdate_range(last_date, datetime.now().date())]
        result = []

        for date in dates:
            date_info = {
                'date': date,
                'collectedOrders': len([order for order in orders_collected if order.date_booked_for == date]),
                'uncollectedOrders': len([order for order in orders_uncollected if order.date_booked_for == date]),
                'cancelledOrders': len([order for order in orders_cancelled if order.date_booked_for == date]),
                'averageRating': self.rating_repo.daily_average_rating(date),
                'vendor': self.engagement_repo.vendor_of_the_day(date)
            }
            result.append(date_info)

        return self.handle_response('OK', payload=result)

