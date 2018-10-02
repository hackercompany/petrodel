import redis
import random
import string

from django.conf import settings


class Methods():
    def __init__(self):
        self.redis = None

    def get_redis_client(self):
        if self.redis is None:
            self.redis = redis.StrictRedis(
                host=settings.REDIS_HOST,
                port=settings.REDIS_PORT, db=settings.REDIS_DB)
        return self.redis

    def get_txn_id(self):
        txn_id = ''.join(
            random.choice(
                string.ascii_uppercase + string.digits) for _ in range(10))
        txn_id = "PTRD" + txn_id
        client = self.get_redis_client()
        exists = client.get(txn_id)
        if exists:
            return self.get_txn_id()
        return txn_id
