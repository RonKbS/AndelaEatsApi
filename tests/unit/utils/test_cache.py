from tests.base_test_case import BaseTestCase
from datetime import datetime
from app.utils.cache import Cache
from unittest.mock import patch
import json


class MockObj:
    def set(self, key, value):
        return {str(key): value}

    def get(self, key):
        if key:
            return json.dumps(key)
        return key


class MockRedis:

    @staticmethod
    def StrictRedis(*args, **kwargs):
        return MockObj()

    @staticmethod
    def ConnectionPool(*args, **kwargs):
        return 1


class TestCache(BaseTestCase):

    def setUp(self):
        self.BaseSetUp()

    def test_set_method(self):
        with patch('app.utils.cache.redis', new_callable=MockRedis):

            obj = datetime.now()
            response = Cache().set('test_key', obj)

            if not response:
                assert True
            else:
                assert False

    def test_get_method(self):
        with patch('app.utils.cache.redis', new_callable=MockRedis):
            response = Cache().get('test_key')

            if not response:
                assert False
            else:
                assert True

    def test_get_method_empty_object(self):
        with patch('app.utils.cache.redis', new_callable=MockRedis):
            response = Cache().get('')

            if not response:
                assert True
            else:
                assert False


