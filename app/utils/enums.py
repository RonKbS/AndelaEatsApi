import enum

class MealTypes(str, enum.Enum):
    main = "main"
    side = "side"
    protein = "protein"

    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)


class MealPeriods(str, enum.Enum):
    lunch = "lunch"
    breakfast = "breakfast"

    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)
