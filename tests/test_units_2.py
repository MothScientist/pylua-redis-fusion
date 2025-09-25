"""
Multiple databases tests
"""
import unittest
from redis import Redis, ConnectionPool
from random import randint, choice
from string import ascii_letters, digits
from sys import path as sys_path

from connection_params import REDIS_PWS, REDIS_HOST, REDIS_PORT, REDIS_USERNAME
sys_path.append('../')
from pyluaredis.client import PyRedis

redis_db_2: int = 2  # redis_db: int = 2 - for quick search in IDE
redis_db_3: int = 3  # redis_db: int = 3


class MultipleDatabasesTests(unittest.TestCase):
	# def setUp(self):
	# 	self.maxDiff = None

	r2 = PyRedis(
		host=REDIS_HOST,
		port=REDIS_PORT,
		password=REDIS_PWS,
		username=REDIS_USERNAME,
		db=redis_db_2,
		socket_timeout=.1
	)

	r3 = PyRedis(
		host=REDIS_HOST,
		port=REDIS_PORT,
		password=REDIS_PWS,
		username=REDIS_USERNAME,
		db=redis_db_3,
		socket_timeout=.1
	)

	original_redis_db2 = Redis(connection_pool=ConnectionPool(
		host=REDIS_HOST, port=REDIS_PORT, db=2, password=REDIS_PWS, username=REDIS_USERNAME
	))

	original_redis_db3 = Redis(connection_pool=ConnectionPool(
		host=REDIS_HOST, port=REDIS_PORT, db=3, password=REDIS_PWS, username=REDIS_USERNAME
	))

	@classmethod
	def setUpClass(cls):
		# clear the database before tests
		MultipleDatabasesTests.original_redis_db2.flushdb()
		MultipleDatabasesTests.original_redis_db3.flushdb()

	@classmethod
	def tearDownClass(cls):
		# clear the database after tests
		MultipleDatabasesTests.original_redis_db2.flushdb()
		MultipleDatabasesTests.original_redis_db3.flushdb()

	@staticmethod
	def get_random_integer():
		return randint(0, 1_000_000)

	@staticmethod
	def get_random_string(length: int = randint(10, 20)):
		return ''.join(choice(ascii_letters + digits) for _ in range(length))

	def test_ping_001(self):
		""" Service db=0 is available """
		self.assertTrue(MultipleDatabasesTests.r2.r_ping())

	def test_ping_002(self):
		""" Service db=1 is available """
		self.assertTrue(MultipleDatabasesTests.r3.r_ping())

	def test_ping_003(self):
		wrong_r = PyRedis(host='unknown')
		self.assertFalse(wrong_r.r_ping())

	def test_r_remove_all_keys_local_001(self):
		pass

	def test_r_remove_all_keys_local_002(self):
		pass

	def test_r_remove_all_keys_001(self):
		MultipleDatabasesTests.original_redis_db2.flushall()
		MultipleDatabasesTests.original_redis_db3.flushall()

		# for first database
		key_0: str = MultipleDatabasesTests.get_random_string(length=3)
		MultipleDatabasesTests.r2.r_set(key_0, key_0)
		res_0: str = MultipleDatabasesTests.r2.r_get(key_0)
		self.assertEqual(res_0, key_0)

		# for second database
		key_1: str = MultipleDatabasesTests.get_random_string(length=5)
		MultipleDatabasesTests.r3.r_set(key_1, key_1)
		res_1: str = MultipleDatabasesTests.r3.r_get(key_1)
		self.assertEqual(res_1, key_1)

		count_keys: int = MultipleDatabasesTests.r2.r_remove_all_keys(get_count_keys=True)
		res_0: None = MultipleDatabasesTests.r2.r_get(key_0)
		res_1: None = MultipleDatabasesTests.r3.r_get(key_1)
		self.assertEqual(res_0, None)
		self.assertEqual(res_1, None)
		self.assertEqual(count_keys, 2)

	def test_r_remove_all_keys_002(self):
		MultipleDatabasesTests.original_redis_db2.flushall()
		MultipleDatabasesTests.original_redis_db3.flushall()

		# for first database
		key_0: str = MultipleDatabasesTests.get_random_string(length=3)
		MultipleDatabasesTests.r2.r_set(key_0, key_0)
		res_0: str = MultipleDatabasesTests.r2.r_get(key_0)
		self.assertEqual(res_0, key_0)

		# for second database
		key_1: str = MultipleDatabasesTests.get_random_string(length=5)
		MultipleDatabasesTests.r3.r_set(key_1, key_1)
		res_1: str = MultipleDatabasesTests.r3.r_get(key_1)
		self.assertEqual(res_1, key_1)

		count_keys = MultipleDatabasesTests.r2.r_remove_all_keys(get_count_keys=True)
		res_0: None = MultipleDatabasesTests.r2.r_get(key_0)
		res_1: None = MultipleDatabasesTests.r3.r_get(key_1)
		self.assertEqual(res_0, None)
		self.assertEqual(res_1, None)
		self.assertEqual(count_keys, 2)

	def test_keys_in_different_dbs_001(self):
		key_0: str = 'test_keys_in_different_dbs_001_db3'
		key_1: str = 'test_keys_in_different_dbs_001_db4'
		MultipleDatabasesTests.r2.r_set(key_0, key_0)
		MultipleDatabasesTests.r3.r_set(key_1, key_1)
		self.assertIsNone(MultipleDatabasesTests.r2.r_get(key_1))  # get key for db4 from db3
		self.assertIsNone(MultipleDatabasesTests.r3.r_get(key_0))  # get key for db3 from db4


if __name__ == '__main__':
	unittest.main()
