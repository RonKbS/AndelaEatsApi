
from re import sub


class SnakeCaseConversion:

    @staticmethod
    def camel_to_snake(string):
        """
        Converts a string in PascalCase or camelCase to snake_case one
        """
        return sub(r'(.)([A-Z])', r'\1_\2', string).lower()

    @staticmethod
    def snake_to_camel(string):
        return ''.join(x.capitalize() or '_' for x in string.split('_'))
