from app.repositories.base_repo import BaseRepo
from app.models.about import About


class AboutRepo(BaseRepo):

    def __init__(self):
        BaseRepo.__init__(self, About)

    def new_about(self, data):
        about = About(details=data)
        about.save()
        return about

    def first_item(self):
        return self.get_first_item()
