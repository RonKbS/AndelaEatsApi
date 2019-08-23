"""RedisSet class for AndelaEats."""
from redis import Redis
from config import get_env

END_DELIMITER = '%'


class RedisSet(object):
    """
    Implements a simple sorted set with Redis
    """

    def __init__(self, name='redis', namespace='andela', url=None):
        """
        The default connection parameters are:
        host = 'localhost', port = 6379, db = 0
        """
        url = url or get_env('REDIS_URL')
        self.__db = Redis.from_url(
            url, charset="utf-8", decode_responses=True
        )
        self.key = f'{namespace}:{name}'

    def push(self, item, ending=False):
        """Push item onto the sorted set."""
        if ending:
            item = f'{item}{END_DELIMITER}'
        self.__db.zadd(self.key, {item: 0})

    def get(self, prefix, count=50):
        """Get items from the sorted set that match prefix."""
        values = []
        rangelen = 50
        start = self.__db.zrank(self.key, prefix)
        if start is None:
            return []

        while len(values) != count:
            ranges = self.__db.zrange(
                self.key, start, start + rangelen - 1
            )
            start += rangelen
            if not ranges or len(ranges) == 0 or ranges is None:
                break
            for entry in ranges:
                minlen = min(len(entry), len(prefix))
                if entry[0: minlen] != prefix[0: minlen]:
                    count = len(values)
                    break
                if entry[-1] == END_DELIMITER and len(values) != count:
                    values.append(entry[0: -1])
        return values

    def zrange(self, start, stop):
        return self.__db.zrange(
            self.key, start, stop
        )

    def _delete(self):
        self.__db.zremrangebyrank(self.key, 0, -1)
