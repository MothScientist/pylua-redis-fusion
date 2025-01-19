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


def set_cache(key: str, value: int):
    redis_connection().r_set(key, value)


def get_cache(key: str):
    return redis_connection().r_get(key).decode('utf-8')


def main():
    set_cache('12345', 123)
    return get_cache('12345')

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
def easy_get_cache(r, key):
    return r.r_get(key).decode('utf-8')


if __name__ == '__main__':
    print(f'Simple example (set + get): {main()}\n\n')

    print('Example with decorator @redis (set + get):')
    easy_set_cache('1', 2)
    print(f'Get value: {easy_get_cache('1')}')
