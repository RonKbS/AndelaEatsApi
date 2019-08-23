import enum


class BaseEnum(str, enum.Enum):

    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)

    @classmethod
    def all(cls):
        return [status.value for status in cls]


class MealTypes(BaseEnum):
    main = "main"
    side = "side"
    protein = "protein"


class Channels(BaseEnum):
    web = "web"
    slack = "slack"
    mobile = "mobile"


class MealPeriods(BaseEnum):
    lunch = "lunch"
    breakfast = "breakfast"


class OrderStatus(BaseEnum):
    booked = "booked"
    collected = "collected"
    cancelled = "cancelled"


class RatingType(BaseEnum):
    meal = "meal"
    order = "order"
    engagement = "engagement"


class ActionType(BaseEnum):
    create = "create"
    update = "update"
    delete = "delete"


class FaqCategoryType(BaseEnum):
    user_faq = 'user_faq'
    admin_faq = 'admin_faq'


class MealSessionNames(BaseEnum):
    breakfast = 'breakfast'
    lunch = 'lunch'


class WeekDays(BaseEnum):
    monday = 'monday'
    tuesday = 'tuesday'
    wednesday = 'wednesday'
    thursday = 'thursday'
    friday = 'friday'
