from os import getenv
from dotenv import load_dotenv
from redis import Redis, ConnectionPool

class PyRedis:
    def __init__(self, host, port, psw, db=0):
        self.redis = Redis(connection_pool=ConnectionPool(host=host, port=port, db=db, password=psw))

    def set(
            self,
            key: str,
            value,
            time_ms=None,
            time_s=None,
            if_exist: bool = None,
            if_not_exist: bool = None
    ) -> None:
        """
        Set a new key or override an existing one
        If both parameters (time_s, time_ms) are specified, the key will be deleted based on the smallest value.
        :param key:
        :param value:
        :param time_ms:
        :param time_s:
        :param if_exist:
        :param if_not_exist:
        :return: None
        """
        self.redis.set(key, value, nx=if_not_exist, xx=if_exist, ex=time_s, px=time_ms)

    def get(self, key, default_value=None):
        res = self.redis.get(key)
        return res if res else default_value

    def delete(self, key, returning: bool = False):
        """
        Delete a key
        :param key:
        :param returning: Should I return the value that the key had before deletion?
        :return: value or None
        """
        res = self.redis.get(key) if returning else None
        self.redis.delete(key)
        return res


load_dotenv('redis.env')  # Load environment variables from redis.env file
redis_psw: str = getenv('REDIS_PSW')
redis_db: int = int(getenv('REDIS_DB'))
redis_host: str = getenv('REDIS_HOST')
redis_port: int = int(getenv('REDIS_PORT'))

r = PyRedis(redis_host, redis_port, redis_psw, db=redis_db)
