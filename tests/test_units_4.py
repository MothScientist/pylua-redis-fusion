"""
Multiple databases tests
"""
import unittest
from redis import Redis, ConnectionPool
from dotenv import load_dotenv
from os import getenv
from random import randint, choice, random
from string import ascii_letters, digits
from sys import path as sys_path

sys_path.append('../')
from src.client import PyRedis

load_dotenv('../src/redis.env')  # Load environment variables from redis.env file
redis_psw: str = getenv('REDIS_PSW')
redis_host: str = getenv('REDIS_HOST') or 'localhost'
redis_port: int = int(getenv('REDIS_PORT') or 6379)
redis_username: str = getenv('REDIS_USERNAME') or 'default'

original_redis_db0 = Redis(connection_pool=ConnectionPool(
		host=redis_host, port=redis_port, db=0, password=redis_psw, username=redis_username
	))


class MultipleDatabasesTests(unittest.TestCase):
	# def setUp(self):
	# 	self.maxDiff = None

	r0 = PyRedis(
		host=redis_host,
		port=redis_port,
		password=redis_psw,
		username=redis_username,
		db=0,
		socket_timeout=.1
	)

	r1 = PyRedis(
		host=redis_host,
		port=redis_port,
		password=redis_psw,
		username=redis_username,
		db=1,
		socket_timeout=.1
	)

	@staticmethod
	def get_random_integer():
		return randint(0, 1_000_000)

	@staticmethod
	def get_random_string(length: int = randint(10, 20)):
		return ''.join(choice(ascii_letters + digits) for _ in range(length))

	def test_ping_001(self):
		""" Service db=0 is available """
		self.assertTrue(MultipleDatabasesTests.r0.r_ping())

	def test_ping_002(self):
		""" Service db=1 is available """
		self.assertTrue(MultipleDatabasesTests.r1.r_ping())

	def test_ping_003(self):
		wrong_r = PyRedis(host='unknown')
		self.assertFalse(wrong_r.r_ping())

	def test_r_remove_all_keys_local_001(self):
		pass

	def test_r_remove_all_keys_001(self):
		original_redis_db0.flushall()

		# for first database
		key_0: str = MultipleDatabasesTests.get_random_string(length=3)
		MultipleDatabasesTests.r0.r_set(key_0, key_0)
		res_0: str = MultipleDatabasesTests.r0.r_get(key_0)
		self.assertEqual(res_0, key_0)

		# for second database
		key_1: str = MultipleDatabasesTests.get_random_string(length=5)
		MultipleDatabasesTests.r1.r_set(key_1, key_1)
		res_1: str = MultipleDatabasesTests.r1.r_get(key_1)
		self.assertEqual(res_1, key_1)

		count_keys: int = MultipleDatabasesTests.r0.r_remove_all_keys(get_count_keys=True)
		res_0: None = MultipleDatabasesTests.r0.r_get(key_0)
		res_1: None = MultipleDatabasesTests.r1.r_get(key_1)
		self.assertEqual(res_0, None)
		self.assertEqual(res_1, None)
		self.assertEqual(count_keys, 2)

	def test_r_remove_all_keys_002(self):
		original_redis_db0.flushall()

		# for first database
		key_0: str = MultipleDatabasesTests.get_random_string(length=3)
		MultipleDatabasesTests.r0.r_set(key_0, key_0)
		res_0: str = MultipleDatabasesTests.r0.r_get(key_0)
		self.assertEqual(res_0, key_0)

		# for second database
		key_1: str = MultipleDatabasesTests.get_random_string(length=5)
		MultipleDatabasesTests.r1.r_set(key_1, key_1)
		res_1: str = MultipleDatabasesTests.r1.r_get(key_1)
		self.assertEqual(res_1, key_1)

		count_keys = MultipleDatabasesTests.r0.r_remove_all_keys(get_count_keys=True)
		res_0: None = MultipleDatabasesTests.r0.r_get(key_0)
		res_1: None = MultipleDatabasesTests.r1.r_get(key_1)
		self.assertEqual(res_0, None)
		self.assertEqual(res_1, None)
		self.assertEqual(count_keys, 2)


if __name__ == '__main__':
	original_redis_db0.flushall()  # clear the databases before tests

	unittest.main()
