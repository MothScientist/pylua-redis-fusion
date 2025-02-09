"""
Ttl tests that need to be run in 1 thread
"""
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
	Tests to check the service life of keys, the sleep() function will be used
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

	def test_set_get_ttl_int_001(self):
		key: str = 'set_get_int_001'
		value: int = TtlTests.get_random_integer()
		self.assertIsNone(TtlTests.r.r_set(key, value, time_s=3))
		res_1: str = TtlTests.r.r_get(key, convert_to_type='int')
		self.assertEqual(res_1, value)
		sleep(1)
		res_2: str = TtlTests.r.r_get(key, convert_to_type='integer')
		self.assertEqual(res_2, value)
		sleep(2)
		res_3: None = TtlTests.r.r_get(key)
		self.assertIsNone(res_3, f'res = {res_2}')

	def test_set_get_ttl_float_001(self):
		key: str = 'set_get_float_001'
		value: float = random()
		self.assertIsNone(TtlTests.r.r_set(key, value, time_s=3))
		res_1: str = TtlTests.r.r_get(key, convert_to_type='numeric')
		self.assertEqual(res_1, value)
		sleep(1)
		res_2: str = TtlTests.r.r_get(key, convert_to_type='double')
		self.assertEqual(res_2, value)
		sleep(2)
		res_3: None = TtlTests.r.r_get(key)
		self.assertIsNone(res_3, f'res = {res_2}')


if __name__ == '__main__':
	from redis import Redis, ConnectionPool
	_redis = Redis(connection_pool=ConnectionPool(
		host=redis_host,port=redis_port,db=0,password=redis_psw, username=redis_username
	))
	_redis.flushall()  # clear the database before tests
