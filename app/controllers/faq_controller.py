from app.controllers.base_controller import BaseController
from app.repositories.faq_repo import FaqRepo
from sqlalchemy.exc import DataError
from app.utils.enums import FaqCategoryType
from datetime import datetime


class FaqController(BaseController):
    def __init__(self, request):
        BaseController.__init__(self, request)
        self.faq_repo = FaqRepo()

    def list_faqs(self, **kwargs):

        for name, val in kwargs.items():

            if name.endswith('ted_at'):
                try:
                    kwargs.__setitem__(name, datetime.strptime(kwargs.get(name), '%Y-%m-%d'))
                except Exception:
                    return self.handle_response(
                        f'Bad Request - {name} should be valid date. Format: YYYY-MM-DD', status_code=400
                    )

        try:
            faqs = self.faq_repo.filter_by(is_deleted=False, **kwargs)
            faqs_list = [faq.to_dict() for faq in faqs.items]

        except DataError:
            enum_values = [value.value for value in FaqCategoryType.__members__.values()]
            return self.handle_response(f'Category should be one of these values {enum_values}', status_code=400)

        return self.handle_response('OK', payload={'FAQs': faqs_list, 'meta': self.pagination_meta(faqs)})
