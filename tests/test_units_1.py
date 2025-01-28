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
redis_db: int = int(getenv('REDIS_DB'))
redis_host: str = getenv('REDIS_HOST')
redis_port: int = int(getenv('REDIS_PORT'))


class SmokeTests(unittest.TestCase):
	# def setUp(self):
	# 	self.maxDiff = None

	r = PyRedis(redis_host, redis_port, redis_psw, db=redis_db, socket_timeout=.1)  # .1 special for smoke tests

	@staticmethod
	def get_random_integer():
		return randint(0, 1_000_000)

	@staticmethod
	def get_random_string(length: int = randint(10, 20)):
		return ''.join(choice(ascii_letters + digits) for _ in range(length))

	def test_ping(self):
		self.assertTrue(SmokeTests.r.r_ping())

	# set/get ##########################################################################################################

	def test_set_get_int_001(self):
		key: str = 'set_get_int_001'
		value: int = SmokeTests.get_random_integer()
		self.assertIsNone(SmokeTests.r.r_set(key, value))
		res = SmokeTests.r.r_get(key)
		self.assertEqual(int(res), value)

	def test_set_get_int_002(self):
		key: str = 'set_get_int_002'
		value_1: int = SmokeTests.get_random_integer()
		self.assertIsNone(SmokeTests.r.r_set(key, value_1))
		res_1 = SmokeTests.r.r_get(key)
		self.assertEqual(int(res_1), value_1)

		# rewrite
		value_2: int = SmokeTests.get_random_integer()
		self.assertIsNone(SmokeTests.r.r_set(key, value_2))
		res_2 = SmokeTests.r.r_get(key)
		self.assertEqual(int(res_2), value_2)

	def test_set_get_int_003(self): # convert_to_type
		key: str = 'set_get_int_003'
		value: int = SmokeTests.get_random_integer()
		self.assertIsNone(SmokeTests.r.r_set(key, value))
		res = SmokeTests.r.r_get(key, convert_to_type='int')
		self.assertEqual(res, value)

	def test_set_get_int_004(self): # convert_to_type
		key: str = 'set_get_int_004'
		value: int = SmokeTests.get_random_integer()
		self.assertIsNone(SmokeTests.r.r_set(key, value))
		res = SmokeTests.r.r_get(key, convert_to_type='integer')
		self.assertEqual(res, value)

	def test_set_get_float_001(self):
		key: str = 'set_get_float_001'
		value: float = float(SmokeTests.get_random_integer())
		self.assertIsNone(SmokeTests.r.r_set(key, value))
		res = SmokeTests.r.r_get(key)
		self.assertEqual(float(res), value)

	def test_set_get_float_002(self):
		key: str = 'set_get_float_002'
		value_1: float = float(SmokeTests.get_random_integer())
		self.assertIsNone(SmokeTests.r.r_set(key, value_1))
		res_1 = SmokeTests.r.r_get(key)
		self.assertEqual(float(res_1), value_1)

		# rewrite
		value_2: float = float(SmokeTests.get_random_integer())
		self.assertIsNone(SmokeTests.r.r_set(key, value_2))
		res_2 = SmokeTests.r.r_get(key)
		self.assertEqual(float(res_2), value_2)

	def test_set_get_float_003(self): # convert_to_type
		key: str = 'set_get_float_003'
		value: float = float(SmokeTests.get_random_integer())
		self.assertIsNone(SmokeTests.r.r_set(key, value))
		res = SmokeTests.r.r_get(key, convert_to_type='float')
		self.assertEqual(res, value)

	def test_set_get_float_004(self): # convert_to_type
		key: str = 'set_get_float_004'
		value: float = float(SmokeTests.get_random_integer())
		self.assertIsNone(SmokeTests.r.r_set(key, value))
		res = SmokeTests.r.r_get(key, convert_to_type='double')
		self.assertEqual(res, value)

	def test_set_get_float_005(self): # convert_to_type
		key: str = 'set_get_float_005'
		value: float = float(SmokeTests.get_random_integer())
		self.assertIsNone(SmokeTests.r.r_set(key, value))
		res = SmokeTests.r.r_get(key, convert_to_type='numeric')
		self.assertEqual(res, value)

	def test_set_get_str_001(self):
		key: str = 'set_get_str_001'
		value: str = SmokeTests.get_random_string()
		self.assertIsNone(SmokeTests.r.r_set(key, value))
		res = SmokeTests.r.r_get(key)
		self.assertEqual(res, value)

	def test_set_get_str_002(self):
		key: str = 'set_get_str_002'
		value_1: str = SmokeTests.get_random_string()
		self.assertIsNone(SmokeTests.r.r_set(key, value_1))
		res_1: str = SmokeTests.r.r_get(key)
		self.assertEqual(res_1, value_1)

		# rewrite
		value_2: str = SmokeTests.get_random_string()
		self.assertIsNone(SmokeTests.r.r_set(key, value_2))
		res_2: str = SmokeTests.r.r_get(key)
		self.assertEqual(res_2, value_2)

	def test_set_get_bool_001(self): # convert_to_type
		key: str = 'set_get_bool_001'
		value: bool = True
		self.assertIsNone(SmokeTests.r.r_set(key, value))
		res = SmokeTests.r.r_get(key, convert_to_type='bool')
		self.assertEqual(res, value)

	def test_set_get_bool_002(self): # convert_to_type
		key: str = 'set_get_bool_002'
		value: bool = False
		self.assertIsNone(SmokeTests.r.r_set(key, value))
		res = SmokeTests.r.r_get(key, convert_to_type='bool')
		self.assertEqual(res, value)

	def test_set_get_bool_003(self):  # convert_to_type
		key: str = 'set_get_bool_003'
		value: int = 1
		self.assertIsNone(SmokeTests.r.r_set(key, value))
		res = SmokeTests.r.r_get(key, convert_to_type='bool')
		self.assertEqual(res, bool(value))

	def test_set_get_bool_004(self):  # convert_to_type
		key: str = 'set_get_bool_004'
		value: int = 0
		self.assertIsNone(SmokeTests.r.r_set(key, value))
		res = SmokeTests.r.r_get(key, convert_to_type='bool')
		self.assertEqual(res, bool(value))

	def test_set_get_bool_005(self): # convert_to_type
		key: str = 'set_get_bool_005'
		value: bool = True
		self.assertIsNone(SmokeTests.r.r_set(key, value))
		res = SmokeTests.r.r_get(key)
		self.assertEqual(res, str(value))

	def test_set_get_bool_006(self): # convert_to_type
		key: str = 'set_get_bool_006'
		value: bool = False
		self.assertIsNone(SmokeTests.r.r_set(key, value))
		res = SmokeTests.r.r_get(key)
		self.assertEqual(res, str(value))

	def test_set_get_list_001(self):
		key: str = 'set_get_list_001'
		value: list = [SmokeTests.get_random_integer() for _ in range(randint(10, 15))]
		self.assertIsNone(SmokeTests.r.r_set(key, value))
		res: list = list(map(int, SmokeTests.r.r_get(key)))
		self.assertEqual(res, value)

	def test_set_get_list_002(self):
		key: str = 'set_get_list_002'
		value_1: list = [SmokeTests.get_random_integer() for _ in range(randint(10, 25))]
		self.assertIsNone(SmokeTests.r.r_set(key, value_1))
		res_1: list = list(map(int, SmokeTests.r.r_get(key)))
		self.assertEqual(res_1, value_1)

		# rewrite
		value_2: list = [SmokeTests.get_random_integer() for _ in range(randint(10, 15))]
		self.assertIsNone(SmokeTests.r.r_set(key, value_2))
		res_2: list = list(map(int, SmokeTests.r.r_get(key)))
		self.assertEqual(res_2, value_2)

	def test_set_get_list_003(self):
		key: str = 'set_get_list_003'
		value: list = [SmokeTests.get_random_string() for _ in range(randint(10, 50))]
		self.assertIsNone(SmokeTests.r.r_set(key, value))
		res: list = list(map(str, SmokeTests.r.r_get(key)))
		self.assertEqual(res, value)

	def test_set_get_list_004(self): # convert_to_type
		key: str = 'set_get_list_004'
		value: list[bool] = [bool(randint(0, 1)) for _ in range(randint(10, 50))]
		self.assertIsNone(SmokeTests.r.r_set(key, value))
		res: list = list(SmokeTests.r.r_get(key, convert_to_type='boolean'))
		self.assertEqual(res, value)

	def test_set_get_tuple_001(self):
		key: str = 'set_get_tuple_001'
		value: tuple = tuple(SmokeTests.get_random_integer() for _ in range(randint(10, 25)))
		self.assertIsNone(SmokeTests.r.r_set(key, value))
		res: tuple = tuple(map(int, SmokeTests.r.r_get(key)))
		self.assertEqual(res, value)

	def test_set_get_tuple_002(self):
		key: str = 'set_get_tuple_002'
		value_1: tuple = tuple(SmokeTests.get_random_integer() for _ in range(randint(10, 25)))
		self.assertIsNone(SmokeTests.r.r_set(key, value_1))
		res_1: tuple = tuple(map(int, SmokeTests.r.r_get(key)))
		self.assertEqual(res_1, value_1)

		# rewrite
		value_2: tuple = tuple(SmokeTests.get_random_integer() for _ in range(randint(10, 15)))
		self.assertIsNone(SmokeTests.r.r_set(key, value_2))
		res_2: tuple = tuple(map(int, SmokeTests.r.r_get(key)))
		self.assertEqual(res_2, value_2)

	def test_set_get_tuple_003(self): # convert_to_type
		key: str = 'set_get_tuple_003'
		value: tuple = tuple(SmokeTests.get_random_string() for _ in range(randint(10, 50)))
		self.assertIsNone(SmokeTests.r.r_set(key, value))
		res: tuple = tuple(map(str, SmokeTests.r.r_get(key)))
		self.assertEqual(res, value)

	def test_set_get_tuple_004(self): # convert_to_type
		key: str = 'set_get_tuple_004'
		value: tuple = tuple(SmokeTests.get_random_integer() for _ in range(randint(10, 50)))
		self.assertIsNone(SmokeTests.r.r_set(key, value))
		res: tuple = tuple(SmokeTests.r.r_get(key, convert_to_type='int'))
		self.assertEqual(res, value)

	def test_set_get_tuple_005(self): # convert_to_type
		key: str = 'set_get_tuple_005'
		value: tuple = tuple(float(SmokeTests.get_random_integer()) for _ in range(randint(10, 25)))
		self.assertIsNone(SmokeTests.r.r_set(key, value))
		res: tuple = tuple(SmokeTests.r.r_get(key, convert_to_type='float'))
		self.assertEqual(res, value)

	def test_set_get_tuple_006(self): # convert_to_type
		key: str = 'set_get_tuple_006'
		value_1: tuple = tuple(bool(randint(0, 1)) for _ in range(randint(50, 100)))
		self.assertIsNone(SmokeTests.r.r_set(key, value_1))
		res_1: tuple = tuple(SmokeTests.r.r_get(key, convert_to_type='bool'))
		self.assertEqual(res_1, value_1)

		# rewrite (integer)
		value_2: int = SmokeTests.get_random_integer()
		self.assertIsNone(SmokeTests.r.r_set(key, value_2))
		res_2: int = SmokeTests.r.r_get(key, convert_to_type='integer')
		self.assertEqual(res_2, value_2)

		# rewrite (str)
		value_3: str = SmokeTests.get_random_string()
		self.assertIsNone(SmokeTests.r.r_set(key, value_3))
		res_3: str = SmokeTests.r.r_get(key)
		self.assertEqual(res_3, value_3)

	def test_set_get_set_001(self):
		key: str = 'set_get_set_001'
		value: set = set(SmokeTests.get_random_integer() for _ in range(randint(1, 100)))
		self.assertIsNone(SmokeTests.r.r_set(key, value))
		res: set = set(map(int, SmokeTests.r.r_get(key)))
		self.assertEqual(res, value)

	def test_set_get_set_002(self):
		key: str = 'set_get_set_002'
		value: set = set(SmokeTests.get_random_string() for _ in range(randint(1, 25))).union(
			set(str(SmokeTests.get_random_integer()) for _ in range(randint(1, 25)))
		)
		self.assertIsNone(SmokeTests.r.r_set(key, value))
		res: set = set(SmokeTests.r.r_get(key))
		self.assertEqual(res, value)

	def test_set_get_set_003(self): # convert_to_type
		key: str = 'set_get_set_003'
		value: set = set(SmokeTests.get_random_string() for _ in range(randint(1, 10))).union(
			set(SmokeTests.get_random_integer() for _ in range(randint(1, 10)))
		)
		self.assertIsNone(SmokeTests.r.r_set(key, value))
		res: set = set(SmokeTests.r.r_get(key, convert_to_type='int'))
		self.assertEqual(res, value)

	def test_set_get_set_004(self): # convert_to_type
		key: str = 'set_get_set_004'
		value: set = set(SmokeTests.get_random_integer() for _ in range(randint(50, 100)))
		self.assertIsNone(SmokeTests.r.r_set(key, value))
		res: set = set(SmokeTests.r.r_get(key, convert_to_type='int'))
		self.assertEqual(value, res)

	def test_set_get_set_005(self):
		key: str = 'set_get_set_005'
		value: set = set(SmokeTests.get_random_string() for _ in range(randint(50, 100)))
		self.assertIsNone(SmokeTests.r.r_set(key, value))
		res: set = set(SmokeTests.r.r_get(key))
		self.assertEqual(value, res)

	def test_set_get_set_006(self): # convert_to_type
		key: str = 'set_get_set_006'
		value: set = set(SmokeTests.get_random_string() for _ in range(randint(25, 50)))
		self.assertIsNone(SmokeTests.r.r_set(key, value))
		res: set = set(SmokeTests.r.r_get(key, convert_to_type='float'))  # str -> float = str
		self.assertEqual(value, res)

	def test_set_get_frozenset_001(self):
		key: str = 'set_get_frozenset_001'
		value: frozenset = frozenset(SmokeTests.get_random_string() for _ in range(randint(5, 10)))
		self.assertIsNone(SmokeTests.r.r_set(key, value))
		res: frozenset = frozenset(SmokeTests.r.r_get(key))
		self.assertEqual(value, res)

	def test_set_get_frozenset_002(self): # convert_to_type
		key: str = 'set_get_frozenset_002'
		value: frozenset = frozenset(SmokeTests.get_random_integer() for _ in range(randint(50, 100)))
		self.assertIsNone(SmokeTests.r.r_set(key, value))
		res: frozenset = frozenset(SmokeTests.r.r_get(key, convert_to_type='integer'))
		self.assertEqual(value, res)

	def test_set_get_frozenset_003(self): # convert_to_type
		key: str = 'set_get_frozenset_003'
		value: frozenset = frozenset(float(SmokeTests.get_random_integer()) for _ in range(randint(25, 50)))
		self.assertIsNone(SmokeTests.r.r_set(key, value))
		res: frozenset = frozenset(SmokeTests.r.r_get(key, convert_to_type='numeric'))
		self.assertEqual(value, res)

	def test_set_get_frozenset_004(self): # convert_to_type
		key: str = 'set_get_frozenset_004'
		value_1: frozenset = frozenset(SmokeTests.get_random_integer() for _ in range(randint(50, 100)))
		self.assertIsNone(SmokeTests.r.r_set(key, value_1))
		res_1: frozenset = frozenset(SmokeTests.r.r_get(key, convert_to_type='integer'))
		self.assertEqual(value_1, res_1)

		# rewrite
		value_2: frozenset = frozenset(SmokeTests.get_random_string() for _ in range(randint(5, 10)))
		self.assertIsNone(SmokeTests.r.r_set(key, value_2))
		res_2: frozenset = frozenset(SmokeTests.r.r_get(key))
		self.assertEqual(value_2, res_2)

	# change type, example: set (float) -> get (int) / set (list) -> get (tuple) #######################################

	def test_change_set_get_type_001(self):
		key: str = 'change_set_get_type_001'
		value: float = float(SmokeTests.get_random_integer()) + random()
		self.assertIsNone(SmokeTests.r.r_set(key, value))
		res: int = SmokeTests.r.r_get(key, convert_to_type='int')
		self.assertEqual(int(value), res, f'res = {res}; type(res) = {type(res)}')
		self.assertTrue(isinstance(res, int), type(res))

	def test_change_set_get_type_002(self):
		key: str = 'change_set_get_type_002'
		value: float = float(SmokeTests.get_random_integer() + random())
		self.assertIsNone(SmokeTests.r.r_set(key, value))
		res: int = SmokeTests.r.r_get(key, convert_to_type='integer')
		self.assertEqual(int(value), res, f'res = {res}; type(res) = {type(res)}')
		self.assertTrue(isinstance(res, int), type(res))

	def test_change_set_get_type_003(self):
		key: str = 'change_set_get_type_003'
		value: int = SmokeTests.get_random_integer()
		self.assertIsNone(SmokeTests.r.r_set(key, value))
		res: float = SmokeTests.r.r_get(key, convert_to_type='float')
		self.assertEqual(float(value), res, f'res = {res}; type(res) = {type(res)}')
		self.assertTrue(isinstance(res, float), type(res))

	def test_change_set_get_type_004(self):
		key: str = 'change_set_get_type_004'
		value: int = SmokeTests.get_random_integer()
		self.assertIsNone(SmokeTests.r.r_set(key, value))
		res: float = SmokeTests.r.r_get(key, convert_to_type='numeric')
		self.assertEqual(float(value), res, f'res = {res}; type(res) = {type(res)}')
		self.assertTrue(isinstance(res, float), type(res))

	def test_change_set_get_type_005(self):
		key: str = 'change_set_get_type_005'
		value: int = SmokeTests.get_random_integer()
		self.assertIsNone(SmokeTests.r.r_set(key, value))
		res: float = SmokeTests.r.r_get(key, convert_to_type='double')
		self.assertEqual(float(value), res, f'res = {res}; type(res) = {type(res)}')
		self.assertTrue(isinstance(res, float), type(res))

	def test_change_set_get_type_006(self):
		key: str = 'change_set_get_type_006'
		value: int = 0
		self.assertIsNone(SmokeTests.r.r_set(key, value))
		res: bool = SmokeTests.r.r_get(key, convert_to_type='bool')
		self.assertEqual(bool(value), res, f'res = {res}; type(res) = {type(res)}')
		self.assertTrue(isinstance(res, bool), type(res))

	def test_change_set_get_type_007(self):
		key: str = 'change_set_get_type_007'
		value: int = 1
		self.assertIsNone(SmokeTests.r.r_set(key, value))
		res: bool = SmokeTests.r.r_get(key, convert_to_type='boolean')
		self.assertEqual(bool(value), res, f'res = {res}; type(res) = {type(res)}')
		self.assertTrue(isinstance(res, bool), type(res))

	def test_change_set_get_type_008(self):
		""" Wrong type to convert """
		key: str = 'change_set_get_type_008'
		value: int = SmokeTests.get_random_integer()
		self.assertIsNone(SmokeTests.r.r_set(key, value))
		res: str = SmokeTests.r.r_get(key, convert_to_type='float1')
		self.assertEqual(str(value), res, f'res = {res}; type(res) = {type(res)}')
		self.assertTrue(isinstance(res, str), type(res))

	def test_change_set_get_type_009(self):
		""" Wrong type to convert """
		key: str = 'change_set_get_type_009'
		value: int = SmokeTests.get_random_integer()
		self.assertIsNone(SmokeTests.r.r_set(key, value))
		res: str = SmokeTests.r.r_get(key, convert_to_type='bigint')
		self.assertEqual(str(value), res, f'res = {res}; type(res) = {type(res)}')
		self.assertTrue(isinstance(res, str), type(res))

	# set/get/delete ###################################################################################################

	def test_set_get_delete_int_001(self):
		key: str = 'set_get_delete_int_001'
		value: int = SmokeTests.get_random_integer()

		self.assertIsNone(SmokeTests.r.r_set(key, value))
		res_1 = SmokeTests.r.r_get(key)
		self.assertEqual(int(res_1), value)

		# delete (without returning - None)
		self.assertIsNone(SmokeTests.r.r_delete(key))
		self.assertIsNone(SmokeTests.r.r_get(key))

		res_2 = SmokeTests.r.r_get(key)
		self.assertIsNone(res_2)

	def test_set_get_delete_int_002(self):
		key: str = 'set_get_delete_int_002'
		value: int = SmokeTests.get_random_integer()

		self.assertIsNone(SmokeTests.r.r_set(key, value))
		res_1 = SmokeTests.r.r_get(key)
		self.assertEqual(int(res_1), value)

		# delete (without returning - False)
		self.assertIsNone(SmokeTests.r.r_delete(key, returning=False))
		self.assertIsNone(SmokeTests.r.r_get(key))

		res_2 = SmokeTests.r.r_get(key)
		self.assertIsNone(res_2)

	def test_set_get_delete_int_003(self):
		key: str = 'set_get_delete_int_003'
		value: int = SmokeTests.get_random_integer()

		self.assertIsNone(SmokeTests.r.r_set(key, value))
		res_1 = SmokeTests.r.r_get(key)
		self.assertEqual(res_1, str(value))

		# delete (with returning)
		self.assertEqual(SmokeTests.r.r_delete(key, returning=True), str(value))
		self.assertIsNone(SmokeTests.r.r_get(key))

		res_2 = SmokeTests.r.r_get(key)
		self.assertIsNone(res_2)

	def test_set_get_delete_str_001(self):
		key: str = 'set_get_delete_str_001'
		value: str = SmokeTests.get_random_string()

		self.assertIsNone(SmokeTests.r.r_set(key, value))
		res_1 = SmokeTests.r.r_get(key)
		self.assertEqual(res_1, value)

		# delete (without returning - False)
		self.assertIsNone(SmokeTests.r.r_delete(key, returning=False))
		self.assertIsNone(SmokeTests.r.r_get(key))

		res_2 = SmokeTests.r.r_get(key)
		self.assertIsNone(res_2)

	def test_set_get_delete_str_002(self):
		key: str = 'set_get_delete_str_002'
		value: str = SmokeTests.get_random_string()

		self.assertIsNone(SmokeTests.r.r_set(key, value))
		res_1 = SmokeTests.r.r_get(key)
		self.assertEqual(res_1, value)

		# delete (with returning)
		self.assertEqual(SmokeTests.r.r_delete(key, returning=True), value)
		self.assertIsNone(SmokeTests.r.r_get(key))

		res_2 = SmokeTests.r.r_get(key)
		self.assertIsNone(res_2)

	def test_cycle_set_get_delete_001(self):
		for value, key in enumerate([i for i in range(100_000_000, 100_000_000 + randint(100, 500))]):
			key = str(key)
			str_value = str(value)
			self.assertIsNone(SmokeTests.r.r_set(key, value))
			self.assertEqual(SmokeTests.r.r_get(key), str_value)
			self.assertEqual(SmokeTests.r.r_delete(key, returning=True), str_value)
			self.assertIsNone(SmokeTests.r.r_get(key))

	# mass check keys ##################################################################################################

	def test_r_mass_check_keys_exists_001(self):
		keys: list = list({SmokeTests.get_random_string(length=randint(5, 15)) for _ in range(randint(50, 100))})
		for key in keys:
			SmokeTests.r.r_set(key, randint(0, 10_000))
		non_exist: tuple = tuple({SmokeTests.get_random_string(length=randint(1, 3)) for _ in range(randint(5, 10))})
		res: list = list(SmokeTests.r.r_mass_check_keys_exists({*keys, *non_exist}))

		keys.sort()
		res.sort()

		self.assertEqual(res, keys, f'len(res) = {len(res)}; len(keys) = {len(keys)}')

	def test_r_mass_check_keys_exists_002(self):
		keys: list = list({SmokeTests.get_random_string(length=randint(10, 20)) for _ in range(randint(50, 100))})
		for key in keys:
			SmokeTests.r.r_set(key, SmokeTests.get_random_string(length=randint(1, 100)))
		non_exist: tuple = tuple({SmokeTests.get_random_string(length=randint(3, 5)) for _ in range(randint(10, 25))})
		res: list = list(SmokeTests.r.r_mass_check_keys_exists({*keys, *non_exist}))

		keys.sort()
		res.sort()

		self.assertEqual(res, keys, f'len(res) = {len(res)}; len(keys) = {len(keys)}')

	# remove all keys ##################################################################################################

	def test_r_remove_all_keys_001(self):
		self.assertIsNone(SmokeTests.r.r_remove_all_keys())
		key_count: int = randint(100, 250)
		for key in range(key_count):
			SmokeTests.r.r_set(str(key), key)
		res = SmokeTests.r.r_remove_all_keys(get_count_keys=True)
		self.assertEqual(res, key_count)
		self.assertIsNone(SmokeTests.r.r_remove_all_keys())


if __name__ == '__main__':
	from redis import Redis, ConnectionPool
	_redis = Redis(connection_pool=ConnectionPool(host=redis_host,port=redis_port,db=0,password=redis_psw))
	_redis.flushall()

	unittest.main()
