
from app.controllers.base_controller import BaseController
from app.repositories.menu_template_repo import MenuTemplateRepo
from app.models.menu_template import MenuTemplate

from app.utils.auth import Auth


class MenuTemplateController(BaseController):
    def __init__(self, request):
        super().__init__(request)
        self.menu_template_repo = MenuTemplateRepo(MenuTemplate)

    def create(self):
        location = Auth.get_location()
        name, meal_period, description = self.request_params(
            'templateName', 'mealPeriod', 'description')
        # check unique together attirbutes
        if self.menu_template_repo.exists(name=name, location_id=location):
            return self.handle_response('error', payload={
                'message': "Meal Template with name  exists in your center"}, status_code=400)

        template = self.menu_template_repo.create(
            name, location, meal_period, description)
        return self.handle_response('OK', payload=template.serialize(), status_code=201)

    def update(self, template_id):
        name, = self.request_params(
            'templateName')
        menu_template = self.menu_template_repo.get_or_404(template_id)
        template = self.menu_template_repo.update(menu_template,name=name)
        return self.handle_response('OK', payload=template.serialize(), status_code=200)

