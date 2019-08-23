
from app.controllers.base_controller import BaseController
from app.models.menu_template import MenuTemplate
from app.repositories.menu_template_repo import MenuTemplateRepo
from app.utils.auth import Auth


class MenuTemplateController(BaseController):
    def __init__(self, request):
        super().__init__(request)
        self.repo = MenuTemplateRepo(MenuTemplate)

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
