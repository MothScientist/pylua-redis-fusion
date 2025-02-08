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
    def __init__(self, host='localhost', port=6379, password='',username='default', db=0, socket_timeout=None):
        self.redis = Redis(
            connection_pool=rConnectionPool(
                host=host,
                port=port,
                password=password,
                username=username,
                db=db,
                socket_timeout=socket_timeout,
                encoding='utf-8',
                decode_responses=True
            )
        )
        self.lua_scripts = dict()  # storing registered lua scripts
        self.lua_scripts['rename_key'] = PyRedis.__load_lua_script('rename_key')
        self.lua_scripts['remove_all_keys'] = PyRedis.__load_lua_script('remove_all_keys')

    def r_ping(self) -> bool:
        try:
            return self.redis.ping()
        except (rConnectionError, rTimeoutError):
            return False

    def key_is_exist(self, key: str) -> bool:
        return bool(self.redis.exists(key))

    def r_set(
            self,
            key: str | dict,
            value: int | float | str | list | tuple | set | frozenset | None,
            get_old_value: bool = None,
            convert_to_type_for_get: str = None,
            time_ms=None,
            time_s=None,
            if_exist: bool = False,
            if_not_exist: bool = False,
            keep_ttl: bool = False
    ) -> None | str:
        """
        Set a new key or override an existing one
        If both parameters (time_s, time_ms) are specified, the key will be deleted based on the smallest value.
        :param key:
        :param value: IMPORTANT: not considered if a dict type object was passed in key.
        :param get_old_value: return the old value stored at key, or None if the key did not exist.
        :param convert_to_type_for_get: parameter for 'get_old_value', similar to the action in the 'get' function
        :param time_ms: key lifetime in milliseconds.
        :param time_s: key lifetime in seconds.
        :param if_exist: set value only if such key already exists.
        :param if_not_exist: set value only if such key does not exist yet.
        :param keep_ttl: retain the time to live associated with the key (only for bool/int/float/str).
        :return: None
        """
        if key is value is None:
            return

        key_exist: bool | None = None
        if (if_exist or if_not_exist) and not isinstance(key, dict):
            key_exist: bool = self.key_is_exist(key)

        if time_s or time_ms:
            time_s, time_ms = None, PyRedis.__compare_and_select_sec_ms(time_s, time_ms)

        res = None
        if get_old_value:
            # Moved to a separate block, not as a parameter,
            # because this library allows you to write after integer in this key, for example, list.
            # Therefore, it is necessary to get the old value separately,
            # although the set function has a built-in parameter for this, it is not suitable for this function
            res = self.r_get(key, convert_to_type=convert_to_type_for_get)

        if isinstance(key, dict):
            # TODO - key_exists if dict
            self.__r_set_dict_helper(key, time_ms=time_ms, if_exist=if_exist, if_not_exist=if_not_exist)

        elif isinstance(value, (bool, int, float, str)):
            self.redis.set(
                key,
                str(value) if isinstance(value, bool) else value,
                nx=if_not_exist,
                xx=if_exist,
                keepttl=keep_ttl,
                ex=time_s,
                px=time_ms
            )

        elif isinstance(value, (list, tuple, set, frozenset)):
            self.__r_set_array_helper(
                key,
                value,
                time_ms=time_ms,
                if_exist=if_exist,
                if_not_exist=if_not_exist,
                key_exist=key_exist
            )

        return res

    def __r_set_array_helper(
            self,
            key: str,
            value: list | tuple | set | frozenset,
            time_ms: int | None,
            if_exist: bool | None,
            if_not_exist: bool | None,
            key_exist: bool | None
    ) -> None:
        # if such a key already exists, it must be cleared before writing, otherwise it will simply expand
        key_exist: bool = self.key_is_exist(key) if key_exist is None else key_exist
        if key_exist:
            self.r_delete(key)

        elif (if_exist and not key_exist) or (if_not_exist and key_exist):
            return

        if any(isinstance(element, bool) for element in value):
            # if there are values of type bool, then we convert them to strings
            value = tuple(str(element) if isinstance(element, bool) else element for element in value)
        self.redis.rpush(key, *value)
        if time_ms:
            self.redis.pexpire(key, time_ms, if_exist, if_not_exist)

    def __r_set_dict_helper(
            self,
            key: dict,
            time_ms: int | None,
            if_exist: bool | None,
            if_not_exist: bool | None
    ) -> None:
        pass  # TODO

    def r_get(self, key: str, default_value=None, convert_to_type: str = None):
        """
        Used both to get a value by key and to check for its existence
        :param key:
        :param default_value: value that will be returned if there is no such key.
        :param convert_to_type: bool/int/float (by default all output data is of type str after decode() function)
        :return: value, none or default_value
        """
        if not key:
            return default_value  # default_value or None

        value_type = self.redis.type(key)

        if value_type == 'string':
            res = self.redis.get(key) or None
        elif value_type == 'list':
            res = [byte for byte in self.redis.lrange(key, 0, -1)]
        else:  # value_type = 'none'
            return default_value

        return PyRedis.__convert_to_type(res, convert_to_type) if convert_to_type else res

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
            return None

        value = self.r_get(key, convert_to_type=convert_to_type_for_return) if returning else None
        self.redis.delete(key)
        return value

    def rename_key(self, key: str, new_key: str, get_rename_status: bool = None):  # TODO tests
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
    ) -> tuple[tuple, tuple, dict]:
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

    def r_mass_check_keys_exists(self, keys: list | tuple | set | frozenset) -> tuple:
        """
        Mass operation to check for keys
        """
        if not keys:
            return ()

        keys: tuple = PyRedis.__remove_duplicates(keys)  # remove duplicates
        existing_keys = self.redis.mget(keys)

        # filter only those keys whose values is not None
        return tuple(keys[i] for i, value in enumerate(existing_keys) if value is not None)

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
        count_keys = self.__register_lua_scripts('remove_all_keys', 0, '1' if get_count_keys else '0')
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
                _true: tuple = ('1', 'True', 'true')
                value: bool | str = (value in _true) if value in ('0', 'False', 'false', *_true) else value

        except ValueError:
            pass
        return value

    @staticmethod
    def __compare_and_select_sec_ms(time_s: float, time_ms: float) -> float:
        """
        If both seconds and milliseconds are specified,
        the time is converted to milliseconds and the smallest one is selected
        """
        return min(time_s * 1_000, time_ms) if (time_s and time_ms) else (time_s * 1_000 if time_s else time_ms)

    @staticmethod
    def __remove_duplicates(iterable_var: list | tuple | set | frozenset) -> tuple:
        if isinstance(iterable_var, (set, frozenset)):
            return tuple(iterable_var)
        return tuple(set(iterable_var))

    @staticmethod
    def __load_lua_script(filename: str):
        """ Load Lua script from a file """
        curr_dir = os_path.dirname(__file__)
        with open(os_path.join(curr_dir, f'scripts/{filename}.lua'), 'r') as lua_file:
            return lua_file.read()
