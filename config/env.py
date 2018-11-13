from config import get_env


class EnvConfig(object):
    """Parent configuration class."""
    DEBUG = False
    CSRF_ENABLED = True
    SECRET = get_env('SECRET')
    SQLALCHEMY_DATABASE_URI = get_env('DATABASE_URL')
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
    SQLALCHEMY_DATABASE_URI = 'sqlite:///andelaeats.db'
    DEBUG = True


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
