import json
import os

import redis


def _get_env_credentials():
    env_data = {"host": os.environ.get("REDIS_HOST", "localhost"),
                "port": int(os.environ.get("REDIS_PORT", 6379)),
                "db": int(os.environ.get("REDIS_DB", 0))}
    return env_data


class RedisClient:
    def __init__(self):
        self._client = redis.Redis(**_get_env_credentials())

    def get(self, key):
        value = self._client.get(key).decode('utf8')
        wrapped_value = json.loads(value)
        return wrapped_value['_value']

    def set(self, key, value):
        dv = {"_value": value}
        self._client.set(key, json.dumps(dv))
        return {'key': key, 'value': value}

    def exists(self, key):
        return self._client.exists(key)

    def delete(self, key):
        self._client.delete(key)

    def get_all(self):
        keys = self._client.keys("*")
        result = []

        for key in keys:
            key = key.decode('utf8')
            key_value = {key: self.get(key)}
            result.append(key_value)

        return result

    def flush_db(self):
        self._client.flushdb()
