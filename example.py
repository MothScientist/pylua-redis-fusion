"""
Run this file to check the correctness of your .env file data and to see the minimal library functions
"""
from dotenv import load_dotenv
from os import getenv
from functools import wraps

from pyluaredis.client import PyRedis

load_dotenv('pyluaredis/redis.env')  # Load environment variables from redis.env file
redis_psw: str = getenv('REDIS_PSW')
redis_db: int = int(getenv('REDIS_DB'))
redis_host: str = getenv('REDIS_HOST')
redis_port: int = int(getenv('REDIS_PORT'))
redis_username: str = str(getenv('REDIS_USERNAME'))


def redis_connection() -> PyRedis:
    return PyRedis(host=redis_host, port=redis_port, password=redis_psw, db=redis_db, username=redis_username)


def set_cache(key: str, value):
    redis_connection().r_set(key, value)


def get_cache(key: str, convert_to_type=None):
    return redis_connection().r_get(key, convert_to_type=convert_to_type)


def decorator():
    easy_set_cache('1', 'Decorator')
    easy_set_cache('2', 1.5)
    print(f'\tGet value: {easy_get_cache('1')}')
    res = easy_get_cache('2', convert_to_type="float")
    print(f'\tGet value: {res} / type = {type(res)}')

    res: int = easy_delete_all_keys(get_count_keys=True)
    print(f'\tDelete {res} keys')
    res = easy_get_cache('1')
    print(f'\teasy_1 key = {res}')


def main():
    set_cache('1', 'cache')
    print(f"\tSimple set/get: {get_cache('1')}")
    set_cache('1', [1, 2, 3, 4, 5])
    res: tuple = get_cache('1', convert_to_type='int')
    print(f"\tList[int] set/get: {res} / type(res) = {type(res)} / type(res[0]) = {type(res[0])}")
    set_cache('1', True)
    res: bool = get_cache('1', convert_to_type='bool')
    print(f"\tSet/get bool type: {res} / type = {type(res)}")
    set_cache('1', {'ASCII', 'UTF-8', 'UTF-16'})
    res: set = get_cache('1')
    print(f"\tSet/get set type: {res} / type = {type(res)}")


def memory():
    r = redis_connection()
    r.flush_lua_scripts()  # clean up lua scripts sha before example
    set_cache('1', [1, 2, 3, 4, 5])
    set_cache('2', 1)
    set_cache('3', True)
    set_cache('4', {1, 2, 3, 4, 5, 5, 5})
    res: dict = r.get_redis_info()
    print(f"\tused_memory_vm_eval: {res.get('used_memory_vm_eval')} /"
          f" number_of_cached_scripts = {res.get('number_of_cached_scripts')}")
    r.flush_lua_scripts()
    print('\tflush_lua_scripts()')
    res = r.get_redis_info()
    print(f"\tused_memory_vm_eval: {res.get('used_memory_vm_eval')} /"
          f" number_of_cached_scripts = {res.get('number_of_cached_scripts')}")
    print('\n')
    print('\tLet\'s write a simple string into the key value:')
    set_cache('1', '1')
    res: int = r.get_key_memory_usage('1')
    print(f'\t\tget_key_memory_usage(key) = {res}')
    print('\tLet\'s write a list of 1000 elements into the key value:')
    set_cache('1', [i for i in range(0, 1_000)])
    res: int = r.get_key_memory_usage('1')
    print(f'\t\tget_key_memory_usage(key) = {res}')
    print('\tLet\'s delete the key:')
    r.r_delete('1')
    res: int = r.get_key_memory_usage('1')
    print(f'\t\tget_key_memory_usage(key) = {res}')


def context_manager():
    with redis_connection() as redis_conn:
        conn = redis_conn
        print(redis_conn.r_ping())

    try:
        conn.r_ping()
    except AttributeError:
        print('It is impossible to connect using the old variable!')


def type_converter():
    pass


########################################################################################################################
# Works with the help of a decorator
# P.S. the decorator is not included in the library, as I want each user to customize it for themselves


def redis(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # try/except + logs
        return func(redis_connection(), *args, **kwargs)
    return wrapper


@redis
def easy_set_cache(r, key, value):
    r.r_set(key, value)


@redis
def easy_get_cache(r, key, **kwargs):
    return r.r_get(key, **kwargs)


@redis
def easy_delete_all_keys(r, **kwargs):
    return r.r_remove_all_keys_local(**kwargs)

#######################################################################################################################


if __name__ == '__main__':
    easy_delete_all_keys()  # delete keys from database before example
    print('Example with decorator @redis (set + get):')
    decorator()
    print('\nMain:')
    main()
    print('\nMemory:')
    memory()
    print('\nContextManager:')
    context_manager()
    print('\nTypeConverter:')
    type_converter()
