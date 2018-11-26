import enum


class MealTypes(str, enum.Enum):
    main = "main"
    side = "side"
    protein = "protein"

    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)


class Channels(str, enum.Enum):
    web = "web"
    slack = "slack"
    mobile = "mobile"

    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)


class MealPeriods(str, enum.Enum):
    lunch = "lunch"
    breakfast = "breakfast"

    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)


class OrderStatus(str, enum.Enum):
    booked = "booked"
    collected = "collected"
    cancelled = "cancelled"

    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)


class RatingType(str, enum.Enum):
    meal = "meal"
    order = "order"
    engagement = "engagement"

    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)
