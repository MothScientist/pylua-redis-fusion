from dotenv import load_dotenv
from os import getenv
from functools import wraps

from src.client import PyRedis

load_dotenv('src/redis.env')  # Load environment variables from redis.env file
redis_psw: str = getenv('REDIS_PSW')
redis_db: int = int(getenv('REDIS_DB'))
redis_host: str = getenv('REDIS_HOST')
redis_port: int = int(getenv('REDIS_PORT'))


def redis_connection() -> PyRedis:
    return PyRedis(redis_host, redis_port, redis_psw, db=redis_db, socket_timeout=.001)


def set_cache(key: str, value):
    redis_connection().r_set(key, value)


def get_cache(key: str, convert_to_type=None):
    return redis_connection().r_get(key, convert_to_type=convert_to_type)


def main():
    set_cache('1', 'cache')
    set_cache('2', (1, 2, 3, 4, 5))
    print(f"--- Simple set/get: {get_cache('1')}")
    data_1: tuple = get_cache('2', convert_to_type='int')
    print(f"--- tuple[int] set/get: {data_1} / type(tuple[0]) = {type(data_1[0])}")
    set_cache('3', True)
    data_2: bool = get_cache('3', convert_to_type='bool')
    print(f"--- Set/get bool type: {data_2} / type = {type(data_2)}")

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
def easy_get_cache(r, key, convert_to_type=None):
    return r.r_get(key, convert_to_type=convert_to_type)

#######################################################################################################################


if __name__ == '__main__':
    main()
    print('\n')
    print('Example with decorator @redis (set + get):')
    easy_set_cache('easy_1', 'Decorator')
    easy_set_cache('easy_2', 1.5)
    print(f'Get value: {easy_get_cache('easy_1')}')
    easy_2 = easy_get_cache('easy_2', convert_to_type="float")
    print(f'Get value: {easy_2} / type = {type(easy_2)}')
