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
        """
        Handles the creation of a menu template item
        """
        main_meal_id, allowed_side, allowed_protein, protein_items, side_items, day_id = self.request_params(
            'mainMealId', 'allowedSide', 'allowedProtein', 'proteinItems', 'sideItems', 'dayId')

        protein_item_objects = self.meal_item_repo.get_meal_items_by_ids(protein_items)
        side_item_objects = self.meal_item_repo.get_meal_items_by_ids(side_items)

        return self.return_response(
            protein_item_objects, side_item_objects,
            main_meal_id, allowed_side, allowed_protein,day_id,
            create=True
        )

    def update_item(self, template_id):
        """
        Handles the updating of a menu template item
        """
        main_meal_id, allowed_side, allowed_protein, protein_items, side_items, day_id = self.request_params(
                    'mainMealId', 'allowedSide', 'allowedProtein', 'proteinItems', 'sideItems', 'dayId')

        template_item = self.repo.get_or_404(template_id)

        protein_item_objects = self.meal_item_repo.get_meal_items_by_ids(protein_items) if protein_items else []
        side_item_objects = self.meal_item_repo.get_meal_items_by_ids(side_items) if side_items else []

        update_fields = self.check_passed_params(
            main_meal_id, allowed_side, allowed_protein,
            protein_item_objects, side_item_objects, day_id
        )
        # if template_item is not None:
        params = {
            "update_fields": update_fields,
            "template_item": template_item,
            "create": False
        }

        return self.return_response(
            protein_item_objects, side_item_objects,
            main_meal_id, allowed_side, allowed_protein,
            day_id, **params
    )


    def check_passed_params(self, *args):
        """
        Checks whether user intends to update all fields or
        just some of the fields and return the partial or 
        complete dict of fields
        """
        main_meal_id, allowed_side, allowed_protein, protein_items, side_items, day_id = args

        update_params = {
            'all': main_meal_id and allowed_side and allowed_protein\
                and protein_items and side_items and day_id,
            'main_meal_id': main_meal_id,
            'allowed_side': allowed_side,
            'allowed_protein': allowed_protein,
            'protein_items': protein_items,
            'side_items': side_items,
            'day_id': day_id
        }

        if update_params['all']: 
            return (None, { param:update_params[param] for param\
                in update_params if param != 'all'})
                
        else:
            del update_params['all']
            update_params = { key: update_params[key] for key in update_params.keys() if update_params[key]}
            return (update_params, )

    def check_protein_side_items_exist(self, *args):
        """
        Checks that exact template item with exact side and protein
        items exists and return True or False accordingly
        """
        protein_item_objects, side_item_objects, main_meal_id,\
            allowed_side, allowed_protein, day_id = args
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

    def return_response(self, *args, **kwargs):
        """
        Returns appropriate response for `create` or `update` action
        """
        protein_item_objects, side_item_objects, main_meal_id,\
            allowed_side, allowed_protein, day_id = args
        create, update_fields, template_item = (
            kwargs.get('create'), kwargs.get('update_fields'), kwargs.get('template_item')
        )

        if self.handle_exists(
            protein_item_objects, side_item_objects,
            main_meal_id, allowed_side, allowed_protein,
            day_id, update_fields, create
        ):
            return self.handle_response('error', payload={
                'message': "Menu Template Item already exists"}, status_code=400)

        return self.handle_create_update_response(
            template_item,update_fields, main_meal_id,
            allowed_side, allowed_protein, protein_item_objects,
            side_item_objects, day_id, create)
        

    def handle_create_update_response(self, *args):
        """
        Returns appropriate response depending on whether
        it was a successful `create` or `update` action
        """
        template_item, update_fields, main_meal_id, allowed_side, allowed_protein,\
            protein_item_objects, side_item_objects, day_id, create = args

        # returns template depending on where it's
        # a `create` or `update` action
        template = self.create_or_update(
            create, update_fields, update_fields, main_meal_id,
            template_item, allowed_side, allowed_protein,
            protein_item_objects, side_item_objects, day_id
        )

        # return appropriate results depending on the `create` flag
        payload, status = ({'menuTemplateItem': template_item.serialize()}, 200)\
            if not create else (template.serialize(), 201)

        return self.handle_response(
            'OK', payload=payload,
            status_code=status
            )

    def create_or_update(self, *args):
        """
        Returns template depending on where it's
        a `create` or `update` action
        """
        create, update_fields, update_fields, main_meal_id, template_item,\
            allowed_side, allowed_protein, protein_item_objects, side_item_objects, day_id = args
        if not create:
            update_fields = update_fields[0] if update_fields[0] else update_fields[1]
            template = self.repo.update(template_item, **update_fields)

        else:
            template = self.repo.create(
                main_meal_id, allowed_side, allowed_protein,
                protein_item_objects, side_item_objects, day_id)
        return template


    def handle_exists(self, *args):
        """
        Returns `True` if template to be create or updated
        exists else False
        """
        protein_item_objects, side_item_objects, main_meal_id, allowed_side, allowed_protein, day_id, update_fields, create = args
        if (self.check_protein_side_items_exist(
            protein_item_objects, side_item_objects,
            main_meal_id, allowed_side, allowed_protein,
            day_id) and create) or (
                    self.check_protein_side_items_exist(
                protein_item_objects, side_item_objects,
                main_meal_id, allowed_side, allowed_protein,
                day_id) and not update_fields[0] and not create
            ):
                return True
        return False
