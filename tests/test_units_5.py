"""
Checking the execution and saving of user scripts
"""
import unittest
from redis import Redis, ConnectionPool
from random import randint, choice, random
from string import ascii_letters, digits
from sys import path as sys_path

from connection_params import REDIS_PWS, REDIS_HOST, REDIS_PORT, REDIS_USERNAME

sys_path.append('../')
from pyluaredis.client import PyRedis

redis_db: int = 6


class UserScriptsInterface(unittest.TestCase):
	"""
	Testing custom user functions
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

	@staticmethod
	def clear_dictionaries():
		UserScriptsInterface.r.lua_scripts_sha.clear()
		UserScriptsInterface.r.user_lua_scripts_buffer.clear()

	@classmethod
	def setUpClass(cls):
		cls.clear_dictionaries()
		UserScriptsInterface.original_redis.flushdb()  # clear the database before tests

	@classmethod
	def tearDownClass(cls):
		cls.clear_dictionaries()
		UserScriptsInterface.original_redis.flushdb()  # clear the database after tests

	@staticmethod
	def get_random_string(length: int = randint(5, 10)):
		return ''.join(choice(ascii_letters + digits) for _ in range(length))

	def test_ping(self):
		""" Service is available """
		self.assertTrue(UserScriptsInterface.r.r_ping())

	# redis_py object ##################################################################################################

	def test_get_main_object_1(self):
		obj = UserScriptsInterface.r.redis_py()
		self.assertTrue(obj.ping())

	def test_get_main_object_2(self):
		obj: Redis = UserScriptsInterface.r.redis_py()
		key: str = self.test_get_main_object_2.__name__
		obj.set(key, key)
		res: str = obj.get(key)
		self.assertEqual(key, res)

	def test_get_main_object_3(self):
		obj: Redis = UserScriptsInterface.r.redis_py()
		key: str = self.test_get_main_object_3.__name__
		obj.flushdb()
		obj.set(key, key)
		res: int = obj.dbsize()
		self.assertTrue(res == 1)

	def test_get_main_object_4(self):
		obj: Redis = UserScriptsInterface.r.redis_py()
		obj.flushdb()
		res: int = obj.dbsize()
		self.assertTrue(res == 0)

	def test_get_main_object_5(self):
		obj: Redis = UserScriptsInterface.r.redis_py()
		key: str = self.test_get_main_object_5.__name__
		value: list = [str(i) for i in range(randint(10, 25))]
		obj.rpush(key, *value)
		res: list = obj.lrange(key, 0, -1)
		self.assertEqual(res, value)

	# load_lua_script / run_lua_script #################################################################################

	def test_load_and_run_lua_users_script_1(self):
		""" User script with buffer """
		UserScriptsInterface.clear_dictionaries()
		key: str = self.test_load_and_run_lua_users_script_1.__name__
		value: str = UserScriptsInterface.get_random_string()
		lua_script: str = \
			(
				'local key = KEYS[1];'
				'local value = ARGV[1];'
				'redis.call("SET", key, value);'
				'local key_exist = redis.call("EXISTS", key) == 1;'
				'return key_exist'
			)
		sha: str = UserScriptsInterface.r.load_lua_script(lua_script, use_buffer=True)
		self.assertTrue(len(sha) > 0)
		key_exist = UserScriptsInterface.r.run_lua_script(1, key, value, sha=sha)
		self.assertTrue(key_exist)
		# check buffer
		self.assertEqual(UserScriptsInterface.r.lua_scripts_sha, dict())
		self.assertTrue(lua_script in UserScriptsInterface.r.user_lua_scripts_buffer)
		self.assertTrue(sha == UserScriptsInterface.r.user_lua_scripts_buffer.get(lua_script))

	def test_load_and_run_lua_users_script_2(self):
		""" User script without buffer """
		UserScriptsInterface.clear_dictionaries()
		key: str = self.test_load_and_run_lua_users_script_2.__name__
		value: str = UserScriptsInterface.get_random_string()
		lua_script: str = \
			(
				'local key = KEYS[1];'
				'local value = ARGV[1];'
				'redis.call("SET", key, value);'
				'local key_exist = redis.call("EXISTS", key) == 1;'
				'return key_exist'
			)
		sha: str = UserScriptsInterface.r.load_lua_script(lua_script, use_buffer=False)
		self.assertTrue(len(sha) > 0)
		key_exist = UserScriptsInterface.r.run_lua_script(1, key, value, sha=sha)
		self.assertTrue(key_exist)
		# check buffer
		self.assertEqual(UserScriptsInterface.r.lua_scripts_sha, dict())
		self.assertEqual(UserScriptsInterface.r.user_lua_scripts_buffer, dict())

	def test_load_library_lua_func_obj_001(self):
		script: str = UserScriptsInterface.r._PyRedis__load_lua_script_from_file('get_helper')
		self.assertNotEqual(script, '')
		self.assertTrue(isinstance(script, str))

	def test_load_library_lua_func_obj_002(self):
		res = UserScriptsInterface.r._PyRedis__load_lua_script_from_file('set_arrays_helper')
		self.assertNotEqual(res, '')
		self.assertTrue(isinstance(res, str))

	def test_load_library_lua_func_obj_003(self):
		with self.assertRaises(FileNotFoundError):
			UserScriptsInterface.r._PyRedis__load_lua_script_from_file('unknown_script')

	# flush_lua_scripts ################################################################################################
