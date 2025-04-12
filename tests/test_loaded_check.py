"""
Checking the execution and saving of user scripts
"""
import unittest
from time import perf_counter
from redis import Redis, ConnectionPool
from random import randint
from sys import path as sys_path

from connection_params import REDIS_PWS, REDIS_HOST, REDIS_PORT, REDIS_USERNAME

sys_path.append('../')
from src.client import PyRedis

redis_db: int = 6


class LoadedTests(unittest.TestCase):
	"""
	TODO
	"""
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

	original_redis = Redis(connection_pool=ConnectionPool(
		host=REDIS_HOST, port=REDIS_PORT, db=redis_db, password=REDIS_PWS, username=REDIS_USERNAME
	))

	@staticmethod
	def clear_dictionaries():
		LoadedTests.r.lua_scripts_sha.clear()
		LoadedTests.r.user_lua_scripts_buffer.clear()

	@classmethod
	def setUpClass(cls):
		cls.clear_dictionaries()
		LoadedTests.original_redis.flushdb()  # clear the database before tests

	@classmethod
	def tearDownClass(cls):
		cls.clear_dictionaries()
		LoadedTests.original_redis.flushdb()  # clear the database after tests

	def test_ping(self):
		""" Service is available """
		self.assertTrue(LoadedTests.r.r_ping())

	# Cycle test #######################################################################################################

	def test_cycle_set_get_delete_001(self):
		start_time = perf_counter()
		_iterations: int = randint(250, 500)
		for value, key in enumerate([i for i in range(_iterations)]):
			key = str(key)
			str_value = str(value)
			self.assertIsNone(LoadedTests.r.r_set(key, value))
			self.assertEqual(LoadedTests.r.r_get(key), str_value)
			self.assertEqual(LoadedTests.r.r_delete(key, returning=True), str_value)
			self.assertIsNone(LoadedTests.r.r_get(key))
		end_time = perf_counter()
		print(f'test_cycle_set_get_delete_001: iterations = {_iterations}; {end_time-start_time:.3f} sec.; ')

	# Loaded test ######################################################################################################

	def test_loaded_001(self):
		""" List | 5_500 <= len <= 10_000 : r_set -> append_value_to_array -> r_get - with chunks """
		key: str = self.test_loaded_001.__name__
		value: list = [randint(0, 100_000) for _ in range(randint(5_500, 10_000))]
		_len = len(value)
		new_value: int = randint(500_000, 1_000_000)
		_index: int = _len * (randint(25, 75) // 100)  # 25-75%

		start_time = perf_counter()
		LoadedTests.r.r_set(key, value)
		end_time = perf_counter()
		set_time = end_time - start_time

		start_time = perf_counter()
		res: list = LoadedTests.r.r_get(key, convert_to_type='int')
		end_time = perf_counter()
		self.assertTrue(len(res) == len(value))
		get_time_1 = end_time - start_time

		start_time = perf_counter()
		LoadedTests.r.append_value_to_array(key, new_value, index=_index)
		end_time = perf_counter()
		append_time = end_time - start_time

		start_time = perf_counter()
		res: list = LoadedTests.r.r_get(key, convert_to_type='int')
		end_time = perf_counter()
		get_time_2 = end_time - start_time

		self.assertTrue(len(res) == len(value) + 1)
		self.assertEqual(res[_index], new_value)

		print(
			f'test_loaded_001: len = {_len} + 1; '
			f'r_set = {set_time:.3f} sec.; '
			f'append_value = {append_time:.3f} sec.; '
			f'r_get = {(get_time_1 + get_time_2) / 2:.3f} sec.'
		)

	def test_loaded_002(self):
		""" List | 250_000 <= len <= 500_000 : r_set -> append_value_to_array in 20-30% len -> r_get - with chunks """
		key: str = self.test_loaded_002.__name__
		value: list = [randint(0, 100_000) for _ in range(randint(250_000, 500_000))]
		_len = len(value)
		new_value: int = randint(500_000, 1_000_000)
		_index: int = _len * (randint(20, 30) // 100)  # 20-30%

		start_time = perf_counter()
		LoadedTests.r.r_set(key, value)
		end_time = perf_counter()
		set_time = end_time - start_time

		res: list = LoadedTests.r.r_get(key, convert_to_type='int')
		self.assertTrue(len(res) == len(value))

		start_time = perf_counter()
		LoadedTests.r.append_value_to_array(key, new_value, index=_index)
		end_time = perf_counter()
		append_time = end_time - start_time

		start_time = perf_counter()
		res: list = LoadedTests.r.r_get(key, convert_to_type='int')
		end_time = perf_counter()
		get_time = end_time - start_time

		self.assertTrue(len(res) == len(value) + 1)
		self.assertEqual(res[_index], new_value)

		print(
			f'test_loaded_002 (20-30%): len = {_len} + 1; '
			f'r_set = {set_time:.3f} sec.; '
			f'append_value = {append_time:.3f} sec.; '
			f'r_get = {get_time:.3f} sec.'
		)

	def test_loaded_003(self):
		""" List | 250_000 <= len <= 500_000 : r_set -> append_value_to_array in 45-55% len -> r_get - with chunks """
		key: str = self.test_loaded_003.__name__
		value: list = [randint(0, 100_000) for _ in range(randint(250_000, 500_000))]
		_len = len(value)
		new_value: int = randint(500_000, 1_000_000)
		_index: int = _len * (randint(45, 55) // 100)  # 45-55%

		start_time = perf_counter()
		LoadedTests.r.r_set(key, value)
		end_time = perf_counter()
		set_time = end_time - start_time

		res: list = LoadedTests.r.r_get(key, convert_to_type='int')
		self.assertTrue(len(res) == len(value))

		start_time = perf_counter()
		LoadedTests.r.append_value_to_array(key, new_value, index=_index)
		end_time = perf_counter()
		append_time = end_time - start_time

		start_time = perf_counter()
		res: list = LoadedTests.r.r_get(key, convert_to_type='int')
		end_time = perf_counter()
		get_time = end_time - start_time

		self.assertTrue(len(res) == len(value) + 1)
		self.assertEqual(res[_index], new_value)

		print(
			f'test_loaded_003 (45-55%): len = {_len} + 1; '
			f'r_set = {set_time:.3f} sec.; '
			f'append_value = {append_time:.3f} sec.; '
			f'r_get = {get_time:.3f} sec.'
		)

	def test_loaded_004(self):
		""" List | 250_000 <= len <= 500_000 : r_set -> append_value_to_array in 75-90% len -> r_get - with chunks"""
		key: str = self.test_loaded_004.__name__
		value: list = [randint(0, 100_000) for _ in range(randint(250_000, 500_000))]
		_len = len(value)
		new_value: int = randint(500_000, 1_000_000)
		_index: int = _len * (randint(75, 90) // 100)  # 75-90%

		start_time = perf_counter()
		LoadedTests.r.r_set(key, value)
		end_time = perf_counter()
		set_time = end_time - start_time

		res: list = LoadedTests.r.r_get(key, convert_to_type='int')
		self.assertTrue(len(res) == len(value))

		start_time = perf_counter()
		LoadedTests.r.append_value_to_array(key, new_value, index=_index)
		end_time = perf_counter()
		append_time = end_time - start_time

		# check time start
		start_time = perf_counter()
		res: list = LoadedTests.r.r_get(key, convert_to_type='int')
		# check time finish
		end_time = perf_counter()
		# time assert
		get_time = end_time - start_time

		self.assertTrue(len(res) == len(value) + 1)
		self.assertEqual(res[_index], new_value)

		print(
			f'test_loaded_004 (75-90%): len = {_len} + 1; '
			f'r_set = {set_time:.3f} sec.; '
			f'append_value = {append_time:.3f} sec.; '
			f'r_get = {get_time:.3f} sec.'
		)

	def test_loaded_005(self):
		""" List | 3_000 <= len <= 4_500 : set | append_value_to_array in 30-70% len | get  - without chunks"""
		key: str = self.test_loaded_005.__name__
		value: list = [randint(0, 100_000) for _ in range(randint(3_000, 4_500))]
		_len = len(value)
		new_value: int = randint(500_000, 1_000_000)
		_index: int = _len * (randint(30, 70) // 100)

		start_time = perf_counter()
		LoadedTests.r.r_set(key, value)
		end_time = perf_counter()
		set_time = end_time - start_time

		res: list = LoadedTests.r.r_get(key, convert_to_type='int')
		self.assertTrue(len(res) == len(value))

		start_time = perf_counter()
		LoadedTests.r.append_value_to_array(key, new_value, index=_index)
		end_time = perf_counter()
		append_time = end_time - start_time

		start_time = perf_counter()
		res: list = LoadedTests.r.r_get(key, convert_to_type='int')
		end_time = perf_counter()
		get_time = end_time - start_time

		self.assertTrue(len(res) == len(value) + 1)
		self.assertEqual(res[_index], new_value)

		print(
			f'test_loaded_005: len = {_len} + 1; '
			f'r_set = {set_time:.3f} sec.; '
			f'append_value = {append_time:.3f} sec.; '
			f'r_get = {get_time:.3f} sec.'
		)

	def test_loaded_006(self):
		""" Set | 20_000 <= len <= 25_000 : r_set -> append_value_to_array -> r_get  - with chunks"""
		key: str = self.test_loaded_006.__name__
		value: set = {str(i) for i in range(randint(20_000, 25_000))}
		_len = len(value)
		new_value: int = randint(500_000, 1_000_000)

		LoadedTests.r.r_set(key, value)

		res: list = LoadedTests.r.r_get(key)
		self.assertTrue(len(res) == len(value))

		LoadedTests.r.append_value_to_array(key, new_value)

		res: list = LoadedTests.r.r_get(key)

		self.assertTrue(len(res) == len(value) + 1)

	def test_loaded_007(self):
		""" Tuple | 20_000 <= len <= 25_000 : r_set -> append_value_to_array -> r_get  - with chunks"""
		key: str = self.test_loaded_007.__name__
		value: tuple = tuple(str(i) for i in range(randint(20_000, 25_000)))
		_len = len(value)
		new_value: int = randint(500_000, 1_000_000)
		_index: int = _len * (randint(25, 75) // 100)

		LoadedTests.r.r_set(key, value)

		res: list = LoadedTests.r.r_get(key)
		self.assertTrue(len(res) == len(value))

		LoadedTests.r.append_value_to_array(key, new_value)

		res: list = LoadedTests.r.r_get(key)

		self.assertTrue(len(res) == len(value) + 1)
		self.assertEqual(res[_index], new_value)

	def test_loaded_008(self):
		""" Frozenset | 20_000 <= len <= 25_000 : r_set -> append_value_to_array -> r_get  - with chunks"""
		key: str = self.test_loaded_006.__name__
		value: frozenset = frozenset(str(i) for i in range(randint(20_000, 25_000)))
		_len = len(value)
		new_value: int = randint(500_000, 1_000_000)

		LoadedTests.r.r_set(key, value)

		res: list = LoadedTests.r.r_get(key)
		self.assertTrue(len(res) == len(value))

		LoadedTests.r.append_value_to_array(key, new_value)

		res: list = LoadedTests.r.r_get(key)

		self.assertTrue(len(res) == len(value) + 1)
