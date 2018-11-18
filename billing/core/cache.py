import redis

from billing.config import settings

__all__ = [
    'cache'
]


class Cache:

    def __init__(self):
        self.client = redis.StrictRedis(settings.REDIS_URL)
        self.timeout = settings.RATES_CACHE_TIMEOUT

    def get(self, key):
        self.client.get(key)

    def set(self, key, value):
        self.client.set(key, value)
        self.client.expire(key, self.timeout)


cache = Cache()
