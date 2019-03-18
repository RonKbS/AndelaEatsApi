import base64
from app.controllers.base_controller import BaseController
from app.repositories.about_repo import AboutRepo


class AboutController(BaseController):

    def __init__(self, request):
        BaseController.__init__(self, request)
        self.about_repo = AboutRepo()

    def create_or_modify_about_page(self):
        """
        This endpoint creates a non existing about page or modifies the existing one
        :return: created or modified about page as a JSON
        """
        data = self.request_params('data')

        first_item = self.about_repo.first_item()

        if first_item:
            about = self.about_repo.update(first_item, details=base64.b64encode(data[0].encode('utf-8')))
        else:
            about = self.about_repo.new_about(data=base64.b64encode(data[0].encode('utf-8')))

        about = about.serialize()
        about['details'] = base64.b64decode(about.get('details', '')).decode('utf-8')

        return self.handle_response('OK', payload={'data': about}, status_code=201)

    def get_about_page(self):
        """
        This endpoint gets the about page details
        :return: about page
        """
        first_item = self.about_repo.first_item()

        if first_item:
            about = first_item.serialize()
            about['details'] = base64.b64decode(about.get('details', '')).decode('utf-8')
        else:
            about = {}

        return self.handle_response('OK', payload={'data': about}, status_code=200)
