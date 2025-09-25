"""
Client for working with the Redis database
Original library documentation: https://redis-py.readthedocs.io/en/stable/index.html
"""
from os import path as os_path
from json import loads as json_loads
from redis import (
    Redis,
    ConnectionPool as rConnectionPool,
    ConnectionError as rConnectionError,
    TimeoutError as rTimeoutError
)

from .data_type_converter import TypeConverter


class PyRedis:
    """
    The main entity for working with Redis
    """
    __slots__ = ('redis', 'curr_dir', 'lua_scripts_sha', 'user_lua_scripts_buffer', 'data_type_converter')

    def __init__(
            self, host: str = 'localhost', port: int = 6379, password='',username='default', db=0,
            socket_timeout: int | float = 0.1, retry_on_timeout: bool = True, socket_keepalive: bool = True
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
                retry_on_timeout=retry_on_timeout,
                socket_keepalive=socket_keepalive
            )
        )
        self.curr_dir = os_path.dirname(__file__)
        self.lua_scripts_sha: dict = {}  # saving SHA1 hash of Lua scripts
        self.user_lua_scripts_buffer: dict = {}  # structure for storing SHA user Lua scripts
        self.data_type_converter = TypeConverter().converter

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """ Unbinds the context from the connection reference """
        self.redis.close()
        self.redis.connection_pool = None

    def __del__(self):
        self.redis.close()

    def redis_py(self) -> Redis:
        """
        Returns the original library object that the current library is built on if you need to perform an action
        that is not available within the current library.
        :return: redis-py library object
        """
        return self.redis

    def r_ping(self) -> bool:
        try:
            return self.redis.ping()
        except (rConnectionError, rTimeoutError):
            return False

    def get_redis_info(self) -> dict:
        """
        Some of the most popular keys in the output dictionary are:

        used_memory_vm_eval (For Redis >= 7.0):
        Number of bytes used by the script VM engines for EVAL framework (not part of used_memory)

        number_of_cached_scripts (For Redis >= 7.0):
        The number of EVAL scripts cached by the server

        uptime_in_seconds, uptime_in_days, redis_version, gcc_version, arch_bits, os, etc.
        """
        return self.redis.info()

    def get_key_memory_usage(self, key: str):
        """
        The MEMORY USAGE command reports the number of bytes that a key and its value require to be stored in RAM.
        The reported usage is the total of memory allocations for data and administrative
        overheads that a key and its value require.
        SAMPLES option is set to 0.
        :param key:
        :return: [integer] the memory usage in bytes
        """
        return self.redis.memory_usage(key, samples=0) or 0

    def get_count_of_keys(self) -> int:
        """ Returns the number of keys in the current database """
        return self.redis.dbsize()

    def flush_lua_scripts(self):
        self.lua_scripts_sha: dict = {}
        self.redis.script_flush()

    def keys_is_exists(self, keys: str | list[str] | tuple[str] | set[str] | frozenset[str]) -> int:
        if isinstance(keys, str) and keys:
            keys = [keys]
        return self.redis.exists(*keys) if keys else None

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
        ttl = self.redis.ttl(key) if in_seconds else self.redis.pttl(key)
        return ttl if ttl not in (-1, -2) else (0 if ttl == -1 else None)

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
            value: bool | int | float | str | list | tuple | set | frozenset,
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
        :param time_ms: key lifetime in milliseconds (0 equal None).
        :param time_s: key lifetime in seconds (0 equal None).
        :param if_exist: set value only if such key already exists.
        :param if_not_exist: set value only if such key does not exist yet.
        :param keep_ttl: retain the time to live associated with the key.
        :return: None
        """
        if (not key or (not value and value not in (False, 0))
                or not isinstance(value, (bool, int, float, str, list, tuple, set, frozenset))):
            # Writing empty objects is not supported
            return None

        if time_s or time_ms:
            time_s, time_ms = None, PyRedis.__compare_and_select_sec_ms(time_s, time_ms)

        res = None

        if isinstance(key, dict):
            pass

        elif isinstance(value, (bool, int, float, str)):
            get_old_value: int = int(get_old_value)
            time_ms: int = time_ms or 0
            if_exist: int = int(if_exist)
            if_not_exist: int = int(if_not_exist)
            keep_ttl: int = int(keep_ttl)
            value: str = str(value)
            res = self.__register_lua_scripts(
                'set_not_array_helper', 1, key, get_old_value, time_ms, if_exist, if_not_exist, keep_ttl, value
            )

        elif isinstance(value, (list, tuple, set, frozenset)):
            value: list | tuple | set | frozenset = type(value)(str(element) for element in value)
            time_ms: int = time_ms or 0
            if_exist: int = int(if_exist)
            if_not_exist: int = int(if_not_exist)
            get_old_value: int = int(get_old_value)
            keep_ttl: int = int(keep_ttl)
            res = self.__register_lua_scripts(
                'set_arrays_helper', 1, key,
                get_old_value, time_ms, if_exist, if_not_exist, keep_ttl,
                'rpush' if isinstance(value, (list, tuple)) else 'sadd', int(len(value) < 7850), *value
            )

        return self.__convert_to_type(res, convert_to_type_for_get) if res and convert_to_type_for_get else res

    def append_value_to_array(
            self,
            key: str,
            value: bool | int | float | str,
            index: int = -1,
            type_if_not_exists: str | None = None,
            get_old_value: bool = False,
            convert_to_type: str | None = None
    ) -> list | set | None:
        """
        Adding a new value to a list or set.

        Writing to the middle of a list of length ~500_000 about 0.045s.
        :param key:
        :param value: Remember that Redis does not support nested structures,
            so arrays cannot be values inside other arrays.
        :param index: (>= -1) At what position this element should be added. 0 - to the beginning, -1 - to the end,
            otherwise a specific position within the list (For sets index is ignored).
            If the position is greater than the length of the list,
            the element will be added to the end (equivalent to parameter -1).
        :param type_if_not_exists: If such a key does not exist, then a list or set value will be created,
            if otherwise specified, then the None parameter is assigned,
            which says that if such a key does not exist, it will not be created.
        :param get_old_value: Return the previous value of the key
        :param convert_to_type: bool/int/float (by default all output data is of type str after decode() function);
            For float -> int: rounds down to integer part number (drops fractional part)
        :return: None if such value did not exist before or get_old_value = False
        """
        if not key or (not value and value not in (False, 0)) or not isinstance(value, (bool,  int, float, str)):
            return None
        value: str = str(value)
        type_if_not_exists: str = 'null' if type_if_not_exists not in ('list', 'set') else type_if_not_exists
        get_old_value: int = int(get_old_value)
        res = self.__register_lua_scripts(
            'append_value_to_array', 1, key, index, type_if_not_exists, get_old_value, value
        )
        res = (set(res[0]) if res[1] == 'set' else res[0]) if res else None
        return self.__convert_to_type(res, convert_to_type) if (convert_to_type and res is not None) else res

    def r_get(self, key: str, default_value=None, convert_to_type: str | None = None):
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

        res = self.__register_lua_scripts('get_helper', 1, key)
        res = (set(res[0]) if res[1] == 'set' else res[0]) if res else default_value
        return self.__convert_to_type(res, convert_to_type) if (convert_to_type and res is not None) else res

    def r_len(self, key: str) -> int | None:
        """
        Получить длину списка/множества в Redis
        :param key:
        :return: None - такого ключа нет; 0 - такой ключ есть, но в нем записан не массив;
        """
        res = self.__register_lua_scripts('r_len', 1, key)
        return int(res) if res is not None else None

    def r_pop(
            self,
            key: str,
            count: int = 1,
            reverse: bool = False,
            convert_to_type: str = None
    ) -> tuple:
        """
        Removes and returns an element of the list stored by key.
        It`s important to remember that a "random" element is taken from the set,
        since the set does not preserve the order in which the elements are stored.
        :param key:
        :param count: By default, it returns 1 item, you can specify the number to extract and return
        :param reverse: By default, items in lists are taken from the beginning. Specify True to get items from the end.
        :param convert_to_type:
        :return: tuple
        """
        res = self.__register_lua_scripts('r_pop', 1, key, count, int(reverse))  # return list
        return tuple(self.__convert_to_type(res, convert_to_type) if convert_to_type else res) if res else ()

    def array_is_empty(self, key: str):
        pass

    def r_sort(
            self, key: str, desc: bool = True, return_before: bool = False, return_after: bool = False
    ) -> None | tuple:
        """
        Сортирует список
        :param key:
        :param desc: True = DESC; False = ASC
        :param return_before:
        :param return_after:
        :return: None
        """
        pass

    def get_element(self, key: str):
        pass

    def get_range(self, key: str, start: int, stop: int):
        """

        :param key:
        :param start: [включительно]
        :param stop: [включительно]
        :return:
        """
        pass

    def del_element(self, key: str):
        pass

    def del_range(self, key: str, start: int, stop: int, return_before: bool = False, return_after: bool = False):
        """

        :param key:
        :param start: [включительно]
        :param stop: [включительно]
        :param return_before:
        :param return_after:
        :return:
        """
        pass

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
        return self.__helper_delete_or_unlink(
            False, key=key, returning=returning, convert_to_type_for_return=convert_to_type_for_return
        )

    def r_unlink(self, key: str, returning: bool = False, convert_to_type_for_return: str = None):
        """
        Unlink a key.
        r_unlink is very similar to r_delete: it removes the specified keys.
        The command just unlinks the keys from the keyspace. The actual removal will happen later asynchronously.
        :param key:
        :param returning: return the value the key had before deletion
        :param convert_to_type_for_return: what type the return value should be converted to (if returning=True)
        :return: value or None
        """
        return self.__helper_delete_or_unlink(
            True, key=key, returning=returning, convert_to_type_for_return=convert_to_type_for_return
        )

    def __helper_delete_or_unlink(
            self,
            command: bool,
            key: str,
            returning: bool = False,
            convert_to_type_for_return: str = None
    ):
        """
        :param command: False - delete / True - unlink
        :param key:
        :param returning:
        :param convert_to_type_for_return:
        :return:
        """
        if not key:
            return

        res = self.__register_lua_scripts(
            'delete_or_unlink_with_returning', 1, key, int(returning), 'unlink' if command else 'delete'
        )
        res = (set(res[0]) if res[1] == 'set' else res[0]) if res else None

        if returning and res:
            return self.__convert_to_type(res, convert_to_type_for_return) if convert_to_type_for_return else res
        return

    def rename_key(self, key: str, new_key: str, get_rename_status: bool = None):
        """
        Change key name
        :param key: current key name
        :param new_key: new key name
        :param get_rename_status: get True if the key exists and has been renamed, False if there is no such key
        :return:
        """
        rename_status = self.__register_lua_scripts('rename_key', 2, key, new_key)
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
        Uses the same function as regular r_delete/r_unlink,
        but has a wrapper that allows you to get information about deleted keys.
        :param keys:
        :param return_exists: return keys that existed and were deleted
        :param return_non_exists: return keys that were not found
        :param get_dict_key_value_exists: get dictionary of remote keys with values
        :param convert_to_type_dict_key: is type conversion needed for the returned dictionary
        :return: ((return_exists), (return_non_exists), {get_dict_key_value_exists})
        """
        return self.__helper_mass_delete_or_unlink(
            False,
            keys=keys,
            return_exists=return_exists,
            return_non_exists=return_non_exists,
            get_dict_key_value_exists=get_dict_key_value_exists,
            convert_to_type_dict_key=convert_to_type_dict_key
        )

    def r_mass_unlink(
            self,
            keys: list | tuple | set | frozenset,
            return_exists: bool = False,
            return_non_exists: bool = False,
            get_dict_key_value_exists: bool = False,
            convert_to_type_dict_key: str = None
    ) -> tuple[tuple, tuple, dict]:
        """
        Mass unlink keys from a given iterable.
        Uses the same function as regular r_delete/r_unlink,
        but has a wrapper that allows you to get information about deleted keys.
        :param keys:
        :param return_exists: return keys that existed and were deleted
        :param return_non_exists: return keys that were not found
        :param get_dict_key_value_exists: get dictionary of remote keys with values
        :param convert_to_type_dict_key: is type conversion needed for the returned dictionary
        :return: ((return_exists), (return_non_exists), {get_dict_key_value_exists})
        """
        return self.__helper_mass_delete_or_unlink(
            True,
            keys=keys,
            return_exists=return_exists,
            return_non_exists=return_non_exists,
            get_dict_key_value_exists=get_dict_key_value_exists,
            convert_to_type_dict_key=convert_to_type_dict_key
        )

    def __helper_mass_delete_or_unlink(
            self,
            command: bool,
            keys: list | tuple | set | frozenset,
            return_exists: bool = False,
            return_non_exists: bool = False,
            get_dict_key_value_exists: bool = False,
            convert_to_type_dict_key: str = None
    ) -> tuple[tuple, tuple, dict]:
        """
        :param command: False - delete / True - unlink
        :param keys:
        :param return_exists:
        :param return_non_exists:
        :param get_dict_key_value_exists:
        :param convert_to_type_dict_key:
        :return:
        """
        if not keys:
            return (), (), {}

        keys: tuple = PyRedis.__remove_duplicates(keys)  # remove duplicates

        # all parameters = None | False
        if return_exists is return_non_exists is get_dict_key_value_exists is False:
            self.redis.unlink(*keys) if command else self.redis.delete(*keys)  # pylint: disable=expression-not-assigned
            return (), (), {}

        # if one of the parameters is specified, then we collect a dictionary of existing key-values
        exists_key_value: dict = json_loads(
            self.__register_lua_scripts('r_mass_delete_or_unlink', len(keys), *keys, 'unlink' if command else 'delete')
        )
        exists_keys: tuple = tuple(sorted(exists_key_value.keys()))
        non_exists_keys: tuple = tuple(sorted(set(keys) - set(exists_keys)))

        # convert_to_type_dict_key
        exists_key_value = {
            key: self.__convert_to_type(value, convert_to_type_dict_key)
            for key, value in exists_key_value.items()
        } if convert_to_type_dict_key else exists_key_value

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
        return {keys[i]: self.__convert_to_type(value, convert_to_type_dict_key)
                if convert_to_type_dict_key else value for i, value in enumerate(values) if value is not None}

    def r_remove_all_keys_local(self, get_count_keys: bool = False) -> int | None:
        """
        Delete all keys in current database
        :param get_count_keys: need to return the number of deleted keys (True -> return integer, False -> return None)
        :return: count keys or None
        """
        count_keys = self.__register_lua_scripts('remove_all_keys_local', 0, int(get_count_keys))
        return int(count_keys) if count_keys else None

    def r_remove_all_keys(self, get_count_keys: bool = False) -> int | None:
        """
        Delete all keys in all databases on the current host
        :param get_count_keys: need to return the number of deleted keys (True -> return integer, False -> return None)
        :return: count keys or None

        Why isn't this function written in Lua?
        Redis requires that all actions remain within the same database during a single script execution session.
        The prohibition on SELECT in Lua is due to the fact that in Redis,
        a single Lua script can only change the data of the current database to which the connection is connected.
        """
        total_keys = 0
        if get_count_keys:
            databases = int(self.redis.config_get('databases')['databases'])  # Get the number of databases
            for db in range(databases):
                self.redis.execute_command("SELECT", db)
                total_keys += self.redis.dbsize()

        self.redis.flushall()

        return int(total_keys) if get_count_keys else None

    def run_lua_script(self, *args, lua_script: str | None = None, sha: str | None = None, read_only: bool = False):
        """
        Execute the Lua script, specifying the numkeys the script
        will touch and the key names and argument values in keys_and_args.

        :param lua_script: Lua script as a string
        :param sha: SHA or result load_lua_script() function
        :param read_only: True if the EVAL command should be executed, read-only
        :param args: The first arguments in *args you must pass are the number of keys,
            and then the keys themselves in the required order. Then come the additional arguments.
        :return: Returns the result of the script
        """
        if not (lua_script or sha):
            return
        if sha or (sha := self.user_lua_scripts_buffer.get(lua_script)):
            return self.redis.evalsha_ro(sha, *args) if read_only else self.redis.evalsha(sha, *args)
        return self.redis.eval_ro(lua_script, *args) if read_only else self.redis.eval(lua_script, *args)

    def load_lua_script(self, lua_script: str, use_buffer: bool = True) -> str:
        """
        Load a Lua script into the script cache_data
        :param lua_script:
        :param use_buffer: You can use the built-in buffer to store the SHA of your scripts,
            and if it is found when executing the script,
            its SHA will already be inside the structure and will not be calculated again.
        :return: SHA
        """
        res = self.user_lua_scripts_buffer.get(lua_script) or self.redis.script_load(lua_script)
        if use_buffer and lua_script not in self.user_lua_scripts_buffer:
            self.user_lua_scripts_buffer[lua_script] = res
        return res

    def __register_lua_scripts(self, script_name: str, *args):
        if script_name not in self.lua_scripts_sha:
            lua_script = self.__load_lua_script_from_file(script_name)
            self.lua_scripts_sha[script_name] = self.redis.script_load(lua_script)
        return self.redis.evalsha(self.lua_scripts_sha[script_name], *args)

    def __load_lua_script_from_file(self, filename: str) -> str:
        """ Load Lua script from a file """
        with open(os_path.join(self.curr_dir, f'lua_scripts/{filename}.lua'), 'r', encoding='utf-8') as lua_file:
            return lua_file.read()

    def __convert_to_type(
            self,
            value: str | list[str] | set[str],
            _type: str
    ) -> str | bool | int | float | list | set:
        return self.data_type_converter(value, _type)

    @staticmethod
    def __compare_and_select_sec_ms(time_s: int | None, time_ms: int | None) -> int | None:
        """
        If both seconds and milliseconds are specified,
        the time is converted to milliseconds and the smallest one is selected
        """
        if not (time_s or time_ms):
            return None

        if not time_s or not time_ms:
            return time_s * 1_000 if time_s else time_ms

        return min(time_s * 1_000, time_ms)

    @staticmethod
    def __remove_duplicates(iterable_var: list | tuple | set | frozenset) -> tuple:
        if isinstance(iterable_var, (set, frozenset)):
            return tuple(iterable_var)
        return tuple(set(iterable_var))
