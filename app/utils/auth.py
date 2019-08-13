import jwt
from os import getenv
from base64 import b64decode
from functools import wraps
from flask import request, jsonify, make_response
from app.repositories.permission_repo import PermissionRepo
from app.repositories.user_role_repo import UserRoleRepo
from app.repositories.role_repo import RoleRepo


class Auth:
    ''' This class will house Authentication and Authorization Methods '''

    ''' Routes The Location Header Should  Not Be Applied Ignore'''
    location_header_ignore = [
        '/locations', '/docs', '/apidocs', '/flasgger_static', '/apispec_1.json', '/bot'
    ]

    ''' Routes The Authentication Header Should  Not Be Applied Ignore'''
    authentication_header_ignore = [
        '/docs', '/apidocs', '/flasgger_static', '/apispec_1.json', '/bot'
    ]

    @staticmethod
    def check_token():
        if request.method != 'OPTIONS':

            for endpoint in Auth.authentication_header_ignore:
                # If endpoint in request.path, ignore this check
                if endpoint in request.path:
                    return None

            try:
                token = Auth.get_token()
            except Exception as e:
                return make_response(jsonify({'msg': str(e)}), 400)

            try:
                decoded = Auth.decode_token(token)
            except Exception as e:
                return make_response(jsonify({'msg': str(e)}), 400)

    @staticmethod
    def _get_user():
        token = None
        try:
            token = Auth.get_token()
        except Exception as e:
            raise e

        try:
            if token:
                return Auth.decode_token(token)['UserInfo']
        except Exception as e:
            raise e

    @staticmethod
    def _get_jwt_public_key():
        def decode_public_key(key_64): return b64decode(key_64).decode('utf-8')

        jwt_env_mapper = {
            'testing': 'JWT_PUBLIC_KEY_TEST',
            'production': 'JWT_PUBLIC_KEY',
            'development': 'JWT_PUBLIC_KEY',
            'staging': 'JWT_PUBLIC_KEY'
        }

        public_key_mapper = {
            'testing': lambda key_64: key_64,
            'development': decode_public_key,
            'production': decode_public_key,
            'staging': decode_public_key,
        }

        app_env = getenv('APP_ENV', 'production')

        public_key_64 = getenv(jwt_env_mapper.get(app_env, 'JWT_PUBLIC_KEY'))

        public_key = public_key_mapper.get(
            app_env, decode_public_key)(public_key_64)

        return public_key

    @staticmethod
    def user(*keys):
        user = Auth._get_user()
        if keys:
            if len(keys) > 1:
                values = list()
                for key in keys:
                    values.append(
                        user[key]) if key in user else values.append(None)
                return values
            if len(keys) == 1 and keys[0] in user:
                return user[keys[0]]

        return user

    @staticmethod
    def get_token(request_obj=None):
        if request_obj:
            header = request_obj.headers.get('Authorization', None)
        else:
            header = request.headers.get('Authorization', None)
        if not header:
            raise Exception('Authorization Header is Expected')

        header_parts = header.split()

        if header_parts[0].lower() != 'bearer':
            raise Exception('Authorization Header Must Start With Bearer')
        elif len(header_parts) > 1:
            return header_parts[1]

        raise Exception('Internal Application Error')

    @staticmethod
    def decode_token(token):

        public_key = Auth._get_jwt_public_key()

        try:
            decoded = jwt.decode(
                token,
                public_key,
                algorithms=['RS256'],
                audience='andela.com',
                issuer="accounts.andela.com",
                options={
                    'verify_signature': True,
                    'verify_exp': True
                })
            return decoded
        except jwt.ExpiredSignature:
            raise Exception('Token is Expired')
        except jwt.DecodeError:
            raise Exception('Error Decoding')

    @staticmethod
    def check_location_header():
        if request.method != 'OPTIONS':
            for endpoint in Auth.location_header_ignore:
                # If endpoint in request.path, ignore this check
                if request.path.find(endpoint) > -1:
                    return None
            try:
                Auth.get_location()
            except Exception as e:
                return make_response(jsonify({'msg': str(e)}), 400)

    @staticmethod
    def get_location():
        location = request.headers.get('X-Location', None)
        if not location:
            raise Exception('Location Header is Expected')
        if not location.isdigit():
            raise Exception('Location Header Value is Invalid')
        return int(location)

    @staticmethod
    def has_role(role):

        def role_checker(f):

            @wraps(f)
            def decorated(*args, **kwargs):

                user_role_repo = UserRoleRepo()

                role_repo = RoleRepo()

                user_id = Auth.user('id')
                user_role = user_role_repo.find_first(**{'user_id': user_id})

                if not user_id:
                    return make_response(jsonify({'msg': 'Missing User ID in token'})), 401

                if not user_role:
                    return make_response(jsonify({'msg': 'Access Error - No Role Granted'})), 401

                if role_repo.get(user_role.role_id).name != role:
                    return make_response(
                        jsonify({'msg': 'Access Error - This role does not have the access rights'}
                                )
                    ), 401

                return f(*args, **kwargs)

            return decorated

        return role_checker

    @staticmethod
    def has_permission(permission):

        def permission_checker(f):

            @wraps(f)
            def decorated(*args, **kwargs):
                user_role_repo = UserRoleRepo()
                permission_repo = PermissionRepo()

                user_id = Auth.user('id')
                user_role = user_role_repo.find_first(**{'user_id': user_id})

                if not user_id:
                    return make_response(jsonify({'msg': 'Missing User ID in token'})), 401

                if not user_role:
                    return make_response(jsonify({'msg': 'Access Error - No Role Granted'})), 401

                user_perms = permission_repo.get_unpaginated(
                    **{'role_id': user_role.role_id})

                perms = [perm.keyword for perm in user_perms]
                if len(perms) == 0:
                    return make_response(jsonify({'msg': 'Access Error - No Permission Granted'})), 401

                if permission not in perms:
                    return make_response(jsonify({'msg': 'Access Error - Permission Denied'})), 401

                return f(*args, **kwargs)

            return decorated
        return permission_checker
