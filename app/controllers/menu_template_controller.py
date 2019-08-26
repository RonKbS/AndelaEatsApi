
from datetime import datetime, timedelta

from app.controllers.base_controller import BaseController
from app.models.menu_template import MenuTemplate
from app.models.vendor_engagement import VendorEngagement
from app.repositories.menu_repo import MenuRepo
from app.repositories.menu_template_repo import MenuTemplateRepo
from app.repositories.vendor_engagement_repo import VendorEngagementRepo
from app.utils.auth import Auth


class MenuTemplateController(BaseController):
    def __init__(self, request):
        super().__init__(request)
        self.repo = MenuTemplateRepo(MenuTemplate)
        self.menu_repo = MenuRepo()
        self.vendor_repo = VendorEngagementRepo()

    def create(self):
        location = Auth.get_location()
        name, meal_period, description = self.request_params(
            'name', 'mealPeriod', 'description')
        # check unique together attirbutes
        if self.repo.exists(name=name, location_id=location):
            return self.handle_response('error', payload={
                'message': "Meal Template with name  exists in your center"}, status_code=400)

        template = self.repo.create(
            name, location, meal_period, description)
        return self.handle_response('OK', payload=template.serialize(), status_code=201)

    def update(self, template_id):
        params = self.request_params_dict()
        menu_template = self.repo.get_or_404(template_id)
        template = self.repo.update(menu_template, **params)
        return self.handle_response('OK', payload=template.serialize(), status_code=200)

    def get(self, template_id):
        menu_template = self.repo.get_or_404(template_id)
        menu_template_weekdays = [item.to_dict(
            only=['id', 'day']) for item in menu_template.menu_template_weekday.all()]
        return self.handle_response('OK', payload={'weekdays': menu_template_weekdays,
                                                   **menu_template.serialize()},
                                    status_code=200)

    def copy(self, *args, **kwargs):
        vendorEngagementId, startDate, endDate, menuTemplate_id = self.request_params(
            'vendorEngagementId', 'startDate', 'endDate', 'menuTemplateId')
        engagement = self.vendor_repo.get_or_404(vendorEngagementId)

        # check vendor engagement end and start date
        end = datetime.strptime(endDate, "%Y-%m-%d").date()
        start = datetime.strptime(startDate, "%Y-%m-%d").date()
        if end > engagement.end_date or start < engagement.start_date or end <= start:
            return self.handle_response('OK', payload={
                'msg': f'Start and end date should be between {engagement.start_date} and {engagement.end_date}'},
                status_code=400)
        data, duplicates = self.generate_menu_object_list(
            menuTemplate_id, startDate, endDate, vendorEngagementId)
        records = len(self.menu_repo.bulk_create(data))
        return self.handle_response('OK', payload={
            'message': f'{records} menu items successfully copied, {len(duplicates)} duplicates found'}, status_code=201)

    def generate_menu_object_list(self, menuTemplate_id, start_date, end_date, vendor_engagement_id):
        """
        Creates a list of menu dictionaries objects from meal items in a template
        Checks if the menu exists with the same main meal item on a given day in a given location
        Reads it as a duplicate

        Args:
            menuTemplate_id (int): menu template id
            start_date (date): start date
            end_date (date): end date

        Returns:
            tuple: menu list, and number of duplicates
        """
        template = self.repo.get_or_404(menuTemplate_id)
        data = [self.menu_object(day, meal_item, vendor_engagement_id)
                for day in self.get_dates_in_daterange(start_date, end_date)
                for meal_item in self.get_template_items(template, day.strftime('%A'))
                if not self._menu_exists(meal_item, day)]

        duplicates = [self.menu_object(day, meal_item, vendor_engagement_id)
                      for day in self.get_dates_in_daterange(start_date, end_date)
                      for meal_item in self.get_template_items(template, day.strftime('%A'))
                      if self._menu_exists(meal_item, day)]

        return data, duplicates

    def menu_object(self, day, meal_item, vendorEngagementId):
        """Creates a menu dictionary

        Args:
            day (date): date for which the menu is to be created for
            meal_item (meal_item): meal item to 
            vendorEngagementId: vendor engagement id
        Returns:
            dict: menu dictionary
        """
        return {
            "date":  day.strftime('%Y-%m-%d'),
            "meal_period": meal_item.day.menu_template.meal_period.value,
            "main_meal_id": meal_item.main_meal_id,
            "allowed_side": meal_item.allowed_protein,
            "allowed_protein": meal_item.allowed_side,
            "side_items": ','.join([str(item.id) for item in meal_item.side_items]),
            "protein_items": ','.join([str(item.id) for item in meal_item.protein_items]),
            "vendor_engagement_id": vendorEngagementId,
            "location_id": meal_item.day.menu_template.location_id}

    @staticmethod
    def get_template_items(template, weekday):
        """
        Returns menu template items for a given weekday eg monday
        """
        return template.menu_template_weekday.filter_by(day=weekday.lower()).first().items

    def _menu_exists(self, meal_item, day):
        """
        Checks if menu already exists on a given day
        """
        return self.menu_repo.exists(
            date=day.strftime('%Y-%m-%d'),
            main_meal_id=meal_item.main_meal_id,
            location_id=meal_item.day.menu_template.location_id)

    @staticmethod
    def get_dates_in_daterange(start_date, end_date):
        """Generates fates from a given date range

        Args:
            start_date (date): start date
            end_date (date): end date
        """
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        delta = timedelta(days=1)
        while start_date <= end_date:
            if start_date.weekday() in range(0, 5):
                yield start_date
            start_date += delta
