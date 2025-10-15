"""
Testing using the library as a PyPI package
"""

import unittest
from pyluaredis import PyRedis

from connection_params import REDIS_PWS, REDIS_HOST, REDIS_PORT, REDIS_USERNAME

redis_db: int = 0


class LibraryTests(unittest.TestCase):
	# def setUp(self):
	# 	self.maxDiff = None

	r = PyRedis(
		host=REDIS_HOST,
		port=REDIS_PORT,
		password=REDIS_PWS,
		username=REDIS_USERNAME,
		db=redis_db,
		socket_timeout=5
	)

	def test_ping_001(self):
		""" Service is available """
		original_redis = LibraryTests.r.redis_py()
		self.assertTrue(original_redis.ping())

	def test_ping_002(self):
		""" Service is available """
		self.assertTrue(LibraryTests.r.r_ping())

	def test_ping_003(self):
		wrong_r = PyRedis(host='unknown')
		self.assertFalse(wrong_r.r_ping())
