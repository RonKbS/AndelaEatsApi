from app.repositories.base_repo import BaseRepo
from app.models.vendor_rating import VendorRating
from statistics import mean


class VendorRatingRepo(BaseRepo):

    def __init__(self):
        BaseRepo.__init__(self, VendorRating)

    def new_rating(self, vendor_id, user_id, rating, service_date, rating_type, type_id, engagement_id, channel, comment='', main_menu_id=0):
        vendor_rating = VendorRating(
            vendor_id=vendor_id, user_id=user_id,
            rating=rating, service_date=service_date, channel=channel, comment=comment,
            rating_type=rating_type, type_id=type_id,
            engagement_id=engagement_id, main_meal_id=main_menu_id
        )
        vendor_rating.save()
        return vendor_rating

    def meal_average(self, main_meal_id, date):
        meal_ratings = self.get_unpaginated(main_meal_id=main_meal_id, service_date=date)
        return mean([meal_rating.rating for meal_rating in meal_ratings])

    @staticmethod
    def daily_average_rating(date):

        daily_ratings = VendorRating.query.filter_by(service_date=date).all()
        if daily_ratings:
            rating_values = [rating.rating for rating in daily_ratings]
            rating_sum = sum(rating_values)
            return round(rating_sum/len(rating_values), 1)
        return None
