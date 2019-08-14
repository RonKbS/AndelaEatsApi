from itertools import zip_longest
from functools import wraps
from datetime import datetime
import re
from flask import request, make_response, jsonify
from app.utils.snake_case import SnakeCaseConversion
from app.utils.enums import ActionType, Channels, FaqCategoryType, MealSessionNames, MealTypes, MealPeriods


class Security:

    EMAIL_REGEX = re.compile(
        r"^[\-a-zA-Z0-9_]+(\.[\-a-zA-Z0-9_]+)*@[\-a-z]+\.[\-a-zA-Z0-9_]+\Z", re.I | re.UNICODE)

    URL_REGEX = re.compile(r"^(http(s)?:\/\/)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]"
                           r"{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)$")

    @staticmethod
    def url_validator(rules):
        """
        This url validator is targeted at validating the urls
        :rules: list -  The sets of keys and rules to be applied
        example: [username|required:max-255:min-120, email|required:email]
        """

        def real_validate_request(f):

            @wraps(f)
            def decorated(*args, **kwargs):

                if not request.args:
                    return make_response(jsonify({'msg': 'Bad Request - Request Must be Properly Formatted'})), 400

                arguments = request.args
                if arguments:
                    for rule in rules:
                        rule_array = rule.split('|')

                        request_key = rule_array[0]
                        validators = rule_array[1].split(':')

                        # If the key is not in the request arguments, and required is not part of the validator rules,
                        # Continue the loop to avoid key errors.
                        if request_key not in arguments and 'required' not in validators:
                            continue
                        # Loop all validators specified in the current rule
                        for validator in validators:
                            if validator == 'int' and type(arguments[request_key]) is str \
                                            and not arguments[request_key].isdigit():
                                return make_response(
                                    jsonify({'msg': 'Bad Request - {} must be integer'.format(request_key)})), 400

                            if validator == 'range':
                                if ':' in arguments[request_key]:
                                    elements_compare = arguments[request_key].split(
                                        ':')
                                else:
                                    return make_response(
                                        jsonify(
                                            {'msg': 'Bad Request - There must be a `:` separating the dates'}
                                        )), 400

                                try:
                                    first_date = datetime.strptime(
                                        str(elements_compare[0]), '%Y-%m-%d')
                                    second_date = datetime.strptime(
                                        str(elements_compare[1]), '%Y-%m-%d')
                                except Exception as e:
                                    return make_response(
                                        jsonify({'msg': 'Bad Request - dates {} and {} should be valid dates.\
											Format: YYYY-MM-DD'.format(
                                            str(elements_compare[0]),
                                            str(elements_compare[1]))
                                        }
                                        )), 400
                                if first_date > second_date:
                                    return make_response(
                                        jsonify({'msg': 'Bad Request - Start Date [{}] must be less than End Date[{}]'
                                                 .format(first_date, second_date)})), 400

                            if validator == 'float':
                                try:
                                    float(arguments[request_key])
                                except Exception as e:
                                    return make_response(
                                        jsonify({'msg': 'Bad Request - {} must be float'.format(request_key)})), 400

                            if (validator == 'required' and request_key not in arguments) \
                                    or arguments[request_key] == '':
                                return make_response(
                                    jsonify({'msg': 'Bad Request - {} is required'.format(request_key)})), 400

                            if validator.find('max') > -1:
                                max_value = int(validator.split('-')[1])
                                if int(arguments[request_key]) > max_value:
                                    return make_response(
                                        jsonify({'msg': 'Bad Request - {} can only have a max value of {}'.format(
                                            request_key, max_value)})), 400

                            if validator.find('min') > -1:
                                min_value = int(validator.split('-')[1])
                                if int(arguments[request_key]) < min_value:
                                    return make_response(
                                        jsonify({'msg': 'Bad Request - {} can only have a min value of {}'.format(
                                            request_key, min_value)})), 400

                            if validator.find('length') > -1:
                                length_value = int(validator.split('-')[1])
                                if len(str(arguments[request_key])) > length_value:
                                    return make_response(
                                        jsonify({'msg': 'Bad Request - {} can only have a len of {}'.format(
                                            request_key, length_value)})), 400

                            if validator == 'enum_options':
                                mapper = {
                                    'action_type': ActionType,
                                    'channels': Channels
                                }

                                if not mapper.get(request_key, None):
                                    return make_response(
                                        jsonify({'msg': 'Bad Request - Invalid search field {}'.format(
                                            request_key)})), 400

                                if not mapper.get(request_key).has_value(arguments[request_key]):
                                    return make_response(
                                        jsonify({'msg': 'Bad Request - {} can only have options: {}'.format(
                                            request_key,
                                            str([item.name for item in mapper.get(
                                                request_key)]).strip('[]')
                                        )}
                                        )
                                    ), 400

                            if validator == 'exists':
                                import importlib
                                from app.utils import to_pascal_case

                                repo_name = rule_array[2]
                                column_name = rule_array[3]

                                rep = 'app.repositories.{}_repo'.format(
                                    repo_name)
                                mod = importlib.import_module(rep)
                                repo_class = getattr(
                                    mod, '{}Repo'.format(to_pascal_case(repo_name)))
                                repo = repo_class()

                                if type(arguments[request_key]) == int:
                                    v = repo.find_first(
                                        **{column_name: arguments[request_key]})

                                    if not v:
                                        return make_response(
                                            jsonify(
                                                {'msg': 'Bad Request - {} contains invalid {}(s) for {} table '
                                                 .format(request_key, column_name,
                                                         repo_name)})), 400

                                if type(arguments[request_key]) == list:
                                    for val in arguments[request_key]:
                                        v = repo.find_first(
                                            **{column_name: val})

                                        if not v:
                                            return make_response(
                                                jsonify(
                                                    {'msg': 'Bad Request - {} contains invalid {}(s) for {} table '
                                                     .format(request_key, column_name,
                                                             repo_name)})), 400

                            if validator == 'date':
                                try:
                                    datetime.strptime(
                                        arguments[request_key], '%Y-%m-%d')
                                except Exception as e:
                                    return make_response(
                                        jsonify(
                                            {'msg': 'Bad Request - {} should be valid date. Format: YYYY-MM-DD'
                                             .format(request_key)})), 400

                            if validator == 'list' and type(arguments[request_key]) is not list:
                                return make_response(
                                    jsonify({'msg': 'Bad Request - {} must be a list'.format(request_key)})), 400

                            if validator == 'list_int':
                                if type(arguments[request_key]) is not list:
                                    return make_response(
                                        jsonify({'msg': 'Bad Request - {} must be a list'.format(request_key)})), 400
                                for val in arguments[request_key]:
                                    if type(val) is not int:
                                        return make_response(jsonify(
                                            {'msg': 'Bad Request - [{}] in list must be integer'.format(val)})), 400

                return f(*args, **kwargs)

            return decorated

        return real_validate_request

    @staticmethod
    def validator(rules):
        """
        :rules: list -  The sets of keys and rules to be applied
        example: [username|required:max-255:min-120, email|required:email]
        """

        def real_validate_request(f):

            @wraps(f)
            def decorated(*args, **kwargs):
                if not request.json:
                    return make_response(jsonify({'msg': 'Bad Request - Request Must be JSON Formatted'})), 400

                payload = request.get_json()

                if payload:
                    # Loop through all validation rules
                    for rule in rules:
                        rule_array = rule.split('|')

                        request_key = rule_array[0]
                        validators = rule_array[1].split(':')

                        # If the key is not in the request payload, and required is not part of the validator rules,
                        # Continue the loop to avoid key errors.
                        if request_key not in payload and 'required' not in validators:
                            continue

                        # Loop all validators specified in the current rule
                        for validator in validators:

                            if validator == 'int' and type(payload[request_key]) is str and not payload[
                                    request_key].isdigit():
                                return make_response(
                                    jsonify({'msg': 'Bad Request - {} must be integer'.format(request_key)})), 400

                            if validator == 'float':
                                try:
                                    float(payload[request_key])
                                except Exception as e:
                                    return make_response(
                                        jsonify({'msg': 'Bad Request - {} must be float'.format(request_key)})), 400

                            if (validator == 'required' and request_key not in payload) or payload[request_key] == '':
                                return make_response(
                                    jsonify({'msg': 'Bad Request - {} is required'.format(request_key)})), 400

                            if validator.find('max') > -1:
                                max_value = int(validator.split('-')[1])
                                if int(payload[request_key]) > max_value:
                                    return make_response(
                                        jsonify({'msg': 'Bad Request - {} can only have a max value of {}'.format(
                                            request_key, max_value)})), 400

                            if validator.find('min') > -1:
                                min_value = int(validator.split('-')[1])
                                if int(payload[request_key]) < min_value:
                                    return make_response(
                                        jsonify({'msg': 'Bad Request - {} can only have a min value of {}'.format(
                                            request_key, min_value)})), 400

                            if validator.find('length') > -1:
                                length_value = int(validator.split('-')[1])
                                if len(str(payload[request_key])) > length_value:
                                    return make_response(
                                        jsonify({'msg': 'Bad Request - {} can only have a len of {}'.format(
                                            request_key, length_value)})), 400

                            if validator == 'exists':
                                import importlib
                                from app.utils import to_pascal_case

                                repo_name = rule_array[2]
                                column_name = rule_array[3]

                                rep = 'app.repositories.{}_repo'.format(
                                    repo_name)
                                mod = importlib.import_module(rep)
                                repo_class = getattr(
                                    mod, '{}Repo'.format(to_pascal_case(repo_name)))
                                repo = repo_class()

                                if type(payload[request_key]) == int:
                                    v = repo.find_first(
                                        **{column_name: payload[request_key]})

                                    if not v:
                                        return make_response(
                                            jsonify({'msg': 'Bad Request - {} contains invalid {}(s) for {} table '
                                                     .format(request_key, column_name,
                                                             repo_name)})), 400

                                if type(payload[request_key]) == list:
                                    for val in payload[request_key]:
                                        v = repo.find_first(
                                            **{column_name: val})

                                        if not v:
                                            return make_response(
                                                jsonify({'msg': 'Bad Request - {} contains invalid {}(s) for {} table '
                                                         .format(request_key, column_name,
                                                                 repo_name)})), 400

                            if validator == 'date' or validator == 'time':

                                mapper = {
                                    'date': {
                                        'formatter': '%Y-%m-%d',
                                        'format':  'YYYY-MM-DD',
                                        'type': 'date',
                                    },
                                    'time': {
                                        'formatter': '%H:%M',
                                        'format': 'Hrs:Mins. Eg 17:59',
                                        'type': 'time'
                                    }
                                }

                                formatter = mapper.get(validator)

                                try:
                                    datetime.strptime(
                                        payload[request_key], formatter.get('formatter'))
                                except Exception as e:
                                    return make_response(
                                        jsonify({'msg': 'Bad Request - {} should be valid {}. Format: {}'
                                                 .format(request_key, formatter.get('type'), formatter.get('format'))})), 400

                            if validator == 'list' and type(payload[request_key]) is not list:
                                return make_response(
                                    jsonify({'msg': 'Bad Request - {} must be a list'.format(request_key)})), 400

                            if validator == 'list_int':
                                if type(payload[request_key]) is not list:
                                    return make_response(
                                        jsonify({'msg': 'Bad Request - {} must be a list'.format(request_key)})), 400
                                for val in payload[request_key]:
                                    if type(val) is not int:
                                        return make_response(jsonify(
                                            {'msg': 'Bad Request - [{}] in list must be integer'.format(val)})), 400

                            # Validate enums
                            if Security.validate_enums(validator, request_key, payload[request_key]):
                                return Security.validate_enums(validator, request_key, payload[request_key])

                            # validate emails
                            if Security.validate_email(validator, payload[request_key]):
                                return Security.validate_email(validator, payload[request_key])

                            # validate urls
                            if Security.validate_url(validator, payload[request_key]):
                                return Security.validate_url(validator, payload[request_key])

                return f(*args, **kwargs)

            return decorated

        return real_validate_request

    @staticmethod
    def validate_query_params(model):
        from app.controllers import BaseController

        model_columns = model.get_columns()

        model_fields = [column for column in model_columns]

        model_fields_camel = list(
            map(SnakeCaseConversion.snake_to_camel, model_fields))

        controller = BaseController(request)

        def validator(f):

            @wraps(f)
            def decorated(*args, **kwargs):
                queries = request.args
                invalid_query_keys = []

                for key in queries:
                    if SnakeCaseConversion.camel_to_snake(key) not in model_fields:
                        invalid_query_keys.append(key)

                if invalid_query_keys:
                    return make_response(
                        jsonify({'msg': 'Invalid keys {}. The supported keys are {}'
                                 .format(invalid_query_keys, model_fields_camel)})), 400

                for name, val in controller.get_params_dict().items():
                    if name.endswith('ted_at'):
                        try:
                            # kwargs.__setitem__(name, datetime.strptime(val, '%Y-%m-%d'))
                            datetime.strptime(val, '%Y-%m-%d')

                        except Exception:
                            return controller.handle_response(
                                f"Bad Request - '{name}' should be valid date. Format: YYYY-MM-DD", status_code=400
                            )

                return f(*args, **kwargs)

            return decorated

        return validator

    @staticmethod
    def validate_enums(validator, key, value):

        split_validator = validator.split('_')

        enum_mapper = {
            'FaqCategoryType': [value.value for value in FaqCategoryType.__members__.values()],
            'MealSessionNames': [value.value for value in MealSessionNames.__members__.values()],
            'MealTypes': [value.value for value in MealTypes.__members__.values()],
            'MealPeriods': [value.value for value in MealPeriods.__members__.values()],
        }

        if split_validator[0] == 'enum':

            enum_values = enum_mapper.get(split_validator[1])

            if value not in enum_values:

                return make_response(jsonify(
                    {'msg': "Bad Request - '{}' is not a valid value for key '{}'. "
                     "values must be any of the following {}".format(value, key, enum_values)})), 400

    @classmethod
    def validate_email(cls, validator, value):

        if validator == 'email':
            if not cls.EMAIL_REGEX.match(value):
                return make_response(jsonify(
                    {'msg': "Bad Request - '{}' is not a valid email address.".format(value)})), 400

    @classmethod
    def validate_url(cls, validator, value):

        if validator == 'url':
            if not re.match(cls.URL_REGEX, value):
                return make_response(jsonify(
                    {'msg': "Bad Request - '{}' is not a valid url.".format(value)})), 400
