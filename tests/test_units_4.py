import unittest
from redis import Redis, ConnectionPool
from sys import path as sys_path

sys_path.append('../')
from src.client import PyRedis
from tests.connection_params import REDIS_PWS, REDIS_HOST, REDIS_PORT, REDIS_USERNAME

redis_db: int = 4


class LuaScriptsSHATests(unittest.TestCase):
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
		LuaScriptsSHATests.original_redis.flushdb()  # clear the database after tests

	@classmethod
	def tearDownClass(cls):
		LuaScriptsSHATests.original_redis.flushdb()  # clear the database before tests

	def test_ping(self):
		""" Service is available """
		self.assertTrue(LuaScriptsSHATests.r.r_ping())

	def test_lua_sha_001(self):
		self.assertEqual(LuaScriptsSHATests.r.eval_status, {})

	def test_lua_sha_002(self):
		key: str = 'lua_sha_002'
		LuaScriptsSHATests.r.r_set(key, key)
		self.assertTrue('set_not_array_helper' in LuaScriptsSHATests.r.eval_status)

	def test_lua_sha_003(self):
		key: str = 'lua_sha_002'
		LuaScriptsSHATests.r.r_set(key, key)
		LuaScriptsSHATests.r.r_set(key, [key])
		self.assertTrue(
			all(key in LuaScriptsSHATests.r.eval_status for key in ('set_not_array_helper', 'arrays_helper'))
		)

	def test_lua_sha_004(self):
		key: str = 'lua_sha_004'
		LuaScriptsSHATests.r.r_set(key, key)
		self.assertTrue(
			all(isinstance(value, str) and value for value in LuaScriptsSHATests.r.eval_status.values())
		)


if __name__ == '__main__':
	unittest.main()
