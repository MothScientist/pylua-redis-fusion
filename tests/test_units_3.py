import unittest
from redis import Redis, ConnectionPool
from sys import path as sys_path

from connection_params import REDIS_PWS, REDIS_HOST, REDIS_PORT, REDIS_USERNAME
sys_path.append('../')
from pyluaredis.client import PyRedis

redis_db: int = 4


class ContextManagerTests(unittest.TestCase):
	"""
	"""
	# def setUp(self):
	# 	self.maxDiff = None

	original_redis = Redis(connection_pool=ConnectionPool(
		host=REDIS_HOST, port=REDIS_PORT, db=redis_db, password=REDIS_PWS, username=REDIS_USERNAME
	))

	@classmethod
	def setUpClass(cls):
		ContextManagerTests.original_redis.flushdb()  # clear the database before tests

	@classmethod
	def tearDownClass(cls):
		ContextManagerTests.original_redis.flushdb()  # clear the database after tests

	def test_ping(self):
		""" Service is available """
		self.assertTrue(PyRedis(
				host=REDIS_HOST,
				port=REDIS_PORT,
				password=REDIS_PWS,
				username=REDIS_USERNAME,
				db=redis_db,
				socket_timeout=.1
		).r_ping())

	def test_with_001(self):
		with PyRedis(
				host=REDIS_HOST,
				port=REDIS_PORT,
				password=REDIS_PWS,
				username=REDIS_USERNAME,
				db=redis_db,
				socket_timeout=.1
		) as redis_conn:
			conn = redis_conn
			self.assertTrue(redis_conn.r_ping())

		self.assertRaises(AttributeError, conn.r_ping)

	def test_with_002(self):
		with PyRedis(
				host=REDIS_HOST,
				port=REDIS_PORT,
				password=REDIS_PWS,
				username=REDIS_USERNAME,
				db=redis_db,
				socket_timeout=.1
		) as redis_conn:
			conn = redis_conn
			key: str = 'RedisContextManager'
			redis_conn.r_set(key, key)
			self.assertEqual(redis_conn.r_get(key), key)

		self.assertRaises(AttributeError, conn.r_ping)


if __name__ == '__main__':
	unittest.main()
