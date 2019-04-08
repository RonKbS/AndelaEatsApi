from os import environ
from config import get_env
from pathlib import Path  # python3 only

from dotenv import load_dotenv

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path, verbose=True)


class EnvConfig(object):
    """Parent configuration class."""
    DEBUG = False
    CSRF_ENABLED = True
    SECRET = get_env('SECRET')
    SQLALCHEMY_DATABASE_URI = get_env('DATABASE_URL')
    JSON_SORT_KEYS = False
    SWAGGER = {
        'title': 'AndelaEATS API',
        'footer_text': '<b>Copyright Andela Eats</b>',
        'head_text': '<style>.top_text{color: red;}</style>',
        'doc_expansion': "list",
        'ui_params': {
            'apisSorter': 'alpha',
            'operationsSorter': 'alpha',
        },
        'ui_params_text': '''{
            "operationsSorter" : (a, b) => a.get("path").localeCompare(b.get("path"))
            }'''
    }


class DevelopmentEnv(EnvConfig):
    """Configurations for Development."""
    DEBUG = True

class TestingEnv(EnvConfig):
    """Configurations for Testing, with a separate test database."""
    TESTING = True
    # SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/andelaeats_test'
    # SQLALCHEMY_POOL_TIMEOUT = 1000
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///andelaeats.db'
    SQLALCHEMY_DATABASE_URI = get_env('DATABASE_TEST_URL')

    DEBUG = True
    PRESERVE_CONTEXT_ON_EXCEPTION = False

    environ['JWT_SECRET_KEY'] = (
        '-----BEGIN RSA PRIVATE KEY-----\n'
        'MIICWwIBAAKBgQDdlatRjRjogo3WojgGHFHYLugdUWAY9iR3fy4arWNA1KoS8kVw33cJi'
        'bXr8bvwUAUparCwlvdbH6dvEOfou0/gCFQsHUfQrSDv+MuSUMAe8jzKE4qW+jK+xQU9a0'
        '3GUnKHkkle+Q0pX/g6jXZ7r1/xAK5Do2kQ+X5xK9cipRgEKwIDAQABAoGAD+onAtVye4i'
        'c7VR7V50DF9bOnwRwNXrARcDhq9LWNRrRGElESYYTQ6EbatXS3MCyjjX2eMhu/aF5YhXB'
        'wkppwxg+EOmXeh+MzL7Zh284OuPbkglAaGhV9bb6/5CpuGb1esyPbYW+Ty2PC0GSZfIXk'
        'Xs76jXAu9TOBvD0ybc2YlkCQQDywg2R/7t3Q2OE2+yo382CLJdrlSLVROWKwb4tb2PjhY'
        '4XAwV8d1vy0RenxTB+K5Mu57uVSTHtrMK0GAtFr833AkEA6avx20OHo61Yela/4k5kQDt'
        'jEf1N0LfI+BcWZtxsS3jDM3i1Hp0KSu5rsCPb8acJo5RO26gGVrfAsDcIXKC+bQJAZZ2X'
        'IpsitLyPpuiMOvBbzPavd4gY6Z8KWrfYzJoI/Q9FuBo6rKwl4BFoToD7WIUS+hpkagwWi'
        'z+6zLoX1dbOZwJACmH5fSSjAkLRi54PKJ8TFUeOP15h9sQzydI8zJU+upvDEKZsZc/UhT'
        '/SySDOxQ4G/523Y0sz/OZtSWcol/UMgQJALesy++GdvoIDLfJX5GBQpuFgFenRiRDabxr'
        'E9MNUZ2aPFaFp+DyAe+b4nDwuJaW2LURbr8AEZga7oQj0uYxcYw=='
        '\n-----END RSA PRIVATE KEY-----')

    environ['JWT_PUBLIC_KEY_TEST'] = (
        '-----BEGIN PUBLIC KEY-----\n'
        'MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDdlatRjRjogo3WojgGHFHYLugdUWAY9'
        'iR3fy4arWNA1KoS8kVw33cJibXr8bvwUAUparCwlvdbH6dvEOfou0/gCFQsHUfQrSDv+M'
        'uSUMAe8jzKE4qW+jK+xQU9a03GUnKHkkle+Q0pX/g6jXZ7r1/xAK5Do2kQ+X5xK9cipRg'
        'EKwIDAQAB'
        '\n-----END PUBLIC KEY-----')


class StagingEnv(EnvConfig):
    """Configurations for Staging."""
    DEBUG = True
    SWAGGER = {
        'title': 'AndelaEATS API',
        'footer_text': '<b>Copyright Andela Eats</b>',
        'head_text': '<style>.top_text{color: red;}</style>',
        'doc_expansion': "list",
        'ui_params': {
            'apisSorter': 'alpha',
            'operationsSorter': 'alpha',
        },
        'ui_params_text': '''{
                "operationsSorter" : (a, b) => a.get("path").localeCompare(b.get("path"))
                }'''
    }


class ProductionEnv(EnvConfig):
    """Configurations for Production."""
    DEBUG = False
    TESTING = False


app_env = {
    'development': DevelopmentEnv,
    'testing': TestingEnv,
    'staging': StagingEnv,
    'production': ProductionEnv,
}
