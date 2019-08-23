from app.controllers.base_controller import BaseController
from app.repositories.menu_template_item_repo import MenuTemplateItemRepo
from app.repositories.meal_item_repo import MealItemRepo

class MenuTemplateItemController(BaseController):
    def __init__(self, request):
        BaseController.__init__(self, request)
        self.repo = MenuTemplateItemRepo()
        self.meal_item_repo = MealItemRepo()
        self.meal_item_fields = ['name', 'image', 'id', 'meal_type']

    def create(self):
        main_meal_id, allowed_side, allowed_protein, protein_items, side_items, day_id = self.request_params(
            'mainMealId', 'allowedSide', 'allowedProtein', 'proteinItems', 'sideItems', 'dayId')

        protein_item_objects = self.meal_item_repo.get_meal_items_by_ids(protein_items)
        side_item_objects = self.meal_item_repo.get_meal_items_by_ids(side_items)

        if self.check_protein_side_items_exist(
                protein_item_objects, side_item_objects,
                main_meal_id, allowed_side, allowed_protein,
                day_id):
            return self.handle_response('error', payload={
                'message': "Menu Template Item already exists"}, status_code=400)

        template = self.repo.create(
            main_meal_id, allowed_side, allowed_protein,
            protein_item_objects, side_item_objects, day_id)

        return self.handle_response('OK', payload=template.serialize(), status_code=201)


    def check_protein_side_items_exist(self, *args):
        protein_item_objects, side_item_objects, main_meal_id, allowed_side, allowed_protein, day_id = args
        template_item = self.repo.filter_by(
            main_meal_id=main_meal_id,
            allowed_side=allowed_side,
            allowed_protein=allowed_protein,
            day_id=day_id
        ).query.first()

        get_ids_list = lambda l: [i.id for i in l].sort()
        if template_item:
            return get_ids_list(template_item.side_items) == get_ids_list(side_item_objects)\
                and get_ids_list(template_item.protein_items) == get_ids_list(protein_item_objects)

    def get_all(self):
        query_kwargs = self.get_params_dict()
        menu_template_items = self.repo.get_menu_template_items_by_day(
            query_kwargs['day_id']
        )
        menu_template_item_list = []
        if menu_template_items.items:
            menu_template_item_list = [menu_template_item.serialize()
                                  for menu_template_item in menu_template_items.items]
        return self.handle_response('OK', payload={'MenuTemplateItems': menu_template_item_list,
                                                   'meta': self.pagination_meta(menu_template_items)})
