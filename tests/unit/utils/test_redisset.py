from tests.base_test_case import BaseTestCase
from app.utils.redisset import RedisSet


class TestRedisSet(BaseTestCase):

    def setUp(self):
        self.BaseSetUp()
        self.redis_set = RedisSet()

    def tearDown(self):
        self.BaseTearDown()

    def test_push(self):
        self.redis_set.push('a')
        self.redis_set.push('b')
        self.redis_set.push('c')
        values = self.redis_set.zrange(0, 3)
        self.assertEquals(values, ['a', 'b', 'c'])
        self.redis_set.push('b')
        self.redis_set.push('a')
        values = self.redis_set.zrange(0, 5)
        self.assertEquals(values, ['a', 'b', 'c'])

    def test_get(self):
        """all valid prefixes should return abracadabra"""
        items = 'abracadabra'
        for i, item in enumerate(items):
            self.redis_set.push(items[0:i])

        self.redis_set.push(items, True)

        # all valid prefixes should return abracadabra
        values = self.redis_set.get('a')
        self.assertTrue(items in values)

        values = self.redis_set.get('ab')
        self.assertTrue(items in values)

        values = self.redis_set.get('abr')
        self.assertTrue(items in values)

        values = self.redis_set.get('aa')
        self.assertFalse(items in values)

        values = self.redis_set.get('abracadx')
        self.assertFalse(items in values)
