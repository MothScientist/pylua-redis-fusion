# test_1: 0.00239 sec.;
# test_1: 0.00053 sec.; (cache)
# test_1 (original): 0.00087 sec.;
#
#
# test_2: 0.00034 sec.;
# test_2: 0.00032 sec.; (cache)
# test_2 (original): 0.00030 sec.;
#
#
# test_3: 0.00092 sec.;
# test_3: 0.00060 sec.; (cache)
# test_3 (original): 0.00049 sec.;
#
#
# test_4: 0.00086 sec.;
# test_4: 0.00047 sec.; (cache)
# test_4 (original): 0.00033 sec.;
#
#
# test_5: 0.00014 sec.;
# test_5: 0.00013 sec.; (cache)
# test_5 (original): 0.00010 sec.;
#
#
# test_6: 0.44811 sec.;
# test_6: 0.31189 sec.; (cache)
# test_6 (original): 0.38190 sec.;
#
#
# test_7: 1.78373 sec.;
# test_7: 1.40646 sec.; (cache)
# test_7 (original): 0.70364 sec.;


from dotenv import load_dotenv
from os import getenv
from time import perf_counter

from redis import (
    Redis,
    ConnectionPool
)

from pyluaredis.client import PyRedis

load_dotenv('../pyluaredis/redis.env')  # Load environment variables from redis.env file
REDIS_PWS: str = getenv('REDIS_PSW')
REDIS_HOST: str = getenv('REDIS_HOST') or 'localhost'
REDIS_PORT: int = int(getenv('REDIS_PORT') or 6379)
REDIS_USERNAME: str = getenv('REDIS_USERNAME') or 'default'

original_r = Redis(connection_pool=ConnectionPool(
    host=REDIS_HOST,
    port=REDIS_PORT,
    password=REDIS_PWS,
    username=REDIS_USERNAME,
    db=0,
    socket_timeout=.1,
    encoding='utf-8',
    decode_responses=True,
    retry_on_timeout=True,
    socket_keepalive=True,
))

r = PyRedis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    password=REDIS_PWS,
    username=REDIS_USERNAME,
    db=0,
    socket_timeout=.1,
)


def ch_1(cache: bool = False):
    """ Write, read and delete the key """
    key: str = 'test_1'
    start_time = perf_counter()
    r.r_set(key, key)
    _ = r.r_get(key)
    r.r_unlink(key)
    end_time = perf_counter()
    print(f'test_1: {(end_time - start_time):.5f} sec.;{" (cache)" if cache else ""}')


def ch_1_original():
    key: str = 'test_1_original'
    start_time = perf_counter()
    original_r.set(key, key)
    _ = original_r.get(key)
    original_r.unlink(key)
    end_time = perf_counter()
    print(f'test_1 (original): {(end_time - start_time):.5f} sec.;')


def ch_2(cache: bool = False):
    """ Write and rewrite the key """
    key: str = 'test_2'
    value: int = 1_000
    start_time = perf_counter()
    r.r_set(key, key)
    r.r_set(key, value)
    end_time = perf_counter()
    print(f'test_2: {(end_time - start_time):.5f} sec.;{" (cache)" if cache else ""}')


def ch_2_original():
    key: str = 'test_2_original'
    value: int = 1_000
    start_time = perf_counter()
    original_r.set(key, key)
    original_r.set(key, value)
    end_time = perf_counter()
    print(f'test_2 (original): {(end_time - start_time):.5f} sec.;')


def ch_3(cache: bool = False):
    """ Write an array of numbers and return them in the same format """
    key: str = 'test_3'
    value: list[int] = [i for i in range(100)]
    start_time = perf_counter()
    r.r_set(key, value)
    _ = r.r_get(key, convert_to_type='int')
    end_time = perf_counter()
    print(f'test_3: {(end_time - start_time):.5f} sec.;{" (cache)" if cache else ""}')


def ch_3_original():
    key: str = 'test_3_original'
    value: list[int] = [i for i in range(100)]
    start_time = perf_counter()
    original_r.rpush(key, *value)
    _ = original_r.lrange(key, 0, -1)
    _ = list(map(int, _))
    end_time = perf_counter()
    print(f'test_3 (original): {(end_time - start_time):.5f} sec.;')


def ch_4(cache: bool = False):
    """ Write an array of numbers, add a new number and get the result in the same format """
    key: str = 'test_4'
    value: list[int] = [i for i in range(100)]
    start_time = perf_counter()
    r.r_set(key, value)

    # добавляем значение
    r.append_value_to_array(key, 999, 0)

    _ = r.r_get(key, convert_to_type='int')
    end_time = perf_counter()
    print(f'test_4: {(end_time - start_time):.5f} sec.;{" (cache)" if cache else ""}')


def ch_4_original():
    key: str = 'test_4_original'
    value: list[int] = [i for i in range(100)]
    start_time = perf_counter()
    original_r.rpush(key, *value)

    # добавляем значение
    original_r.lpush(key, 999)

    _ = original_r.lrange(key, 0, -1)
    _ = list(map(int, _))
    end_time = perf_counter()
    print(f'test_4 (original): {(end_time - start_time):.5f} sec.;')


def ch_5(cache: bool = False):
    """ Write down the key, get the value and write down the new one """
    key: str = 'test_5'
    value_1: int = 1
    value_2: int = 2
    start_time = perf_counter()
    r.r_set(key, value_1)
    _ = r.r_set(key, value_2, get_old_value=True)
    end_time = perf_counter()
    print(f'test_5: {(end_time - start_time):.5f} sec.;{" (cache)" if cache else ""}')


def ch_5_original():
    key: str = 'test_5_original'
    value_1: int = 1
    value_2: int = 2
    start_time = perf_counter()
    original_r.set(key, value_1)
    _ = original_r.set(key, value_2, get=True)
    end_time = perf_counter()
    print(f'test_5 (original): {(end_time - start_time):.5f} sec.;')


def ch_6(cache=False):
    """ Write a large list and add an element to its middle """
    key: str = 'test_6'
    value: list[int] = [1 for _ in range(100_000)]
    start_time = perf_counter()
    r.r_set(key, value)
    r.append_value_to_array(key, 999, 50_000)
    _ = r.r_get(key, convert_to_type='int')
    end_time = perf_counter()
    print(f'test_6: {(end_time - start_time):.5f} sec.;{" (cache)" if cache else ""}')


def ch_6_original():
    key: str = 'test_6_original'
    value: list[int] = [1 for _ in range(100_000)]
    start_time = perf_counter()
    original_r.rpush(key, *value)

    new = original_r.lrange(key, 0, -1)
    original_r.delete(key)
    new = list(map(int, new))
    new.insert(50_000, 999)
    original_r.rpush(key, *new)

    _ = original_r.lrange(key, 0, -1)
    _ = list(map(int, _))
    end_time = perf_counter()
    print(f'test_6 (original): {(end_time - start_time):.5f} sec.;')


def ch_7(cache: bool = False):
    """ Write and delete a very large array """
    key: str = 'test_7'
    value: list[int] = [i for i in range(1_000_000)]
    start_time = perf_counter()
    r.r_set(key, value)
    r.r_delete(key)
    end_time = perf_counter()
    print(f'test_7: {(end_time - start_time):.5f} sec.;{" (cache)" if cache else ""}')


def ch_7_original():
    key: str = 'test_7_original'
    value: list[int] = [i for i in range(1_000_000)]
    start_time = perf_counter()
    original_r.rpush(key, *value)
    original_r.delete(key)
    end_time = perf_counter()
    print(f'test_7 (original): {(end_time - start_time):.5f} sec.;')


if __name__ == '__main__':
    original_r.flushall()
    for i in range(1, 8):
        ch, orig = globals()[f'ch_{i}'], globals()[f'ch_{i}_original']
        ch(), ch(cache=True), orig(), print('\n')
