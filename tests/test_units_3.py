import unittest
from redis import Redis, ConnectionPool
from sys import path as sys_path

from connection_params import REDIS_PWS, REDIS_HOST, REDIS_PORT, REDIS_USERNAME
sys_path.append('../')
from src.client import PyRedis

redis_db: int = 3


class ContextManagerTests(unittest.TestCase):
	"""
	"""
	# def setUp(self):
	# 	self.maxDiff = None

	r = PyRedis(
		host=REDIS_HOST,
		port=REDIS_PORT,
		password=REDIS_PWS,
		username=REDIS_USERNAME,
		db=redis_db,
		socket_timeout=.1
	)

	original_redis = Redis(connection_pool=ConnectionPool(
		host=REDIS_HOST, port=REDIS_PORT, db=redis_db, password=REDIS_PWS, username=REDIS_USERNAME
	))

	@classmethod
	def setUpClass(cls):
		ContextManagerTests.original_redis.flushdb()  # clear the database after tests

	@classmethod
	def tearDownClass(cls):
		ContextManagerTests.original_redis.flushdb()  # clear the database before tests

	def test_ping(self):
		""" Service is available """
		self.assertTrue(ContextManagerTests.r.r_ping())

	def test_with_001(self):
		with ContextManagerTests.r as redis_conn:
			self.assertTrue(redis_conn.r_ping())

	def test_with_002(self):
		with ContextManagerTests.r as redis_conn:
			key: str = 'RedisContextManager'
			redis_conn.r_set(key, key)
			self.assertEqual(redis_conn.r_get(key), key)


if __name__ == '__main__':
	unittest.main()
