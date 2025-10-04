"""
Testing using the library as a PyPI package
"""

import unittest
from pyluaredis.client import PyRedis
from random import randint, choice
from string import ascii_letters, digits

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

	original_redis = r.redis_py

	@classmethod
	def setUpClass(cls):
		LibraryTests.original_redis.flushdb()  # clear the database before tests

	@classmethod
	def tearDownClass(cls):
		LibraryTests.original_redis.flushdb()  # clear the database after tests

	@staticmethod
	def get_random_integer():
		return randint(0, 1_000_000)

	@staticmethod
	def get_random_string(length: int = randint(10, 20)):
		return ''.join(choice(ascii_letters + digits) for _ in range(length))

	def test_ping_001(self):
		""" Service is available """
		self.assertTrue(LibraryTests.r.r_ping())

	def test_ping_002(self):
		wrong_r = PyRedis(host='unknown')
		self.assertFalse(wrong_r.r_ping())
