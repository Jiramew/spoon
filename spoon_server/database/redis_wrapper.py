import json
import random
import redis


class RedisWrapper(object):
    def __init__(self, host, port, db=0, password=None):
        self._connection = redis.Redis(host=host, port=port, db=db, encoding='utf-8', password=password)

    def get(self, name):
        key = self._connection.hgetall(name=name)
        return random.choice([k.decode("utf-8") for k in key.keys()]) if key else None

    def put(self, name, key):
        key = json.dumps(key) if isinstance(key, (dict, list)) else key
        return self._connection.hincrby(name, key, 1)

    def getvalue(self, name, key):
        value = self._connection.hget(name, key)
        return value if value else None

    def pop(self, name):
        key = self.get(name)
        if key:
            self._connection.hdel(name, key)
        return key

    def len(self, name):
        key = self.get(name)
        if key:
            self._connection.hlen(name)

    def delete(self, name, key):
        self._connection.hdel(name, key)

    def inckey(self, name, key, value):
        self._connection.hincrby(name, key, value)

    def set_value(self, name, key, value):
        self._connection.hset(name, key, value)

    def get_all(self, name):
        return self._connection.hgetall(name).keys()

    def get_status(self, name):
        return self._connection.hlen(name)

    def get_keys(self):
        return self._connection.keys()

    def get_all_kv(self, name):
        return self._connection.hgetall(name)


if __name__ == '__main__':
    redis_con = RedisWrapper('localhost', 6379)
    print(redis_con.get_keys())
