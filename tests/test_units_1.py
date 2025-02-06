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
redis_db: int = int(getenv('REDIS_DB') or 0)
redis_host: str = getenv('REDIS_HOST') or 'localhost'
redis_port: int = int(getenv('REDIS_PORT') or 6379)
redis_username: str = getenv('REDIS_USERNAME') or 'default'


class SmokeTests(unittest.TestCase):
	"""
	Required "quick" tests to check the functionality of the main library functions
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

		# rewrite (with 'get_old_value' param)
		value_2: int = SmokeTests.get_random_integer()
		self.assertEqual(SmokeTests.r.r_set(key, value_2, get_old_value=True, convert_to_type_for_get='int'), value_1)
		res_2 = SmokeTests.r.r_get(key)
		self.assertEqual(int(res_2), value_2)

	def test_set_get_int_003(self):  # convert_to_type
		key: str = 'set_get_int_003'
		value: int = SmokeTests.get_random_integer()
		self.assertIsNone(SmokeTests.r.r_set(key, value))
		res = SmokeTests.r.r_get(key, convert_to_type='int')
		self.assertEqual(res, value)

	def test_set_get_int_004(self):  # convert_to_type
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

	def test_set_get_float_003(self):  # convert_to_type
		key: str = 'set_get_float_003'
		value: float = float(SmokeTests.get_random_integer())
		self.assertIsNone(SmokeTests.r.r_set(key, value))
		res = SmokeTests.r.r_get(key, convert_to_type='float')
		self.assertEqual(res, value)

	def test_set_get_float_004(self):  # convert_to_type
		key: str = 'set_get_float_004'
		value: float = float(SmokeTests.get_random_integer())
		self.assertIsNone(SmokeTests.r.r_set(key, value))
		res = SmokeTests.r.r_get(key, convert_to_type='double')
		self.assertEqual(res, value)

	def test_set_get_float_005(self):  # convert_to_type
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

	def test_set_get_bool_001(self):  # convert_to_type
		key: str = 'set_get_bool_001'
		value: bool = True
		self.assertIsNone(SmokeTests.r.r_set(key, value))
		res = SmokeTests.r.r_get(key, convert_to_type='bool')
		self.assertEqual(res, value)

	def test_set_get_bool_002(self):  # convert_to_type
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

	def test_set_get_bool_005(self):  # convert_to_type
		key: str = 'set_get_bool_005'
		value: bool = True
		self.assertIsNone(SmokeTests.r.r_set(key, value))
		res = SmokeTests.r.r_get(key)
		self.assertEqual(res, str(value))

	def test_set_get_bool_006(self):  # convert_to_type
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

	def test_set_get_list_004(self):  # convert_to_type
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

	def test_set_get_tuple_003(self):  # convert_to_type
		key: str = 'set_get_tuple_003'
		value: tuple = tuple(SmokeTests.get_random_string() for _ in range(randint(10, 50)))
		self.assertIsNone(SmokeTests.r.r_set(key, value))
		res: tuple = tuple(map(str, SmokeTests.r.r_get(key)))
		self.assertEqual(res, value)

	def test_set_get_tuple_004(self):  # convert_to_type
		key: str = 'set_get_tuple_004'
		value: tuple = tuple(SmokeTests.get_random_integer() for _ in range(randint(10, 50)))
		self.assertIsNone(SmokeTests.r.r_set(key, value))
		res: tuple = tuple(SmokeTests.r.r_get(key, convert_to_type='int'))
		self.assertEqual(res, value)

	def test_set_get_tuple_005(self):  # convert_to_type
		key: str = 'set_get_tuple_005'
		value: tuple = tuple(float(SmokeTests.get_random_integer()) for _ in range(randint(10, 25)))
		self.assertIsNone(SmokeTests.r.r_set(key, value))
		res: tuple = tuple(SmokeTests.r.r_get(key, convert_to_type='float'))
		self.assertEqual(res, value)

	def test_set_get_tuple_006(self):  # convert_to_type
		key: str = 'set_get_tuple_006'
		value_1: tuple = tuple(bool(randint(0, 1)) for _ in range(randint(25, 50)))
		self.assertIsNone(SmokeTests.r.r_set(key, value_1))
		res_1: tuple = tuple(SmokeTests.r.r_get(key, convert_to_type='bool'))
		self.assertEqual(res_1, value_1)

		# rewrite (integer) (with 'get_old_value' param)
		value_2: int = SmokeTests.get_random_integer()
		self.assertEqual(
			tuple(SmokeTests.r.r_set(key, value_2, get_old_value=True, convert_to_type_for_get='bool')), value_1
		)
		res_2: int = SmokeTests.r.r_get(key, convert_to_type='integer')
		self.assertEqual(res_2, value_2)

		# rewrite (str)
		value_3: str = SmokeTests.get_random_string()
		self.assertIsNone(SmokeTests.r.r_set(key, value_3))
		res_3: str = SmokeTests.r.r_get(key)
		self.assertEqual(res_3, value_3)

	def test_set_get_set_001(self):
		key: str = 'set_get_set_001'
		value: set = set(SmokeTests.get_random_integer() for _ in range(randint(1, 25)))
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

	def test_set_get_set_003(self):  # convert_to_type
		key: str = 'set_get_set_003'
		value: set = set(SmokeTests.get_random_string() for _ in range(randint(1, 10))).union(
			set(SmokeTests.get_random_integer() for _ in range(randint(1, 10)))
		)
		self.assertIsNone(SmokeTests.r.r_set(key, value))
		res: set = set(SmokeTests.r.r_get(key, convert_to_type='int'))
		self.assertEqual(res, value)

	def test_set_get_set_004(self):  # convert_to_type
		key: str = 'set_get_set_004'
		value: set = set(SmokeTests.get_random_integer() for _ in range(randint(25, 50)))
		self.assertIsNone(SmokeTests.r.r_set(key, value))
		res: set = set(SmokeTests.r.r_get(key, convert_to_type='int'))
		self.assertEqual(value, res)

	def test_set_get_set_005(self):
		key: str = 'set_get_set_005'
		value: set = set(SmokeTests.get_random_string() for _ in range(randint(25, 50)))
		self.assertIsNone(SmokeTests.r.r_set(key, value))
		res: set = set(SmokeTests.r.r_get(key))
		self.assertEqual(value, res)

	def test_set_get_set_006(self):  # convert_to_type
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

	def test_set_get_frozenset_002(self):  # convert_to_type
		key: str = 'set_get_frozenset_002'
		value: frozenset = frozenset(SmokeTests.get_random_integer() for _ in range(randint(25, 50)))
		self.assertIsNone(SmokeTests.r.r_set(key, value))
		res: frozenset = frozenset(SmokeTests.r.r_get(key, convert_to_type='integer'))
		self.assertEqual(value, res)

	def test_set_get_frozenset_003(self):  # convert_to_type
		key: str = 'set_get_frozenset_003'
		value: frozenset = frozenset(float(SmokeTests.get_random_integer()) for _ in range(randint(25, 50)))
		self.assertIsNone(SmokeTests.r.r_set(key, value))
		res: frozenset = frozenset(SmokeTests.r.r_get(key, convert_to_type='numeric'))
		self.assertEqual(value, res)

	def test_set_get_frozenset_004(self):  # convert_to_type
		key: str = 'set_get_frozenset_004'
		value_1: frozenset = frozenset(SmokeTests.get_random_integer() for _ in range(randint(25, 50)))
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

	def test_set_get_delete_int_002(self):
		key: str = 'set_get_delete_int_002'
		value: int = SmokeTests.get_random_integer()

		self.assertIsNone(SmokeTests.r.r_set(key, value))
		res_1 = SmokeTests.r.r_get(key)
		self.assertEqual(int(res_1), value)

		# delete (without returning - False)
		self.assertIsNone(SmokeTests.r.r_delete(key, returning=False))
		self.assertIsNone(SmokeTests.r.r_get(key))

	def test_set_get_delete_int_003(self):
		key: str = 'set_get_delete_int_003'
		value: int = SmokeTests.get_random_integer()

		self.assertIsNone(SmokeTests.r.r_set(key, value))
		res_1 = SmokeTests.r.r_get(key)
		self.assertEqual(res_1, str(value))

		# delete (with returning)
		self.assertEqual(SmokeTests.r.r_delete(key, returning=True), str(value))
		self.assertIsNone(SmokeTests.r.r_get(key))

	def test_set_get_delete_str_001(self):
		key: str = 'set_get_delete_str_001'
		value: str = SmokeTests.get_random_string()

		self.assertIsNone(SmokeTests.r.r_set(key, value))
		res_1 = SmokeTests.r.r_get(key)
		self.assertEqual(res_1, value)

		# delete (without returning - False)
		self.assertIsNone(SmokeTests.r.r_delete(key, returning=False))
		self.assertIsNone(SmokeTests.r.r_get(key))

	def test_set_get_delete_str_002(self):
		key: str = 'set_get_delete_str_002'
		value: str = SmokeTests.get_random_string()

		self.assertIsNone(SmokeTests.r.r_set(key, value))
		res_1 = SmokeTests.r.r_get(key)
		self.assertEqual(res_1, value)

		# delete (with returning)
		self.assertEqual(SmokeTests.r.r_delete(key, returning=True), value)
		self.assertIsNone(SmokeTests.r.r_get(key))

	def test_set_get_delete_convert_001(self):
		key: str = 'set_get_delete_convert_001'
		value: int = SmokeTests.get_random_integer()

		self.assertIsNone(SmokeTests.r.r_set(key, value))
		res_1 = SmokeTests.r.r_get(key, convert_to_type='int')
		self.assertEqual(res_1, value)

		res_2 = SmokeTests.r.r_get(key, convert_to_type='float')
		self.assertEqual(res_2, float(value))

		# delete (with returning)
		return_value = SmokeTests.r.r_delete(key, returning=True, convert_to_type_for_return='float')
		self.assertEqual(return_value, float(value))
		self.assertIsNone(SmokeTests.r.r_get(key))

	def test_set_get_delete_convert_002(self):
		key: str = 'set_get_delete_convert_002'
		value: float = float(SmokeTests.get_random_integer())

		self.assertIsNone(SmokeTests.r.r_set(key, value))
		res_1 = SmokeTests.r.r_get(key, convert_to_type='int')
		self.assertEqual(res_1, int(value))

		res_2 = SmokeTests.r.r_get(key, convert_to_type='float')
		self.assertEqual(res_2, value)

		# delete (with returning)
		return_value = SmokeTests.r.r_delete(key, returning=True, convert_to_type_for_return='float')
		self.assertEqual(return_value, value)
		self.assertIsNone(SmokeTests.r.r_get(key))

	def test_set_get_delete_convert_003(self):
		""" use convert to type without returning """
		key: str = 'set_get_delete_convert_003'
		value: list[int] = [1, 2, 3, 4, 5]

		self.assertIsNone(SmokeTests.r.r_set(key, value))
		res_1 = SmokeTests.r.r_get(key, convert_to_type='int')
		self.assertEqual(res_1, value)

		# delete (without returning)
		self.assertIsNone(SmokeTests.r.r_delete(key, convert_to_type_for_return='int'))

	def test_cycle_set_get_delete_001(self):
		for value, key in enumerate([i for i in range(100_000_000, 100_000_000 + randint(25, 50))]):
			key = str(key)
			str_value = str(value)
			self.assertIsNone(SmokeTests.r.r_set(key, value))
			self.assertEqual(SmokeTests.r.r_get(key), str_value)
			self.assertEqual(SmokeTests.r.r_delete(key, returning=True), str_value)
			self.assertIsNone(SmokeTests.r.r_get(key))

	# rename ###########################################################################################################

	def test_rename_key_001(self):
		""" Lua - string """
		key: str = SmokeTests.get_random_string()
		new_key: str = SmokeTests.get_random_string()
		value: str = SmokeTests.get_random_string()
		self.assertIsNone(self.r.r_set(key, value))
		self.assertEqual(self.r.r_get(key), value)
		self.r.rename_key(key, new_key)
		self.assertIsNone(self.r.r_get(key))
		self.assertEqual(self.r.r_get(new_key), value)

	def test_rename_key_002(self):
		""" Lua - boolean """
		key: str = SmokeTests.get_random_string()
		new_key: str = SmokeTests.get_random_string()
		value: bool = True if SmokeTests.get_random_integer() % 2 == 0 else False
		self.assertIsNone(self.r.r_set(key, value))
		self.assertEqual(self.r.r_get(key, convert_to_type='bool'), value)
		self.r.rename_key(key, new_key)
		self.assertIsNone(self.r.r_get(key))
		self.assertEqual(self.r.r_get(new_key, convert_to_type='bool'), value)

	def test_rename_key_003(self):
		""" Lua - integer """
		key: str = SmokeTests.get_random_string()
		new_key: str = SmokeTests.get_random_string()
		value: int = SmokeTests.get_random_integer()
		self.assertIsNone(self.r.r_set(key, value))
		self.assertEqual(self.r.r_get(key, convert_to_type='int'), value)
		self.r.rename_key(key, new_key)
		self.assertIsNone(self.r.r_get(key))
		self.assertEqual(self.r.r_get(new_key, convert_to_type='int'), value)

	def test_rename_key_004(self):
		""" Lua - float """
		key: str = SmokeTests.get_random_string()
		new_key: str = SmokeTests.get_random_string()
		value: float = float(SmokeTests.get_random_integer()) + random()
		self.assertIsNone(self.r.r_set(key, value))
		self.assertEqual(self.r.r_get(key, convert_to_type='float'), value)
		self.r.rename_key(key, new_key)
		self.assertIsNone(self.r.r_get(key))
		self.assertEqual(self.r.r_get(new_key, convert_to_type='float'), value)

	def test_rename_key_005(self):
		""" Lua - list """
		key: str = SmokeTests.get_random_string()
		new_key: str = SmokeTests.get_random_string()
		value: list[int] = [SmokeTests.get_random_integer() for _ in range(randint(10, 20))]
		self.assertIsNone(self.r.r_set(key, value))
		self.assertEqual(self.r.r_get(key, convert_to_type='int'), value)
		self.r.rename_key(key, new_key)
		self.assertIsNone(self.r.r_get(key))
		self.assertEqual(self.r.r_get(new_key, convert_to_type='int'), value)

	def test_rename_key_006(self):
		""" Lua - tuple """
		key: str = SmokeTests.get_random_string()
		new_key: str = SmokeTests.get_random_string()
		value: tuple = tuple(float(SmokeTests.get_random_integer()) + random() for _ in range(randint(10, 20)))
		self.assertIsNone(self.r.r_set(key, value))
		self.assertEqual(tuple(self.r.r_get(key, convert_to_type='float')), value)
		self.r.rename_key(key, new_key)
		self.assertIsNone(self.r.r_get(key))
		self.assertEqual(tuple(self.r.r_get(new_key, convert_to_type='float')), value)

	def test_rename_key_007(self):
		""" Lua - set """
		key: str = SmokeTests.get_random_string()
		new_key: str = SmokeTests.get_random_string()
		value: set = {SmokeTests.get_random_integer() for _ in range(randint(5, 10))}
		self.assertIsNone(self.r.r_set(key, value))
		self.assertEqual(set(self.r.r_get(key, convert_to_type='int')), value)
		self.r.rename_key(key, new_key)
		self.assertIsNone(self.r.r_get(key))
		self.assertEqual(set(self.r.r_get(new_key, convert_to_type='int')), value)

	def test_rename_key_008(self):
		""" Lua - frozenset """
		key: str = SmokeTests.get_random_string()
		new_key: str = SmokeTests.get_random_string()
		value: frozenset = frozenset(SmokeTests.get_random_string() for _ in range(randint(5, 10)))
		self.assertIsNone(self.r.r_set(key, value))
		self.assertEqual(frozenset(self.r.r_get(key)), value)
		self.r.rename_key(key, new_key)
		self.assertIsNone(self.r.r_get(key))
		self.assertEqual(frozenset(self.r.r_get(new_key)), value)

	# mass check keys ##################################################################################################

	def test_r_mass_check_keys_exists_001(self):
		keys: set = {SmokeTests.get_random_string(length=randint(5, 15)) for _ in range(randint(25, 50))}
		for key in keys:
			SmokeTests.r.r_set(key, randint(0, 10_000))
		non_exist: set = {SmokeTests.get_random_string(length=randint(1, 3)) for _ in range(randint(5, 10))}
		res: tuple = SmokeTests.r.r_mass_check_keys_exists(keys.union(non_exist))

		self.assertTrue(set(res) == set(keys), f'len(res) = {len(res)}; len(keys) = {len(keys)}')

	def test_r_mass_check_keys_exists_002(self):
		keys: set = {SmokeTests.get_random_string(length=randint(10, 20)) for _ in range(randint(25, 50))}
		for key in keys:
			SmokeTests.r.r_set(key, SmokeTests.get_random_string(length=randint(1, 100)))
		non_exist: set = {SmokeTests.get_random_string(length=randint(3, 5)) for _ in range(randint(5, 20))}
		res: tuple = SmokeTests.r.r_mass_check_keys_exists(keys.union(non_exist))

		self.assertTrue(set(res) == set(keys), f'len(res) = {len(res)}; len(keys) = {len(keys)}')

	# remove all keys ##################################################################################################

	def test_r_remove_all_keys_001(self):
		""" Lua """
		self.assertIsNone(SmokeTests.r.r_remove_all_keys())
		key_count: int = randint(100, 250)
		for key in range(key_count):
			SmokeTests.r.r_set(str(key), key)
		res = SmokeTests.r.r_remove_all_keys(get_count_keys=True)
		self.assertEqual(res, key_count)

	def test_r_remove_all_keys_002(self):
		""" Lua """
		self.assertIsNone(SmokeTests.r.r_remove_all_keys())
		key_count: int = randint(25, 50)
		for key in range(key_count):
			SmokeTests.r.r_set(str(key), [key])
		res = SmokeTests.r.r_remove_all_keys(get_count_keys=True)
		self.assertEqual(res, key_count)

	def test_r_remove_all_keys_003(self):
		""" Lua """
		self.assertIsNone(SmokeTests.r.r_remove_all_keys())
		key_count: int = randint(25, 50)
		for key in range(key_count):
			SmokeTests.r.r_set(str(key), str(key))
		res = SmokeTests.r.r_remove_all_keys(get_count_keys=True)
		self.assertEqual(res, key_count)

	def test_r_remove_all_keys_004(self):
		""" Lua  - integer - without get_count_keys param """
		self.assertIsNone(SmokeTests.r.r_remove_all_keys())
		key_count: int = randint(50, 100)
		for key in range(key_count):
			SmokeTests.r.r_set(str(key), key)
		self.assertIsNone(SmokeTests.r.r_remove_all_keys())

	def test_r_remove_all_keys_005(self):
		""" Lua  - str - without get_count_keys param """
		self.assertIsNone(SmokeTests.r.r_remove_all_keys())
		key_count: int = randint(50, 100)
		for key in range(key_count):
			SmokeTests.r.r_set(str(key), str(key))
		self.assertIsNone(SmokeTests.r.r_remove_all_keys())

	# check_keys_and_get_values ########################################################################################

	def test_check_keys_and_get_values_001(self):
		""" key is integer """
		self.assertIsNone(SmokeTests.r.r_remove_all_keys())
		exists_keys: tuple = tuple([i for i in range(randint(50, 100)) if i % randint(2, 5) == 0])
		for key in exists_keys:
			SmokeTests.r.r_set(str(key), key)
		res: dict = SmokeTests.r.check_keys_and_get_values(exists_keys)
		self.assertEqual(sorted(res.keys()), sorted(exists_keys))

	def test_check_keys_and_get_values_002(self):
		""" key is string """
		self.assertIsNone(SmokeTests.r.r_remove_all_keys())
		exists_keys: tuple = tuple([str(i) for i in range(randint(50, 100)) if i % randint(2, 5) == 0])
		for key in exists_keys:
			SmokeTests.r.r_set(key, key)
		res: dict = SmokeTests.r.check_keys_and_get_values(exists_keys)
		self.assertEqual(sorted(res.keys()), sorted(exists_keys))

	def test_check_keys_and_get_values_003(self):
		""" check each key - value """
		self.assertIsNone(SmokeTests.r.r_remove_all_keys())
		exists_keys: tuple = tuple([i for i in range(randint(50, 100)) if i % randint(2, 5) == 0])
		for key in exists_keys:
			SmokeTests.r.r_set(str(key), key)
		res: dict = SmokeTests.r.check_keys_and_get_values(exists_keys)
		self.assertEqual(sorted(res.keys()), sorted(exists_keys))
		for key in res.keys():
			self.assertEqual(str(key), res[key])

	# r_mass_delete ####################################################################################################

	def test_r_mass_delete_001(self):
		self.assertIsNone(SmokeTests.r.r_remove_all_keys())
		keys: tuple = tuple([i for i in range(randint(50, 100))])
		for key in keys:
			SmokeTests.r.r_set(str(key), key)
		res = SmokeTests.r.r_mass_delete(keys)
		self.assertEqual(res,  ((), (), dict()))

	def test_r_mass_delete_002(self):
		""" Don't write down all the keys """
		self.assertIsNone(SmokeTests.r.r_remove_all_keys())
		keys: tuple = tuple([str(i) for i in range(randint(50, 100))])
		for str_key in keys[:randint(5, 10)]:
			SmokeTests.r.r_set(str_key, str_key)
		res = SmokeTests.r.r_mass_delete(keys)
		self.assertEqual(res,  ((), (), dict()))

	def test_r_mass_delete_003(self):
		""" Don't write down all the keys """
		self.assertIsNone(SmokeTests.r.r_remove_all_keys())
		keys: tuple = tuple([str(i) for i in range(randint(50, 100))])
		for str_key in keys[:len(keys)//2]:
			SmokeTests.r.r_set(str_key, str_key)
		res = SmokeTests.r.r_mass_delete(keys, return_non_exists=True)
		self.assertTrue(isinstance(res, tuple))
		self.assertEqual(res[0], ())
		self.assertEqual(sorted(res[1]),  sorted(keys[len(keys)//2:]))
		self.assertEqual(res[2], dict())

	def test_r_mass_delete_004(self):
		""" Don't write down all the keys """
		self.assertIsNone(SmokeTests.r.r_remove_all_keys())
		keys: tuple = tuple([i for i in range(randint(50, 100))])
		exists_keys: tuple = keys[:len(keys) // randint(2, 5)]
		for key in exists_keys:
			SmokeTests.r.r_set(str(key), key)
		res = SmokeTests.r.r_mass_delete(keys, return_exists=True)
		self.assertTrue(isinstance(res, tuple))
		self.assertEqual(sorted(res[0]), sorted(exists_keys))
		self.assertEqual(res[1], ())
		self.assertEqual(res[2], dict())

	def test_r_mass_delete_005(self):
		""" Don't write down all the keys """
		self.assertIsNone(SmokeTests.r.r_remove_all_keys())
		keys: tuple = tuple([i for i in range(randint(50, 100))])
		_slice: int = randint(2, 5)
		exists_keys: tuple = keys[:len(keys) // _slice]
		key_value: dict = {key: SmokeTests.get_random_string() for key in exists_keys}
		for key, value in key_value.items():
			SmokeTests.r.r_set(str(key), value)

		res = SmokeTests.r.r_mass_delete(
			keys, return_exists=True, return_non_exists=True, get_dict_key_value_exists=True
		)

		self.assertTrue(isinstance(res, tuple))
		self.assertEqual(sorted(res[0]), sorted(exists_keys))  # return_exists
		self.assertEqual(sorted(res[1]),  sorted(keys[len(keys)//_slice:]))  # return_non_exists
		self.assertEqual(dict(sorted(res[2].items())), dict(sorted(key_value.items())))  # get_dict_key_value_exists

	def test_r_mass_delete_006(self):
		self.assertIsNone(SmokeTests.r.r_remove_all_keys())
		keys: tuple = tuple([i for i in range(randint(50, 100))])
		key_value: dict = {key: SmokeTests.get_random_string() for key in keys}
		for key, value in key_value.items():
			SmokeTests.r.r_set(str(key), value)

		res = SmokeTests.r.r_mass_delete(
			keys, return_exists=True, return_non_exists=True, get_dict_key_value_exists=True,
		)

		self.assertTrue(isinstance(res, tuple))
		self.assertEqual(sorted(res[0]), sorted(keys))  # return_exists
		self.assertEqual(res[1],  ())  # return_non_exists
		self.assertEqual(dict(sorted(res[2].items())), dict(sorted(key_value.items())))  # get_dict_key_value_exists

	def test_r_mass_delete_007(self):
		""" get key-value with converting type """
		self.assertIsNone(SmokeTests.r.r_remove_all_keys())
		keys: tuple = tuple([i for i in range(randint(50, 100))])
		key_value: dict = {key: SmokeTests.get_random_integer() for key in keys}
		for key, value in key_value.items():
			SmokeTests.r.r_set(str(key), value)

		res = SmokeTests.r.r_mass_delete(keys, get_dict_key_value_exists=True, convert_to_type_dict_key='int')

		self.assertTrue(isinstance(res, tuple))
		self.assertEqual(res[0], ())  # return_exists
		self.assertEqual(res[1], ())  # return_non_exists
		self.assertEqual(dict(sorted(res[2].items())), dict(sorted(key_value.items())))  # get_dict_key_value_exists

	def test_r_mass_delete_008(self):
		""" get key-value with converting type """
		self.assertIsNone(SmokeTests.r.r_remove_all_keys())
		keys: tuple = tuple([i for i in range(randint(50, 100))])
		key_value: dict = {key: bool(randint(0, 1)) for key in keys}
		for key, value in key_value.items():
			SmokeTests.r.r_set(str(key), value)

		res = SmokeTests.r.r_mass_delete(keys, get_dict_key_value_exists=True, convert_to_type_dict_key='boolean')

		self.assertTrue(isinstance(res, tuple))
		self.assertEqual(res[0], ())  # return_exists
		self.assertEqual(res[1], ())  # return_non_exists
		self.assertEqual(dict(sorted(res[2].items())), dict(sorted(key_value.items())))  # get_dict_key_value_exists

	def test_r_mass_delete_009(self):
		""" get key-value with converting type """
		self.assertIsNone(SmokeTests.r.r_remove_all_keys())
		keys: tuple = tuple([i for i in range(randint(50, 100))])
		key_value: dict = {key: bool(randint(0, 1)) for key in keys}
		for key, value in key_value.items():
			SmokeTests.r.r_set(str(key), value)

		res = SmokeTests.r.r_mass_delete(
			keys, return_exists=True, get_dict_key_value_exists=True, convert_to_type_dict_key='bool'
		)

		self.assertTrue(isinstance(res, tuple))
		self.assertEqual(res[0], keys)  # return_exists
		self.assertEqual(res[1], ())  # return_non_exists
		self.assertEqual(dict(sorted(res[2].items())), dict(sorted(key_value.items())))  # get_dict_key_value_exists

	def test_r_mass_delete_010(self):
		""" get key-value with converting type """
		self.assertIsNone(SmokeTests.r.r_remove_all_keys())
		keys: tuple = tuple([i for i in range(randint(50, 100))])
		key_value: dict = {key: randint(0, 1_000) for key in keys}
		for key, value in key_value.items():
			SmokeTests.r.r_set(str(key), value)

		res = SmokeTests.r.r_mass_delete(
			keys, return_exists=True, get_dict_key_value_exists=True, convert_to_type_dict_key='integer'
		)

		self.assertTrue(isinstance(res, tuple))
		self.assertEqual(res[0], keys)  # return_exists
		self.assertEqual(res[1], ())  # return_non_exists
		self.assertEqual(dict(sorted(res[2].items())), dict(sorted(key_value.items())))  # get_dict_key_value_exists

	def test_r_mass_delete_011(self):
		""" get key-value with converting type (integer) and without other params """
		self.assertIsNone(SmokeTests.r.r_remove_all_keys())
		keys: tuple = tuple([i for i in range(randint(50, 100))])
		key_value: dict = {key: randint(0, 1_000) for key in keys}
		for key, value in key_value.items():
			SmokeTests.r.r_set(str(key), value)

		res = SmokeTests.r.r_mass_delete(
			keys, convert_to_type_dict_key='integer'
		)

		self.assertTrue(isinstance(res, tuple))
		self.assertEqual(res[0], ())  # return_exists
		self.assertEqual(res[1], ())  # return_non_exists
		self.assertEqual(res[2], dict())  # get_dict_key_value_exists

	def test_r_mass_delete_012(self):
		""" get key-value with converting type (boolean) and without other params """
		self.assertIsNone(SmokeTests.r.r_remove_all_keys())
		keys: tuple = tuple([i for i in range(randint(50, 100))])
		key_value: dict = {key: randint(0, 1_000) for key in keys}
		for key, value in key_value.items():
			SmokeTests.r.r_set(str(key), value)

		res = SmokeTests.r.r_mass_delete(
			keys, convert_to_type_dict_key='boolean'
		)

		self.assertTrue(isinstance(res, tuple))
		self.assertEqual(res[0], ())  # return_exists
		self.assertEqual(res[1], ())  # return_non_exists
		self.assertEqual(res[2], dict())  # get_dict_key_value_exists


if __name__ == '__main__':
	from redis import Redis, ConnectionPool
	_redis = Redis(connection_pool=ConnectionPool(
		host=redis_host, port=redis_port,db=0, password=redis_psw, username=redis_username
	))
	_redis.flushall()  # clear the database before tests

	unittest.main()
