import unittest
from dotenv import load_dotenv
from os import getenv
from random import randint, choice, random
from string import ascii_letters, digits
from sys import path as sys_path
from time import sleep

sys_path.append('../')
from src.client import PyRedis

load_dotenv('../src/redis.env')  # Load environment variables from redis.env file
redis_psw: str = getenv('REDIS_PSW')
redis_db: int = int(getenv('REDIS_DB') or 0)
redis_host: str = getenv('REDIS_HOST') or 'localhost'
redis_port: int = int(getenv('REDIS_PORT') or 6379)
redis_username: str = getenv('REDIS_USERNAME') or 'default'


class TtlTests(unittest.TestCase):
	"""
	Tests to check the service life of keys, the sleep() function will be used,
	so the tests are run in parallel on all processor cores
	"""
	# def setUp(self):
	# 	self.maxDiff = None

	r = PyRedis(
		host=redis_host,
		port=redis_port,
		password=redis_psw,
		username=redis_username,
		db=redis_db
	)

	@staticmethod
	def get_random_integer():
		return randint(0, 100)

	@staticmethod
	def get_random_string(length: int = randint(5, 10)):
		return ''.join(choice(ascii_letters + digits) for _ in range(length))

	def test_ping(self):
		self.assertTrue(TtlTests.r.r_ping())

	def test_set_get_ttl_str_001(self):
		key: str = 'set_get_str_001'
		value: str = TtlTests.get_random_string()
		self.assertIsNone(TtlTests.r.r_set(key, value, time_s=1))
		res_1: str = TtlTests.r.r_get(key)
		self.assertEqual(res_1, value)
		sleep(1)
		res_2: None = TtlTests.r.r_get(key)
		self.assertIsNone(res_2, f'res = {res_2}')

	def test_set_get_ttl_str_002(self):
		key: str = 'set_get_str_002'
		value: str = TtlTests.get_random_string()
		self.assertIsNone(TtlTests.r.r_set(key, value, time_s=5))
		res_1: str = TtlTests.r.r_get(key)
		self.assertEqual(res_1, value)
		sleep(5)
		res_2: None = TtlTests.r.r_get(key)
		self.assertIsNone(res_2, f'res = {res_2}')

	def test_set_get_ttl_str_003(self):
		key: str = 'set_get_str_003'
		value: str = TtlTests.get_random_string()
		self.assertIsNone(TtlTests.r.r_set(key, value, time_s=1, time_ms=5000))
		res_1: str = TtlTests.r.r_get(key)
		self.assertEqual(res_1, value)
		sleep(1)
		res_2: None = TtlTests.r.r_get(key)
		self.assertIsNone(res_2, f'res = {res_2}')

	def test_set_get_ttl_str_004(self):
		key: str = 'set_get_str_004'
		value: str = TtlTests.get_random_string()
		self.assertIsNone(TtlTests.r.r_set(key, value, time_s=10, time_ms=5000))
		res_1: str = TtlTests.r.r_get(key)
		self.assertEqual(res_1, value)
		sleep(5)
		res_2: None = TtlTests.r.r_get(key)
		self.assertIsNone(res_2, f'res = {res_2}')

	def test_set_get_ttl_str_005(self):
		key: str = 'set_get_str_005'
		value: str = TtlTests.get_random_string()
		self.assertIsNone(TtlTests.r.r_set(key, value, time_s=0.1, time_ms=100))
		res_1 = TtlTests.r.r_get(key)
		self.assertEqual(res_1, value)
		sleep(1)
		res_2: None = TtlTests.r.r_get(key)
		self.assertIsNone(res_2, f'res = {res_2}')

	def test_set_get_ttl_int_001(self):
		key: str = 'set_get_int_001'
		value: int = TtlTests.get_random_integer()
		self.assertIsNone(TtlTests.r.r_set(key, value, time_s=1))
		res_1: str = TtlTests.r.r_get(key)
		self.assertEqual(res_1, str(value))
		sleep(1)
		res_2: None = TtlTests.r.r_get(key)
		self.assertIsNone(res_2, f'res = {res_2}')

	def test_set_get_ttl_float_001(self):
		key: str = 'set_get_float_001'
		value: float = random()
		self.assertIsNone(TtlTests.r.r_set(key, value, time_s=2))
		res_1: str = TtlTests.r.r_get(key)
		self.assertEqual(res_1, str(value))
		sleep(2)
		res_2: None = TtlTests.r.r_get(key)
		self.assertIsNone(res_2, f'res = {res_2}')


if __name__ == '__main__':
	from redis import Redis, ConnectionPool
	_redis = Redis(connection_pool=ConnectionPool(
		host=redis_host,port=redis_port,db=0,password=redis_psw, username=redis_username
	))
	_redis.flushall()  # clear the database before tests
