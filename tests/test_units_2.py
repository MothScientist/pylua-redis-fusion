import unittest
from dotenv import load_dotenv
from os import getenv
from random import randint, choice, random
from string import ascii_letters, digits
from sys import path as sys_path

sys_path.append('../')
from src.client import PyRedis

load_dotenv('../src/redis.env')  # Load environment variables from redis.env file
redis_psw: str = getenv('REDIS_PSW')
redis_db: int = int(getenv('REDIS_DB')) or 0
redis_host: str = getenv('REDIS_HOST') or 'localhost'
redis_port: int = int(getenv('REDIS_PORT')) or 6379
redis_username: str = getenv('REDIS_USERNAME') or 'default'


class TtlTests(unittest.TestCase):
	"""
	Tests to check the lifetime of keys, the sleep() function will be used, so all other parameters are optimized as much as possible
	"""
	# def setUp(self):
	# 	self.maxDiff = None

	r = PyRedis(
		host=redis_host,
		port=redis_port,
		password=redis_psw,
		username=redis_username,
		db=redis_db,
		socket_timeout=.1
	)

	@staticmethod
	def get_random_integer():
		return randint(0, 100)

	@staticmethod
	def get_random_string(length: int = randint(5, 10)):
		return ''.join(choice(ascii_letters + digits) for _ in range(length))

	def test_ping(self):
		self.assertTrue(TtlTests.r.r_ping())


if __name__ == '__main__':
	from redis import Redis, ConnectionPool
	_redis = Redis(connection_pool=ConnectionPool(
		host=redis_host,port=redis_port,db=0,password=redis_psw, username=redis_username
	))
	_redis.flushall()  # clear the database before tests

	unittest.main()
