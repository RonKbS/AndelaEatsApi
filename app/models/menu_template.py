
from sqlalchemy.event import listens_for

from app.utils.enums import MealPeriods, WeekDays

from . import constants
from .base_model import BaseModel, db

side_items_association_table = db.Table("menu_template_items_to_meal_items",
                                        db.Column("meal_item_id", db.Integer(),
                                                  db.ForeignKey("meal_items.id")),
                                        db.Column("menu_template_item_id",
                                                  db.Integer(), db.ForeignKey("menu_template_item.id")))
protein_items_association_table = db.Table("menu_template_items_to_protein_items",
                                           db.Column("meal_item_id", db.Integer(),
                                                     db.ForeignKey("meal_items.id")),
                                           db.Column("menu_template_item_id",
                                                     db.Integer(), db.ForeignKey("menu_template_item.id")))


class MenuTemplate(BaseModel):

    __tablename__ = 'menu_template'
    name = db.Column(db.String(constants.MAXLEN), nullable=False)

    description = db.Column(db.String(constants.MAXLEN), nullable=False)

    location_id = db.Column(
        db.Integer(), db.ForeignKey('locations.id'))
    meal_period = db.Column(db.Enum(MealPeriods), nullable=False)

    location = db.relationship('Location', lazy=False)


class MenuTemplateWeekDay(BaseModel):
    __tablename__ = 'menu_template_weekday'

    day = db.Column(db.Enum(WeekDays), nullable=False)

    template_id = db.Column(db.Integer(), db.ForeignKey(
        'menu_template.id'), nullable=False)

    menu_template = db.relationship(
        'MenuTemplate', backref=db.backref('menu_template_weekday', lazy='dynamic'))


class MenuTemplateItem(BaseModel):
    
    __tablename__ = 'menu_template_item'

    main_meal_id = db.Column(db.Integer(), db.ForeignKey(
        'meal_items.id'), nullable=False)

    allowed_side = db.Column(db.Integer())

    allowed_protein = db.Column(db.Integer())

    side_items = db.relationship(
        "MealItem", secondary=side_items_association_table, backref=db.backref('side_items', lazy='dynamic'))

    protein_items = db.relationship(
        "MealItem", secondary=protein_items_association_table, backref=db.backref('protein_items', lazy='dynamic'))

    day_id = db.Column(db.Integer(), db.ForeignKey(
        'menu_template_weekday.id'), nullable=False)

    main_meal = db.relationship('MealItem', lazy=False)
    day = db.relationship('MenuTemplateWeekDay', lazy=True)


@listens_for(MenuTemplate, 'after_insert')
def after_insert(mapper, connect, target):
    """
    Create MenuTemplateWeekDay after creation of template
    """

    @listens_for(db.session, "after_flush", once=True)
    def receive_session_after_flush(session, context):
        menu_template_id = target.id
        objects = [MenuTemplateWeekDay(
            day=day, template_id=menu_template_id) for day in WeekDays.all()]
        session.bulk_save_objects(objects)
