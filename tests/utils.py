import jwt
from faker import Faker
from flask import current_app, testing
from werkzeug.datastructures import Headers

fake = Faker()


class TestClient(testing.FlaskClient):
    def open(self, *args, **kwargs):
        api_key_headers = Headers(headers())
        new_header = kwargs.pop("headers", Headers())
        new_header.extend(api_key_headers)
        kwargs["headers"] = new_header
        return super().open(*args, **kwargs)


class User:
    """Class for creating user mocks"""

    def __init__(self):
        self.first_name = fake.first_name()
        self.id = "-LG__88sozO1OGrqda2z"
        self.last_name = fake.last_name()
        self.firstName = self.first_name
        self.lastName = self.last_name
        self.email = fake.email()
        self.name = f"{self.first_name} {self.last_name}"
        self.picture = fake.image_url(height=None, width=None)
        self.roles = {
            "Technology": "-KXH7iME4ebMEXAEc7HP",
            "Andelan": "-KiihfZoseQeqC6bWTau",
        }

    def to_dict(self):
        """Converts the instance of this class to a dict.
        Returns:
            dict : User data dictionary.
        """
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "firstName": self.firstName,
            "lastName": self.lastName,
            "email": self.email,
            "name": self.name,
            "picture": self.picture,
            "roles": self.roles,
        }


def headers(location_id=1):
    return {
        "Content-Type": "application/json",
        "X-Location": f"{location_id}",
        "Authorization": "Bearer {}".format(generate_token()),
    }


def generate_token(exp=None):
    """
    Generates jwt tokens for testing purpose
    params:
        exp: Token Expiration. This could be datetime object or an integer
    result:
        token: This is the bearer token in this format 'Bearer token'
    """

    secret_key = current_app.config.get("JWT_SECRET_KEY")
    payload = {
        "UserInfo": User().to_dict(),
        "iss": "accounts.andela.com",
        "aud": "andela.com",
    }
    payload.__setitem__("exp", exp) if exp is not None else ""

    token = jwt.encode(payload, secret_key, algorithm="RS256").decode("utf-8")
    return token
