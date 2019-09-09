# -*- coding: utf-8 -*-
"""Application configuration.

Most configuration is set via environment variables.

For local development, use a .env file to set
environment variables.
"""
import logging
import sys

from environs import Env

logger = logging.getLogger(__name__)

env = Env()
env.read_env()

APP_ENV = env.str("FLASK_ENV", default="development")

TESTING = sys.argv[0].endswith("pytest")
if TESTING:
    logger.info(f"Running tests: {sys.argv}")


# AndelaEats
SECRET_KEY = env.str("SECRET_KEY")
BCRYPT_LOG_ROUNDS = env.int("BCRYPT_LOG_ROUNDS", default=13)
CACHE_TYPE = "simple"  # Can be 'memcached', 'redis', etc.
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Debugging
DEBUG = APP_ENV == "development"
DEBUG_TB_ENABLED = DEBUG
DEBUG_TB_INTERCEPT_REDIRECTS = False

# Postgres
SQLALCHEMY_DATABASE_URI = env.str("DATABASE_URL")

# Redis
REDIS_URL = env.str("REDIS_URL")
# redis socket connection timeout
REDIS_SOCKET_TIMEOUT = env.int("REDIS_SOCKET_TIMEOUT", default=5)

# JWT
JWT_PUBLIC_KEY = env.str("JWT_PUBLIC_KEY")
JWT_ALGORITHM = env.str("JWT_ALGORITHM", default="HS256")
JWT_AUTH_SCHEME = env.str("JWT_AUTH_SCHEME", default="JWT")


# Andela API token
ANDELA_API_TOKEN = env.str("ANDELA_API_TOKEN")
API_AUTH_URL = env.str("API_AUTH_URL")


# slack token
SLACK_TOKEN = env.str("SLACK_TOKEN")
