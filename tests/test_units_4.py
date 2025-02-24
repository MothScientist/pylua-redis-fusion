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


class MultipleDatabasesTests(unittest.TestCase):
	# def setUp(self):
	# 	self.maxDiff = None

	r0 = PyRedis(
		host=redis_host,
		port=redis_port,
		password=redis_psw,
		username=redis_username,
		db=0,
		socket_timeout=1
	)

	r1 = PyRedis(
		host=redis_host,
		port=redis_port,
		password=redis_psw,
		username=redis_username,
		db=1,
		socket_timeout=1
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
