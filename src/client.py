"""
Client for working with the Redis database
Original library documentation: https://redis-py.readthedocs.io/en/stable/index.html
"""
from os import path as os_path
from redis import (
    Redis,
    ConnectionPool as rConnectionPool,
    ConnectionError as rConnectionError,
    TimeoutError as rTimeoutError
)


class PyRedis:
    """
    The main entity for working with Redis
    """
    def __init__(
            self, host: str = 'localhost', port: int = 6379, password='',username='default', db=0,
            socket_timeout: int | float = 0.1, retry_on_timeout: bool = True
    ):
        self.redis = Redis(
            connection_pool=rConnectionPool(
                host=host,
                port=port,
                password=password,
                username=username,
                db=db,
                socket_timeout=socket_timeout,
                encoding='utf-8',
                decode_responses=True,
                retry_on_timeout=retry_on_timeout
            )
        )

        # storing registered lua scripts
        self.lua_scripts = {
            'rename_key': PyRedis.__load_lua_script('rename_key'),
            'remove_all_keys': PyRedis.__load_lua_script('remove_all_keys'),
            'rpush_helper': PyRedis.__load_lua_script('rpush_helper'),
            'get_helper': PyRedis.__load_lua_script('get_helper'),
            'delete_with_returning': PyRedis.__load_lua_script('delete_with_returning'),
            'unlink_with_returning': PyRedis.__load_lua_script('unlink_with_returning'),
            'set_not_array_helper': PyRedis.__load_lua_script('set_not_array_helper'),
            'set_keys_ttl': PyRedis.__load_lua_script('set_keys_ttl'),
            'drop_keys_ttl': PyRedis.__load_lua_script('drop_keys_ttl'),
        }

    def r_ping(self) -> bool:
        try:
            return self.redis.ping()
        except (rConnectionError, rTimeoutError):
            return False

    def key_is_exist(self, key: str) -> bool | None:
        return bool(self.redis.exists(key)) if key else None

    def keys_is_exist(self, keys: list[str] | tuple[str] | set[str] | frozenset[str]) -> int:
        """
        Mass operation to check for keys
        """
        return self.redis.exists(*keys) if keys else 0

    def get_count_of_keys(self) -> int:
        """ Returns the number of keys in the current database """
        return self.redis.dbsize()

    def set_key_ttl(
            self,
            key: str,
            ttl_sec: int | None = None,
            ttl_ms: int | None = None
    ) -> None:
        """ Set key time (ttl) in seconds or milliseconds """
        if ttl_ms := PyRedis.__compare_and_select_sec_ms(ttl_sec, ttl_ms) if (ttl_sec or ttl_ms) else None:
            self.redis.pexpire(key, ttl_ms)

    def set_keys_ttl(
            self,
            keys: list[str] | tuple[str] | set[str] | frozenset[str],
            ttl_sec: int | None = None,
            ttl_ms: int | None = None
    ) -> None:
        keys: tuple = PyRedis.__remove_duplicates(keys)
        ttl_ms = PyRedis.__compare_and_select_sec_ms(ttl_sec, ttl_ms) if ((ttl_sec or ttl_ms) and keys) else None
        if ttl_ms:
            self.__register_lua_scripts('set_keys_ttl', len(keys), *keys, ttl_ms)

    def get_key_ttl(self, key: str, in_seconds: bool = False) -> int | None:
        """
        Returns the remaining time to live of a key that has a timeout
        :param key:
        :param in_seconds:
        :return: ttl in seconds;
        return None if the key does not exist;
        return 0 if the key exists but has no associated expire;
        """
        res = self.redis.ttl(key) if in_seconds else self.redis.pttl(key)
        return res if res not in (-1, -2) else (0 if res == -1 else None)

    def drop_key_ttl(self, key: str):
        """ Removes the key lifetime (ttl) if one is set """
        if key:
            self.redis.persist(key)

    def drop_keys_ttl(self, keys: list[str] | tuple[str] | set[str] | frozenset[str]):
        if keys := PyRedis.__remove_duplicates(keys):
            self.__register_lua_scripts('drop_keys_ttl', len(keys), *keys)

    def get_type_value_of_key(self, key: str) -> str | None:
        """
        The type of value stored at this key
        :param key:
        :return: str or None
        """
        res = self.redis.type(key) if key else None
        return res if res != 'none' else None

    def r_set(
            self,
            key: str | dict,
            value: int | float | str | list | tuple | set | frozenset | None,
            get_old_value: bool = False,
            convert_to_type_for_get: str = None,
            time_ms: int | None = None,
            time_s: int | None = None,
            if_exist: bool = False,
            if_not_exist: bool = False,
            keep_ttl: bool = False
    ) -> None | str | int | float | bool | list:
        """
        Set a new key or override an existing one
        If both parameters (time_s, time_ms) are specified, the key will be deleted based on the smallest value.

        WARNING: If keep_ttl is specified, time_ms and time_s will be ignored if such a key exists,
        if such a key did not exist before, time_ms and time_s will work as usual.
        :param key:
        :param value: IMPORTANT: not considered if a dict type object was passed in key.
        :param get_old_value: return the old value stored at key, or None if the key did not exist.
        :param convert_to_type_for_get: parameter for 'get_old_value', similar to the action in the 'get' function
        :param time_ms: key lifetime in milliseconds.
        :param time_s: key lifetime in seconds.
        :param if_exist: set value only if such key already exists.
        :param if_not_exist: set value only if such key does not exist yet.
        :param keep_ttl: retain the time to live associated with the key.  # TODO - tests
        :return: None
        """
        if not key or value is None:
            return

        if time_s or time_ms:
            time_s, time_ms = None, PyRedis.__compare_and_select_sec_ms(time_s, time_ms)

        res = None

        if isinstance(key, dict):
            # TODO - key_exists if dict + get_old_value
            pass

        elif isinstance(value, (bool, int, float, str)):
            res = self.__register_lua_scripts(
                'set_not_array_helper', 1, key,
                str(int(get_old_value)),
                str(time_ms or 0),
                str(int(if_exist)),
                str(int(if_not_exist)),
                str(int(keep_ttl)),
                str(value)
            )

        elif isinstance(value, (list, tuple, set, frozenset)):
            value = tuple(str(element) for element in value)
            res = self.__register_lua_scripts(
                'rpush_helper', 1, key,
                str(int(get_old_value)), str(time_ms or 0), str(int(if_exist)), str(int(if_not_exist)),
                str(int(keep_ttl)),
                *value
            )

        return PyRedis.__convert_to_type(res, convert_to_type_for_get) if res and convert_to_type_for_get else res

    def r_get(self, key: str, default_value=None, convert_to_type: str = None):
        """
        Used both to get a value by key and to check for its existence
        :param key:
        :param default_value: value that will be returned if there is no such key.
        :param convert_to_type: bool/int/float (by default all output data is of type str after decode() function);
        For float -> int: rounds down to integer part number (drops fractional part)
        :return: value, none or default_value
        """
        if not key:
            return default_value  # default_value or None

        res = self.__register_lua_scripts('get_helper', 1, key) or default_value

        return PyRedis.__convert_to_type(res, convert_to_type) if (convert_to_type and res is not None) else res

    def r_delete(self, key: str, returning: bool = False, convert_to_type_for_return: str = None):
        """
        Delete a key
        'getdel' (from origin module) function is not suitable because it only works for string values
        (https://redis.io/docs/latest/commands/getdel/)
        :param key:
        :param returning: return the value the key had before deletion
        :param convert_to_type_for_return: what type the return value should be converted to (if returning=True)
        :return: value or None
        """
        if not key:
            return

        value = self.__register_lua_scripts('delete_with_returning', 1, key, str(int(returning)))

        if returning and value:
            return PyRedis.__convert_to_type(value, convert_to_type_for_return) if convert_to_type_for_return else value
        return

    def r_unlink(self, key: str, returning: bool = False, convert_to_type_for_return: str = None):
        """
        unlinks is very similar to r_delete: it removes the specified keys.
        The command just unlinks the keys from the keyspace. The actual removal will happen later asynchronously.
        :param key:
        :param returning: return the value the key had before deletion
        :param convert_to_type_for_return: what type the return value should be converted to (if returning=True)
        :return: value or None
        """
        if not key:
            return

        value = self.__register_lua_scripts('unlink_with_returning', 1, key, str(int(returning)))

        if returning and value:
            return PyRedis.__convert_to_type(value, convert_to_type_for_return) if convert_to_type_for_return else value
        return

    def rename_key(self, key: str, new_key: str, get_rename_status: bool = None):
        """
        Change key name
        :param key: current key name
        :param new_key: new key name
        :param get_rename_status: get True if the key exists and has been renamed, False if there is no such key
        :return:
        """
        script = self.__register_lua_scripts('rename_key')
        rename_status = script(keys=[key, new_key])
        return rename_status if get_rename_status else None

    def r_mass_delete(
            self,
            keys: list | tuple | set | frozenset,
            return_exists: bool = False,
            return_non_exists: bool = False,
            get_dict_key_value_exists: bool = False,
            convert_to_type_dict_key: str = None
    ) -> tuple[tuple, tuple, dict]:  # todo - lua
        """
        Mass delete keys from a given iterable.
        Uses the same function as regular r_delete,
        but has a wrapper that allows you to get information about deleted keys.
        :param keys:
        :param return_exists: return keys that existed and were deleted
        :param return_non_exists: return keys that were not found
        :param get_dict_key_value_exists: get dictionary of remote keys with values
        :param convert_to_type_dict_key: is type conversion needed for the returned dictionary
        :return: ((return_exists), (return_non_exists), {get_dict_key_value_exists})
        """
        if not keys:
            return (), (), {}

        keys: tuple = PyRedis.__remove_duplicates(keys)  # remove duplicates

        # all parameters = None (None is None is None -> True)
        if return_exists is return_non_exists is get_dict_key_value_exists is False:
            self.redis.delete(*keys)
            return (), (), {}

        # if one of the parameters is specified, then we collect a dictionary of existing key-values
        exists_key_value: dict = self.check_keys_and_get_values(keys, convert_to_type_dict_key=convert_to_type_dict_key)
        exists_keys: tuple = tuple(exists_key_value.keys())
        non_exists_keys: tuple = tuple(frozenset(keys).difference(frozenset(exists_keys)))
        self.redis.delete(*exists_keys)

        return (
            exists_keys if return_exists else (),
            non_exists_keys if return_non_exists else (),
            exists_key_value if get_dict_key_value_exists else {}
        )

    def r_mass_unlink(
            self,
            keys: list | tuple | set | frozenset,
            return_exists: bool = False,
            return_non_exists: bool = False,
            get_dict_key_value_exists: bool = False,
            convert_to_type_dict_key: str = None
    ) -> tuple[tuple, tuple, dict]:  # TODO - Lua
        if not keys:
            return (), (), {}

        keys: tuple = PyRedis.__remove_duplicates(keys)  # remove duplicates

        # all parameters = None (None is None is None -> True)
        if return_exists is return_non_exists is get_dict_key_value_exists is False:
            self.redis.unlink(*keys)
            return (), (), {}

        # if one of the parameters is specified, then we collect a dictionary of existing key-values
        exists_key_value: dict = self.check_keys_and_get_values(keys, convert_to_type_dict_key=convert_to_type_dict_key)
        exists_keys: tuple = tuple(exists_key_value.keys())
        non_exists_keys: tuple = tuple(frozenset(keys).difference(frozenset(exists_keys)))
        self.redis.unlink(*exists_keys)

        return (
            exists_keys if return_exists else (),
            non_exists_keys if return_non_exists else (),
            exists_key_value if get_dict_key_value_exists else {}
        )

    def check_keys_and_get_values(
            self, keys: list | tuple | set | frozenset,
            convert_to_type_dict_key: str = None
    ) -> dict:
        """
        Checks for the existence of keys in Redis and returns a dictionary of existing keys with their values
        """
        keys: tuple = PyRedis.__remove_duplicates(keys)  # remove duplicates
        values = self.redis.mget(keys)  # later in the library the variable is converted to list
        return {keys[i]: PyRedis.__helper_convert_to_type(value, convert_to_type_dict_key)
                if convert_to_type_dict_key else value for i, value in enumerate(values) if value is not None}

    def r_remove_all_keys(self, get_count_keys: bool = False) -> int | None:
        """
        Delete all keys in all databases on the current host
        :param get_count_keys: need to return the number of deleted keys (True -> return integer, False -> return None)
        :return: count keys or None
        """
        count_keys: int | None = self.__register_lua_scripts('remove_all_keys', 0, str(int(get_count_keys)))
        return int(count_keys) if count_keys else None

    def __register_lua_scripts(self, script_name: str, *args):
        lua_script = self.lua_scripts.get(script_name)
        if args:
            return self.redis.eval(lua_script, *args)
        return self.redis.register_script(lua_script)

    @staticmethod
    def __convert_to_type(value: str | list[str], _type: str) -> str | bool | int | float | list:
        if isinstance(value, list):
            return [PyRedis.__helper_convert_to_type(i, _type) for i in value]
        return PyRedis.__helper_convert_to_type(value, _type)

    @staticmethod
    def __helper_convert_to_type(value: str, _type: str) -> str | int | float:
        try:
            if _type in ('int', 'integer'):

                if '.' in value:
                    # if it`s float, then before converting it`s necessary to slice the fractional part from the string
                    idx: int = value.find('.')
                    value: str = value[:idx]

                value: int = int(value)

            elif _type in ('float', 'double', 'numeric'):
                value: float = float(value)

            elif _type in ('bool', 'boolean'):
                _true: tuple[str, str, str] = ('1', 'True', 'true')
                value: bool | str = (value in _true) if value in ('0', 'False', 'false', *_true) else value

        except (ValueError, TypeError):
            pass
        return value

    @staticmethod
    def __compare_and_select_sec_ms(time_s: int, time_ms: int) -> int:
        """
        If both seconds and milliseconds are specified,
        the time is converted to milliseconds and the smallest one is selected
        """
        res = min(time_s * 1_000, time_ms) if (time_s and time_ms) else (time_s * 1_000 if time_s else time_ms)
        return int(res) if isinstance(res, (int, float)) else None

    @staticmethod
    def __remove_duplicates(iterable_var: list | tuple | set | frozenset) -> tuple:
        if isinstance(iterable_var, (set, frozenset)):
            return tuple(iterable_var)
        return tuple(set(iterable_var))

    @staticmethod
    def __load_lua_script(filename: str) -> str:
        """ Load Lua script from a file """
        curr_dir = os_path.dirname(__file__)
        with open(os_path.join(curr_dir, f'lua_scripts/{filename}.lua'), 'r') as lua_file:
            return lua_file.read()

if __name__ == '__main__':
    from os import getenv
    from dotenv import load_dotenv

    load_dotenv('redis.env')  # Load environment variables from redis.env file
    redis_psw: str = getenv('REDIS_PSW')
    redis_db: int = int(getenv('REDIS_DB'))
    redis_host: str = getenv('REDIS_HOST')
    redis_port: int = int(getenv('REDIS_PORT'))
    r = PyRedis(
            host=redis_host,
            port=redis_port,
            db=0,
            password=redis_psw,
            socket_timeout=.1
        )
    r.r_set('test', 25.234)
    print(r.r_get('test'))
    r.rename_key('test', '123')
    print(r.r_get('test'))
    print(r.r_get('123'))
    res = r.r_remove_all_keys(get_count_keys=True)
    print(res)
    print(type(res))

# TODO - прибавление и убавление значений добавить