"""
Client for working with the Redis database
"""

from os import getenv
from dotenv import load_dotenv
from redis import (Redis, ConnectionPool as rConnectionPool, ConnectionError as rConnectionError,
                   TimeoutError as rTimeoutError)


load_dotenv('redis.env')  # Load environment variables from redis.env file
redis_psw: str = getenv('REDIS_PSW')
redis_db: int = int(getenv('REDIS_DB'))
redis_host: str = getenv('REDIS_HOST')
redis_port: int = int(getenv('REDIS_PORT'))


class PyRedis:
    """
    The main entity for working with Redis
    """
    def __init__(self, host, port, psw, db=0, socket_timeout=None):
        self.redis = Redis(
            connection_pool=rConnectionPool(
                host=host,
                port=port,
                db=db,
                password=psw,
                socket_timeout=socket_timeout
            )
        )

    def r_ping(self) -> bool:
        try:
            return self.redis.ping()
        except (rConnectionError, rTimeoutError):
            return False

    def r_set(
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
        :param time_ms: key lifetime in milliseconds
        :param time_s: key lifetime in seconds
        :param if_exist: set value only if such key already exists
        :param if_not_exist: set value only if such key does not exist yet
        :return: None
        """
        if key is value is None:
            return

        if time_s and time_ms:
            time_s, time_ms = None, PyRedis.compare_and_select_seconds_and_milliseconds(time_s, time_ms)

        self.redis.set(key, value, nx=if_not_exist, xx=if_exist, ex=time_s, px=time_ms)

    def r_get(self, key, default_value=None):
        """
        Used both to get a value by key and to check for its existence
        :param key:
        :param default_value: value that will be returned if there is no such key.
        :return:
        """
        if not key:
            return default_value  # default_value or None

        res = self.redis.get(key)
        return res or default_value

    def r_delete(self, key, returning: bool = False):
        """
        Delete a key
        getdel function is not suitable because it only works for string values
        (https://redis.io/docs/latest/commands/getdel/)
        :param key:
        :param returning: return the value the key had before deletion
        :return: value or None
        """
        if not key:
            return None

        res = self.redis.get(key) if returning else None
        self.redis.delete(key)
        return res

    def r_mass_delete(
            self,
            keys: list | tuple | set | frozenset,
            return_exists: bool | None = None,
            return_non_exists: bool | None = None,
            get_dict_key_value_exists: bool | None = None
    ) -> tuple[tuple, tuple, dict]:
        """
        Mass delete keys from a given iterable
        :param keys:
        :param return_exists: return keys that existed and were deleted
        :param return_non_exists: return keys that were not found
        :param get_dict_key_value_exists: get dictionary of remote keys with values
        :return: ((return_exists), (return_non_exists), {get_dict_key_value_exists})
        """
        if not keys:
            return (), (), {}

        keys: tuple = PyRedis.remove_duplicates(keys)  # remove duplicates
        return_exists: list | None = [] if return_exists else None
        return_non_exists: list | None = [] if return_non_exists else None
        get_dict_key_value_exists: dict | None = {} if get_dict_key_value_exists else None

        # all parameters = None (None is None is None -> True)
        if return_exists is return_non_exists is get_dict_key_value_exists:
            self.redis.delete(*keys)
            return (), (), {}

        # if one of the parameters is specified, then we collect a dictionary of existing key-values
        exists_key_value: dict = self.check_keys_and_get_values(keys)
        non_exists_keys: tuple = tuple(frozenset(keys).difference(frozenset(exists_key_value)))

        return (
            non_exists_keys if return_non_exists is not None else (),
            tuple(exists_key_value.keys()) if return_exists is not None else (),
            exists_key_value if get_dict_key_value_exists is not None else {}
        )

    def r_mass_check_keys_exists(self, keys: list | tuple | set | frozenset) -> tuple:
        if not keys:
            return ()

        keys: tuple = PyRedis.remove_duplicates(keys)  # remove duplicates
        existing_keys = self.redis.mget(keys)

        # filter only those keys whose values is not None
        return tuple(keys[i] for i, value in enumerate(existing_keys) if value is not None)

    def check_keys_and_get_values(self, keys: list | tuple | set | frozenset) -> dict:
        """
        Checks for the existence of keys in Redis and returns a dictionary of existing keys with their values
        """
        keys: tuple = PyRedis.remove_duplicates(keys)  # remove duplicates
        values = self.redis.mget(keys)  # later in the library the variable is converted to list
        return {keys[i]: value for i, value in enumerate(values) if value is not None}

    @staticmethod
    def compare_and_select_seconds_and_milliseconds(time_s: float, time_ms: float) -> float:
        """
        If both seconds and milliseconds are specified,
        the time is converted to milliseconds and the smallest one is selected
        """
        return min(time_s * 1_000, time_ms)

    @staticmethod
    def remove_duplicates(iterable_var: list | tuple | set | frozenset) -> tuple:
        if isinstance(iterable_var, (set, frozenset)):
            return tuple(iterable_var)
        return tuple(set(iterable_var))


r = PyRedis(redis_host, redis_port, redis_psw, db=redis_db, socket_timeout=.001)
print(r.r_ping())
