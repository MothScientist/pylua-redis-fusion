import unittest
from redis import Redis, ConnectionPool
from random import randint, choice, random
from string import ascii_letters, digits
from sys import path as sys_path

from connection_params import REDIS_PWS, REDIS_HOST, REDIS_PORT, REDIS_USERNAME
sys_path.append('../')
from pyluaredis.client import PyRedis

redis_db: int = 0


class SmokeTests(unittest.TestCase):
	"""
	Required "quick" tests to check the functionality of the main library functions
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

	@classmethod
	def setUpClass(cls):
		SmokeTests.original_redis.flushdb()  # clear the database before tests

	@classmethod
	def tearDownClass(cls):
		SmokeTests.original_redis.flushdb()  # clear the database after tests

	@staticmethod
	def get_random_integer():
		return randint(0, 1_000_000)

	@staticmethod
	def get_random_string(length: int = randint(10, 20)):
		return ''.join(choice(ascii_letters + digits) for _ in range(length))

	def test_ping_001(self):
		""" Service is available """
		self.assertTrue(SmokeTests.r.r_ping())

	def test_ping_002(self):
		wrong_r = PyRedis(host='unknown')
		self.assertFalse(wrong_r.r_ping())

	# keys_is_exists #####################################################################################################

	def test_keys_is_exists_int_001(self):
		key: str = self.test_keys_is_exists_int_001.__name__
		value: int = SmokeTests.get_random_integer()
		SmokeTests.r.r_set(key, value)
		self.assertTrue(SmokeTests.r.keys_is_exists(key))

	def test_keys_is_exists_int_002(self):
		key: str = self.test_keys_is_exists_int_002.__name__
		self.assertFalse(SmokeTests.r.keys_is_exists(key))

	def test_keys_is_exists_int_003(self):
		key: str = self.test_keys_is_exists_int_003.__name__
		value: int = 0
		SmokeTests.r.r_set(key, value)
		self.assertTrue(SmokeTests.r.keys_is_exists(key))

	def test_keys_is_exists_float_001(self):
		key: str = self.test_keys_is_exists_float_001.__name__
		value: float = random()
		SmokeTests.r.r_set(key, value)
		self.assertTrue(SmokeTests.r.keys_is_exists(key))

	def test_keys_is_exists_float_002(self):
		key: str = self.test_keys_is_exists_float_002.__name__
		value: float = float(SmokeTests.get_random_integer())
		SmokeTests.r.r_set(key, value)
		self.assertTrue(SmokeTests.r.keys_is_exists(key))

	def test_keys_is_exists_float_003(self):
		key: str = self.test_keys_is_exists_float_003.__name__
		self.assertFalse(SmokeTests.r.keys_is_exists(key))

	def test_keys_is_exists_float_004(self):
		key: str = self.test_keys_is_exists_float_004.__name__
		value: float = 0.0
		SmokeTests.r.r_set(key, value)
		self.assertTrue(SmokeTests.r.keys_is_exists(key))

	def test_keys_is_exists_str_001(self):
		key: str = self.test_keys_is_exists_str_001.__name__
		value: str = SmokeTests.get_random_string()
		SmokeTests.r.r_set(key, value)
		self.assertTrue(SmokeTests.r.keys_is_exists(key))

	def test_keys_is_exists_str_002(self):
		key: str = self.test_keys_is_exists_str_002.__name__
		self.assertFalse(SmokeTests.r.keys_is_exists(key))

	def test_keys_is_exists_bool_001(self):
		key: str = self.test_keys_is_exists_bool_001.__name__
		SmokeTests.r.r_set(key, True)
		self.assertTrue(SmokeTests.r.keys_is_exists(key))

	def test_keys_is_exists_bool_002(self):
		key: str = self.test_keys_is_exists_bool_002.__name__
		SmokeTests.r.r_set(key, False)
		self.assertTrue(SmokeTests.r.keys_is_exists(key))

	def test_keys_is_exists_bool_003(self):
		key: str = self.test_keys_is_exists_bool_003.__name__
		self.assertFalse(SmokeTests.r.keys_is_exists(key))

	def test_keys_is_exists_none_001(self):
		key: str = self.test_keys_is_exists_none_001.__name__
		SmokeTests.r.r_set(key, None)
		self.assertFalse(SmokeTests.r.keys_is_exists(key))

	def test_keys_is_exists_list_001(self):
		key: str = self.test_keys_is_exists_list_001.__name__
		value: list = [SmokeTests.get_random_integer() for _ in range(randint(10, 20))]
		SmokeTests.r.r_set(key, value)
		self.assertTrue(SmokeTests.r.keys_is_exists(key))

	def test_keys_is_exists_list_002(self):
		key: str = self.test_keys_is_exists_list_002.__name__
		SmokeTests.r.r_set(key, [])
		self.assertFalse(SmokeTests.r.keys_is_exists(key))

	def test_keys_is_exists_list_003(self):
		key: str = self.test_keys_is_exists_list_003.__name__
		self.assertFalse(SmokeTests.r.keys_is_exists(key))

	def test_keys_is_exists_list_004(self):
		key: str = self.test_keys_is_exists_list_004.__name__
		value: list = [SmokeTests.get_random_string() for _ in range(randint(10, 20))]
		SmokeTests.r.r_set(key, value)
		self.assertTrue(SmokeTests.r.keys_is_exists(key))

	def test_keys_is_exists_list_005(self):
		key: str = self.test_keys_is_exists_list_005.__name__
		value: list = [random() for _ in range(randint(10, 20))]
		SmokeTests.r.r_set(key, value)
		self.assertTrue(SmokeTests.r.keys_is_exists(key))

	def test_keys_is_exists_list_006(self):
		key: str = self.test_keys_is_exists_list_006.__name__
		value: list = [float(SmokeTests.get_random_integer()) for _ in range(randint(10, 20))]
		SmokeTests.r.r_set(key, value)
		self.assertTrue(SmokeTests.r.keys_is_exists(key))

	def test_keys_is_exists_tuple_001(self):
		key: str = self.test_keys_is_exists_tuple_001.__name__
		value: tuple = tuple([SmokeTests.get_random_string() for _ in range(randint(10, 20))])
		SmokeTests.r.r_set(key, value)
		self.assertTrue(SmokeTests.r.keys_is_exists(key))

	def test_keys_is_exists_tuple_002(self):
		key: str = self.test_keys_is_exists_tuple_002.__name__
		SmokeTests.r.r_set(key, tuple())
		self.assertFalse(SmokeTests.r.keys_is_exists(key))

	def test_keys_is_exists_tuple_003(self):
		key: str = self.test_keys_is_exists_tuple_003.__name__
		self.assertFalse(SmokeTests.r.keys_is_exists(key))

	def test_keys_is_exists_tuple_004(self):
		key: str = self.test_keys_is_exists_tuple_004.__name__
		value: tuple = tuple([bool(randint(0, 1)) for _ in range(randint(10, 20))])
		SmokeTests.r.r_set(key, value)
		self.assertTrue(SmokeTests.r.keys_is_exists(key))

	def test_keys_is_exists_tuple_005(self):
		key: str = self.test_keys_is_exists_tuple_005.__name__
		value: tuple = tuple([SmokeTests.get_random_integer() for _ in range(randint(10, 20))])
		SmokeTests.r.r_set(key, value)
		self.assertTrue(SmokeTests.r.keys_is_exists(key))

	def test_keys_is_exists_tuple_006(self):
		key: str = self.test_keys_is_exists_tuple_006.__name__
		value: tuple = tuple([float(SmokeTests.get_random_integer()) for _ in range(randint(10, 20))])
		SmokeTests.r.r_set(key, value)
		self.assertTrue(SmokeTests.r.keys_is_exists(key))

	def test_keys_is_exists_tuple_007(self):
		key: str = self.test_keys_is_exists_tuple_007.__name__
		value: tuple = tuple([random() for _ in range(randint(10, 20))])
		SmokeTests.r.r_set(key, value)
		self.assertTrue(SmokeTests.r.keys_is_exists(key))

	def test_keys_is_exists_set_001(self):
		key: str = self.test_keys_is_exists_set_001.__name__
		value: set = {SmokeTests.get_random_string() for _ in range(randint(10, 20))}
		SmokeTests.r.r_set(key, value)
		self.assertTrue(SmokeTests.r.keys_is_exists(key))

	def test_keys_is_exists_set_002(self):
		key: str = self.test_keys_is_exists_set_002.__name__
		SmokeTests.r.r_set(key, set())
		self.assertFalse(SmokeTests.r.keys_is_exists(key))

	def test_keys_is_exists_set_003(self):
		key: str = self.test_keys_is_exists_set_003.__name__
		self.assertFalse(SmokeTests.r.keys_is_exists(key))

	def test_keys_is_exists_frozenset_001(self):
		key: str = self.test_keys_is_exists_frozenset_001.__name__
		value: frozenset = frozenset({SmokeTests.get_random_string() for _ in range(randint(10, 20))})
		SmokeTests.r.r_set(key, value)
		self.assertTrue(SmokeTests.r.keys_is_exists(key))

	def test_keys_is_exists_frozenset_002(self):
		key: str = self.test_keys_is_exists_frozenset_002.__name__
		SmokeTests.r.r_set(key, frozenset())
		self.assertFalse(SmokeTests.r.keys_is_exists(key))

	def test_keys_is_exists_frozenset_003(self):
		key: str = self.test_keys_is_exists_frozenset_003.__name__
		self.assertFalse(SmokeTests.r.keys_is_exists(key))
		
	def test_keys_is_exists_001(self):
		SmokeTests.original_redis.flushdb()

		keys: set = {SmokeTests.get_random_string(length=randint(5, 15)) for _ in range(randint(25, 50))}
		for key in keys:
			SmokeTests.r.r_set(key, randint(0, 10_000))
		self.assertEqual(len(keys), SmokeTests.r.keys_is_exists(keys))

		SmokeTests.original_redis.flushdb()

	def test_keys_is_exists_002(self):
		SmokeTests.original_redis.flushdb()

		keys: set = {SmokeTests.get_random_integer() for _ in range(randint(250, 500))}
		for key in keys:
			SmokeTests.r.r_set(str(key), SmokeTests.get_random_string())
		self.assertEqual(len(keys), SmokeTests.r.keys_is_exists(keys))

		SmokeTests.original_redis.flushdb()

	def test_keys_is_exists_003(self):
		""" keys_is_exists without set keys """
		SmokeTests.original_redis.flushdb()

		keys: set = {SmokeTests.get_random_string(length=randint(5, 15)) for _ in range(randint(25, 50))}
		self.assertEqual(SmokeTests.r.keys_is_exists(keys), 0)

		SmokeTests.original_redis.flushdb()

	# append_value_to_array ############################################################################################

	def test_append_value_to_array_001(self):
		""" List """
		key: str = self.test_append_value_to_array_001.__name__
		value: list = [1, 2, 3, 4, 5]
		SmokeTests.r.r_set(key, value)
		SmokeTests.r.append_value_to_array(key, 0, index=0)
		res: list[int] = SmokeTests.r.r_get(key, convert_to_type='int')
		self.assertEqual(res, [0, 1, 2, 3, 4, 5])

	def test_append_value_to_array_002(self):
		""" List """
		key: str = self.test_append_value_to_array_002.__name__
		value: list = [0, 1, 2, 3, 4]
		SmokeTests.r.r_set(key, value)
		SmokeTests.r.append_value_to_array(key, 5, index=-1)
		res: list[int] = SmokeTests.r.r_get(key, convert_to_type='int')
		self.assertEqual(res, [0, 1, 2, 3, 4, 5])

	def test_append_value_to_array_003(self):
		""" List """
		key: str = self.test_append_value_to_array_003.__name__
		value: list = [0, 1, 2]
		SmokeTests.r.r_set(key, value)
		SmokeTests.r.append_value_to_array(key, 3)
		res: list[int] = SmokeTests.r.r_get(key, convert_to_type='int')
		self.assertEqual(res, [0, 1, 2, 3])

	def test_append_value_to_array_004(self):
		""" List """
		key: str = self.test_append_value_to_array_004.__name__
		value: list = [0, 1, 2, 4, 5]
		SmokeTests.r.r_set(key, value)
		SmokeTests.r.append_value_to_array(key, 3, index=3)
		res: list[int] = SmokeTests.r.r_get(key, convert_to_type='int')
		self.assertEqual(res, [0, 1, 2, 3, 4, 5])

	def test_append_value_to_array_005(self):
		""" List """
		key: str = self.test_append_value_to_array_005.__name__
		value: list = list(range(10))
		SmokeTests.r.r_set(key, value)
		SmokeTests.r.append_value_to_array(key, randint(0, 100), index=randint(1, 9))
		res: list = SmokeTests.r.r_get(key)
		self.assertTrue(len(res) == len(value) + 1)

	def test_append_value_to_array_006(self):
		""" Set """
		key: str = self.test_append_value_to_array_006.__name__
		value: set = set(range(10))
		SmokeTests.r.r_set(key, value)
		SmokeTests.r.append_value_to_array(key, randint(50, 100))  # the new value must not overlap with existing ones
		res: set = SmokeTests.r.r_get(key)
		self.assertTrue(len(res) == len(value) + 1)

	def test_append_value_to_array_007(self):
		""" Set """
		key: str = self.test_append_value_to_array_007.__name__
		value: set = set(randint(0, 10_000) for _ in range(0, 25))
		SmokeTests.r.r_set(key, value)
		new_value: int = randint(100_000, 1_000_000)
		SmokeTests.r.append_value_to_array(key, new_value)
		res: set = SmokeTests.r.r_get(key, convert_to_type='int')
		self.assertEqual(value.union({new_value}), res)

	def test_append_value_to_array_008(self):
		""" test_append_value_to_array: get_old_value - #1 """
		key: str = self.test_append_value_to_array_008.__name__
		value: list[int] = [0, 1, 2]
		new_value: int = 3
		SmokeTests.r.r_set(key, value)

		old_value: list[int] = SmokeTests.r.append_value_to_array(key, 3, get_old_value=True, convert_to_type='int')
		self.assertEqual(old_value, value)

		res: list[int] = SmokeTests.r.r_get(key, convert_to_type='integer')
		self.assertEqual(res, (value + [new_value]))

	def test_append_value_to_array_009(self):
		""" test_append_value_to_array: get_old_value - #2 """
		key: str = self.test_append_value_to_array_009.__name__
		value: list[int] = [9, 8, 6, 5, 4, 3, 2, 1, 0]
		SmokeTests.r.r_set(key, value)

		old_value: list[int] = SmokeTests.r.append_value_to_array(
			key, 7, index=2, get_old_value=True, convert_to_type='int'
		)
		self.assertEqual(old_value, value)

		res: list[int] = SmokeTests.r.r_get(key, convert_to_type='integer')
		self.assertEqual(res, [9, 8, 7, 6, 5, 4, 3, 2, 1, 0])

	def test_append_value_to_array_010(self):
		""" test_append_value_to_array: get_old_value - #3 """
		key: str = self.test_append_value_to_array_010.__name__
		value: list[int] = [9, 8, 7, 6, 5, 4, 3, 2, 0]
		SmokeTests.r.r_set(key, value)

		old_value: list[int] = SmokeTests.r.append_value_to_array(
			key, 1, index=len(value)-1, get_old_value=True, convert_to_type='int'
		)
		self.assertEqual(old_value, value)

		res: list[int] = SmokeTests.r.r_get(key, convert_to_type='integer')
		self.assertEqual(res, [9, 8, 7, 6, 5, 4, 3, 2, 1, 0])

	def test_append_value_to_array_011(self):
		key: str = self.test_append_value_to_array_011.__name__
		value: list[str] = ['q', 'qw', 'qwer', 'qwert', 'qwerty']
		SmokeTests.r.r_set(key, value)
		old_value: None = SmokeTests.r.append_value_to_array(key, 'qwe', index=2, get_old_value=False)
		self.assertIsNone(old_value)
		res: list[str] = SmokeTests.r.r_get(key)
		self.assertEqual(res, ['q', 'qw', 'qwe', 'qwer', 'qwert', 'qwerty'])

	def test_append_value_to_array_012(self):
		key: str = self.test_append_value_to_array_012.__name__
		SmokeTests.r.append_value_to_array(key, 0, type_if_not_exists='null')
		self.assertIsNone(SmokeTests.r.r_get(key))

	def test_append_value_to_array_013(self):
		key: str = self.test_append_value_to_array_013.__name__
		SmokeTests.r.append_value_to_array(key, 0, type_if_not_exists='list')
		res = SmokeTests.r.r_get(key, convert_to_type='int')
		self.assertEqual(res, [0])

	def test_append_value_to_array_014(self):
		key: str = self.test_append_value_to_array_014.__name__
		SmokeTests.r.append_value_to_array(key, 'res', type_if_not_exists='set')
		self.assertEqual(SmokeTests.r.r_get(key), {'res'})

	def test_append_value_to_array_015(self):
		key: str = self.test_append_value_to_array_015.__name__
		SmokeTests.r.append_value_to_array(key, '123', type_if_not_exists='qwerty')
		self.assertIsNone(SmokeTests.r.r_get(key))

	def test_append_value_to_array_016(self):
		key: str = self.test_append_value_to_array_016.__name__
		SmokeTests.r.append_value_to_array(key, 987, type_if_not_exists='')
		self.assertIsNone(SmokeTests.r.r_get(key))

	def test_append_value_to_array_017(self):
		key: str = self.test_append_value_to_array_017.__name__
		SmokeTests.r.append_value_to_array(key, 98765, type_if_not_exists='   ')
		self.assertIsNone(SmokeTests.r.r_get(key))

	def test_append_value_to_array_018(self):
		""" index > len """
		key: str = self.test_append_value_to_array_018.__name__
		SmokeTests.r.append_value_to_array(key, 123, index=15, type_if_not_exists='list')
		res = SmokeTests.r.r_get(key, convert_to_type='int')
		self.assertEqual(res, [123])

	# TODO - test_append_value_to_array: type_if_not_exists

	# r_len ############################################################################################################

	def test_r_len_001(self):
		""" List"""
		key: str = self.test_r_len_001.__name__
		lst_len: int = randint(5, 25)
		SmokeTests.r.r_set(key, [key] * lst_len)
		res: int = SmokeTests.r.r_len(key)
		self.assertEqual(res, lst_len)

	def test_r_len_002(self):
		""" Tuple """
		key: str = self.test_r_len_002.__name__
		lst_len: int = randint(5, 25)
		SmokeTests.r.r_set(key, tuple([key] * lst_len))
		res: int = SmokeTests.r.r_len(key)
		self.assertEqual(res, lst_len)

	def test_r_len_003(self):
		""" Set """
		key: str = self.test_r_len_003.__name__
		lst_len: int = randint(5, 25)
		SmokeTests.r.r_set(key, set([i for i in range(lst_len)]))
		res: int = SmokeTests.r.r_len(key)
		self.assertEqual(res, lst_len)

	def test_r_len_004(self):
		""" Frozenset """
		key: str = self.test_r_len_004.__name__
		lst_len: int = randint(5, 25)
		SmokeTests.r.r_set(key, frozenset([i for i in range(lst_len)]))
		res: int = SmokeTests.r.r_len(key)
		self.assertEqual(res, lst_len)

	def test_r_len_005(self):
		key: str = self.test_r_len_005.__name__
		# not a list
		SmokeTests.r.r_set(key, key)
		res: int = SmokeTests.r.r_len(key)
		self.assertEqual(res, 0)

	def test_r_len_006(self):
		key: str = self.test_r_len_006.__name__
		# without set
		res: int = SmokeTests.r.r_len(key)
		self.assertIsNone(res)

	def test_r_len_007(self):
		key: str = self.test_r_len_007.__name__
		SmokeTests.r.r_set(key, {key})
		res: int = SmokeTests.r.r_len(key)
		self.assertEqual(res, 1)

	def test_r_len_008(self):
		key: str = self.test_r_len_008.__name__
		SmokeTests.r.r_set(key, None)
		res: int = SmokeTests.r.r_len(key)
		self.assertEqual(res, None)

	# get_count_of_keys ################################################################################################

	def test_get_count_of_keys_001(self):
		""" get_count_of_keys() == dbsize() """
		original_res: int = SmokeTests.original_redis.dbsize()
		library_res: int = SmokeTests.r.get_count_of_keys()
		self.assertEqual(original_res, library_res)

	def test_get_count_of_keys_002(self):
		SmokeTests.original_redis.flushdb()

		count_of_keys: int = randint(50, 100)
		for i in range(count_of_keys):
			SmokeTests.r.r_set(str(i), i)
		res: int = SmokeTests.r.get_count_of_keys()
		self.assertEqual(count_of_keys, res)

		SmokeTests.original_redis.flushdb()

	# get_type_value_of_key ############################################################################################

	def test_get_type_value_of_key_str_001(self):
		key: str = self.test_get_type_value_of_key_str_001.__name__
		value: str = SmokeTests.get_random_string()
		self.assertIsNone(SmokeTests.r.r_set(key, value))
		self.assertEqual('string', SmokeTests.r.get_type_value_of_key(key))

	def test_get_type_value_of_key_int_001(self):
		key: str = self.test_get_type_value_of_key_int_001.__name__
		value: int = SmokeTests.get_random_integer()
		self.assertIsNone(SmokeTests.r.r_set(key, value))
		self.assertEqual('string', SmokeTests.r.get_type_value_of_key(key))

	def test_get_type_value_of_key_float_001(self):
		""" 0.x """
		key: str = self.test_get_type_value_of_key_float_001.__name__
		value: float = random()
		self.assertIsNone(SmokeTests.r.r_set(key, value))
		self.assertEqual('string', SmokeTests.r.get_type_value_of_key(key))

	def test_get_type_value_of_key_float_002(self):
		""" x.0 """
		key: str = self.test_get_type_value_of_key_float_002.__name__
		value: float = float(SmokeTests.get_random_integer())
		self.assertIsNone(SmokeTests.r.r_set(key, value))
		self.assertEqual('string', SmokeTests.r.get_type_value_of_key(key))

	def test_get_type_value_of_key_float_003(self):
		""" x.x """
		key: str = self.test_get_type_value_of_key_float_003.__name__
		value: float = float(SmokeTests.get_random_integer()) + random()
		self.assertIsNone(SmokeTests.r.r_set(key, value))
		self.assertEqual('string', SmokeTests.r.get_type_value_of_key(key))

	def test_get_type_value_of_key_bool_001(self):
		""" True """
		key: str = self.test_get_type_value_of_key_bool_001.__name__
		value: bool = True
		self.assertIsNone(SmokeTests.r.r_set(key, value))
		self.assertEqual('string', SmokeTests.r.get_type_value_of_key(key))

	def test_get_type_value_of_key_bool_002(self):
		""" False """
		key: str = self.test_get_type_value_of_key_bool_002.__name__
		value: bool = False
		self.assertIsNone(SmokeTests.r.r_set(key, value))
		self.assertEqual('string', SmokeTests.r.get_type_value_of_key(key))

	# set ##############################################################################################################

	def test_set_001(self):
		key: str = ''
		value: int = SmokeTests.get_random_integer()
		self.assertIsNone(SmokeTests.r.r_set(key, value))

	def test_set_002(self):
		key: str = SmokeTests.get_random_string()
		self.assertIsNone(SmokeTests.r.r_set(key, None))

	def test_set_003(self):
		key: str = ''
		self.assertIsNone(SmokeTests.r.r_set(key, None))

	# get ##############################################################################################################

	def test_get_001(self):
		self.assertIsNone(SmokeTests.r.r_get(''))

	def test_get_002(self):
		default_value = 'example_default_value'
		self.assertEqual(default_value, SmokeTests.r.r_get('', default_value=default_value))

	# set/get ##########################################################################################################

	def test_set_get_int_001(self):
		key: str = self.test_set_get_int_001.__name__
		value: int = SmokeTests.get_random_integer()
		self.assertIsNone(SmokeTests.r.r_set(key, value))
		res = SmokeTests.r.r_get(key)
		self.assertEqual(int(res), value)

	def test_set_get_int_002(self):
		""" get_old_value """
		key: str = self.test_set_get_int_002.__name__
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
		key: str = self.test_set_get_int_003.__name__
		value: int = SmokeTests.get_random_integer()
		self.assertIsNone(SmokeTests.r.r_set(key, value))
		res = SmokeTests.r.r_get(key, convert_to_type='int')
		self.assertEqual(res, value)

	def test_set_get_int_004(self):  # convert_to_type
		key: str = self.test_set_get_int_004.__name__
		value: int = SmokeTests.get_random_integer()
		self.assertIsNone(SmokeTests.r.r_set(key, value))
		res = SmokeTests.r.r_get(key, convert_to_type='integer')
		self.assertEqual(res, value)

	def test_set_get_float_001(self):
		key: str = self.test_set_get_float_001.__name__
		value: float = float(SmokeTests.get_random_integer())
		self.assertIsNone(SmokeTests.r.r_set(key, value))
		res = SmokeTests.r.r_get(key)
		self.assertEqual(float(res), value)

	def test_set_get_float_002(self):
		key: str = self.test_set_get_float_002.__name__
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
		key: str = self.test_set_get_float_003.__name__
		value: float = float(SmokeTests.get_random_integer())
		self.assertIsNone(SmokeTests.r.r_set(key, value))
		res = SmokeTests.r.r_get(key, convert_to_type='float')
		self.assertEqual(res, value)

	def test_set_get_float_004(self):  # convert_to_type
		key: str = self.test_set_get_float_004.__name__
		value: float = float(SmokeTests.get_random_integer())
		self.assertIsNone(SmokeTests.r.r_set(key, value))
		res = SmokeTests.r.r_get(key, convert_to_type='double')
		self.assertEqual(res, value)

	def test_set_get_float_005(self):  # convert_to_type
		key: str = self.test_set_get_float_005.__name__
		value: float = float(SmokeTests.get_random_integer())
		self.assertIsNone(SmokeTests.r.r_set(key, value))
		res = SmokeTests.r.r_get(key, convert_to_type='numeric')
		self.assertEqual(res, value)

	def test_set_get_str_001(self):
		key: str = self.test_set_get_str_001.__name__
		value: str = SmokeTests.get_random_string()
		self.assertIsNone(SmokeTests.r.r_set(key, value))
		res = SmokeTests.r.r_get(key)
		self.assertEqual(res, value)

	def test_set_get_str_002(self):
		key: str = self.test_set_get_str_002.__name__
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
		key: str = self.test_set_get_bool_001.__name__
		value: bool = True
		self.assertIsNone(SmokeTests.r.r_set(key, value))
		res = SmokeTests.r.r_get(key, convert_to_type='bool')
		self.assertEqual(res, value)

	def test_set_get_bool_002(self):  # convert_to_type
		key: str = self.test_set_get_bool_002.__name__
		value: bool = False
		self.assertIsNone(SmokeTests.r.r_set(key, value))
		res = SmokeTests.r.r_get(key, convert_to_type='bool')
		self.assertEqual(res, value)

	def test_set_get_bool_003(self):  # convert_to_type
		key: str = self.test_set_get_bool_003.__name__
		value: int = 1
		self.assertIsNone(SmokeTests.r.r_set(key, value))
		res = SmokeTests.r.r_get(key, convert_to_type='bool')
		self.assertEqual(res, bool(value))

	def test_set_get_bool_004(self):  # convert_to_type
		key: str = self.test_set_get_bool_004.__name__
		value: int = 0
		self.assertIsNone(SmokeTests.r.r_set(key, value))
		res = SmokeTests.r.r_get(key, convert_to_type='bool')
		self.assertEqual(res, bool(value))

	def test_set_get_bool_005(self):
		key: str = self.test_set_get_bool_005.__name__
		value: bool = True
		self.assertIsNone(SmokeTests.r.r_set(key, value))
		res = SmokeTests.r.r_get(key)
		self.assertEqual(res, str(value))

	def test_set_get_bool_006(self):
		key: str = self.test_set_get_bool_006.__name__
		value: bool = False
		self.assertIsNone(SmokeTests.r.r_set(key, value))
		res = SmokeTests.r.r_get(key)
		self.assertEqual(res, str(value))

	def test_set_get_list_001(self):
		""" integer """
		key: str = self.test_set_get_list_001.__name__
		value: list[int] = [SmokeTests.get_random_integer() for _ in range(randint(10, 15))]
		self.assertIsNone(SmokeTests.r.r_set(key, value))
		res: list = list(map(int, SmokeTests.r.r_get(key)))
		self.assertEqual(res, value)

	def test_set_get_list_002(self):
		""" integer """
		key: str = self.test_set_get_list_002.__name__
		value_1: list[int] = [SmokeTests.get_random_integer() for _ in range(randint(10, 25))]
		self.assertIsNone(SmokeTests.r.r_set(key, value_1))
		res_1: list = list(map(int, SmokeTests.r.r_get(key)))
		self.assertEqual(res_1, value_1)

		# rewrite
		value_2: list[int] = [SmokeTests.get_random_integer() for _ in range(randint(10, 15))]
		self.assertIsNone(SmokeTests.r.r_set(key, value_2))
		res_2: list = list(map(int, SmokeTests.r.r_get(key)))
		self.assertEqual(res_2, value_2)

	def test_set_get_list_003(self):
		""" string """
		key: str = self.test_set_get_list_003.__name__
		value: list[str] = [SmokeTests.get_random_string() for _ in range(randint(10, 50))]
		self.assertIsNone(SmokeTests.r.r_set(key, value))
		res: list[str] = list(map(str, SmokeTests.r.r_get(key)))
		self.assertEqual(res, value)

	def test_set_get_list_004(self):  # convert_to_type
		""" boolean """
		key: str = self.test_set_get_list_004.__name__
		value: list[bool] = [bool(randint(0, 1)) for _ in range(randint(10, 50))]
		self.assertIsNone(SmokeTests.r.r_set(key, value))
		res: list[bool] = list(SmokeTests.r.r_get(key, convert_to_type='boolean'))
		self.assertEqual(res, value)

	def test_set_get_list_005(self):
		""" float """
		key: str = self.test_set_get_list_005.__name__
		value: list[float] = [random() for _ in range(randint(10, 15))]
		self.assertIsNone(SmokeTests.r.r_set(key, value))
		res: list[float] = list(map(float, SmokeTests.r.r_get(key)))
		self.assertEqual(res, value)

	def test_set_get_list_006(self):
		""" float """
		key: str = self.test_set_get_list_006.__name__
		value: list[float] = [float(SmokeTests.get_random_integer()) for _ in range(randint(10, 15))]
		self.assertIsNone(SmokeTests.r.r_set(key, value))
		res: list[float] = list(map(float, SmokeTests.r.r_get(key)))
		self.assertEqual(res, value)

	def test_set_get_list_007(self):  # convert_to_type
		""" float """
		key: str = self.test_set_get_list_007.__name__
		value: list[float] = [random() for _ in range(randint(10, 15))]
		self.assertIsNone(SmokeTests.r.r_set(key, value))
		res: list[float] = SmokeTests.r.r_get(key, convert_to_type='float')
		self.assertEqual(res, value)

	def test_set_get_list_008(self):  # convert_to_type
		""" float """
		key: str = self.test_set_get_list_008.__name__
		value: list[float] = [float(SmokeTests.get_random_integer()) for _ in range(randint(10, 15))]
		self.assertIsNone(SmokeTests.r.r_set(key, value))
		res: list[float] = SmokeTests.r.r_get(key, convert_to_type='float')
		self.assertEqual(res, value)

	def test_set_get_list_009(self):
		""" boolean """
		key: str = self.test_set_get_list_009.__name__
		value: list[bool] = [bool(randint(0, 1)) for _ in range(randint(10, 50))]
		self.assertIsNone(SmokeTests.r.r_set(key, value))
		res: list[bool] = [True if item in ('1', 'true', 'True') else False for item in SmokeTests.r.r_get(key)]
		self.assertEqual(res, value)

	def test_set_get_list_010(self):
		""" integer + get_old_value + convert_to_type_for_get """
		key: str = self.test_set_get_list_010.__name__
		value_1: list[int] = [SmokeTests.get_random_integer() for _ in range(randint(5, 10))]
		self.assertIsNone(SmokeTests.r.r_set(key, value_1))
		res_1: list[int] = SmokeTests.r.r_get(key, convert_to_type='int')
		self.assertEqual(res_1, value_1)

		# rewrite
		value_2: list[int] = [SmokeTests.get_random_integer() for _ in range(randint(20, 25))]
		old_value = SmokeTests.r.r_set(key, value_2, get_old_value=True, convert_to_type_for_get='integer')
		self.assertEqual(old_value, value_1)
		res_2: list[int] = SmokeTests.r.r_get(key, convert_to_type='integer')
		self.assertEqual(res_2, value_2)

	def test_set_get_list_011(self):
		""" string + get_old_value """
		key: str = self.test_set_get_list_011.__name__
		value_1: list[str] = [SmokeTests.get_random_string() for _ in range(randint(5, 10))]
		self.assertIsNone(SmokeTests.r.r_set(key, value_1))
		res_1: list[str] = SmokeTests.r.r_get(key)
		self.assertEqual(res_1, value_1)

		# rewrite
		value_2: list[str] = [SmokeTests.get_random_string() for _ in range(randint(20, 25))]
		old_value: list[str] = SmokeTests.r.r_set(key, value_2, get_old_value=True)
		self.assertEqual(old_value, value_1)
		res_2: list[str] = SmokeTests.r.r_get(key)
		self.assertEqual(res_2, value_2)

	def test_set_get_tuple_001(self):
		""" integer """
		key: str = self.test_set_get_tuple_001.__name__
		value: tuple[int, ...] = tuple(SmokeTests.get_random_integer() for _ in range(randint(10, 25)))
		self.assertIsNone(SmokeTests.r.r_set(key, value))
		res: tuple[int, ...] = tuple(map(int, SmokeTests.r.r_get(key)))
		self.assertEqual(res, value)

	def test_set_get_tuple_002(self):
		""" integer """
		key: str = self.test_set_get_tuple_002.__name__
		value_1: tuple[int, ...] = tuple(SmokeTests.get_random_integer() for _ in range(randint(10, 25)))
		self.assertIsNone(SmokeTests.r.r_set(key, value_1))
		res_1: tuple[int, ...] = tuple(map(int, SmokeTests.r.r_get(key)))
		self.assertEqual(res_1, value_1)

		# rewrite
		value_2: tuple = tuple(SmokeTests.get_random_integer() for _ in range(randint(10, 15)))
		self.assertIsNone(SmokeTests.r.r_set(key, value_2))
		res_2: tuple = tuple(map(int, SmokeTests.r.r_get(key)))
		self.assertEqual(res_2, value_2)

	def test_set_get_tuple_003(self):  # convert_to_type
		""" string """
		key: str = 'set_get_tuple_003'
		value: tuple[str, ...] = tuple(SmokeTests.get_random_string() for _ in range(randint(10, 50)))
		self.assertIsNone(SmokeTests.r.r_set(key, value))
		res: tuple = tuple(map(str, SmokeTests.r.r_get(key)))
		self.assertEqual(res, value)

	def test_set_get_tuple_004(self):  # convert_to_type
		""" integer """
		key: str = 'set_get_tuple_004'
		value: tuple[int, ...] = tuple(SmokeTests.get_random_integer() for _ in range(randint(10, 50)))
		self.assertIsNone(SmokeTests.r.r_set(key, value))
		res: tuple = tuple(SmokeTests.r.r_get(key, convert_to_type='int'))
		self.assertEqual(res, value)

	def test_set_get_tuple_005(self):  # convert_to_type
		""" float """
		key: str = 'set_get_tuple_005'
		value: tuple[float, ...] = tuple(float(SmokeTests.get_random_integer()) for _ in range(randint(10, 25)))
		self.assertIsNone(SmokeTests.r.r_set(key, value))
		res: tuple = tuple(SmokeTests.r.r_get(key, convert_to_type='float'))
		self.assertEqual(res, value)

	def test_set_get_tuple_006(self):  # convert_to_type
		""" boolean + get_old_value """
		key: str = 'set_get_tuple_006'
		value_1: tuple[bool, ...] = tuple(bool(randint(0, 1)) for _ in range(randint(25, 50)))
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

	def test_set_get_tuple_007(self):
		""" integer + get_old_value + convert_to_type_for_get """
		key: str = 'set_get_tuple_007'
		value_1: tuple[int, ...] = tuple([SmokeTests.get_random_integer() for _ in range(randint(5, 10))])
		self.assertIsNone(SmokeTests.r.r_set(key, value_1))
		res_1: tuple[int, ...] = tuple(SmokeTests.r.r_get(key, convert_to_type='int'))
		self.assertEqual(res_1, value_1)

		# rewrite
		value_2: tuple[int, ...] = tuple([SmokeTests.get_random_integer() for _ in range(randint(20, 25))])
		old_value: tuple[int, ...] = tuple(
			SmokeTests.r.r_set(key, value_2, get_old_value=True, convert_to_type_for_get='integer')
		)
		self.assertEqual(old_value, value_1)
		res_2: tuple[int, ...] = tuple(SmokeTests.r.r_get(key, convert_to_type='integer'))
		self.assertEqual(res_2, value_2)

	def test_set_get_set_001(self):
		key: str = 'set_get_set_001'
		value: set[int] = set(SmokeTests.get_random_integer() for _ in range(randint(1, 25)))
		self.assertIsNone(SmokeTests.r.r_set(key, value))
		res: set = set(map(int, SmokeTests.r.r_get(key)))
		self.assertEqual(res, value)

	def test_set_get_set_002(self):
		key: str = 'set_get_set_002'
		value: set[str] = set(SmokeTests.get_random_string() for _ in range(randint(1, 25))).union(
			set(str(SmokeTests.get_random_integer()) for _ in range(randint(1, 25)))
		)
		self.assertIsNone(SmokeTests.r.r_set(key, value))
		res: set = set(SmokeTests.r.r_get(key))
		self.assertEqual(res, value)

	def test_set_get_set_003(self):  # convert_to_type
		key: str = 'set_get_set_003'
		value: set[str] = set(SmokeTests.get_random_string() for _ in range(randint(1, 10))).union(
			set(SmokeTests.get_random_integer() for _ in range(randint(1, 10)))
		)
		self.assertIsNone(SmokeTests.r.r_set(key, value))
		# Changes convert_to_type option
		res: set[int] = SmokeTests.r.r_get(key, convert_to_type='int_any')  # str -> int = str
		self.assertEqual(res, value)

	def test_set_get_set_004(self):  # convert_to_type
		key: str = 'set_get_set_004'
		value: set[int] = set(SmokeTests.get_random_integer() for _ in range(randint(25, 50)))
		self.assertIsNone(SmokeTests.r.r_set(key, value))
		res: set[int] = SmokeTests.r.r_get(key, convert_to_type='int')
		self.assertEqual(value, res)

	def test_set_get_set_005(self):
		key: str = 'set_get_set_005'
		value: set[str] = set(SmokeTests.get_random_string() for _ in range(randint(25, 50)))
		self.assertIsNone(SmokeTests.r.r_set(key, value))
		res: set[str] = SmokeTests.r.r_get(key)
		self.assertEqual(value, res)

	def test_set_get_set_006(self):  # convert_to_type
		key: str = 'set_get_set_006'
		value: set[str] = set(SmokeTests.get_random_string() for _ in range(randint(25, 50)))
		self.assertIsNone(SmokeTests.r.r_set(key, value))
		res: set[str] = SmokeTests.r.r_get(key, convert_to_type='float')  # str -> float = str
		self.assertEqual(value, res)

	def test_set_get_frozenset_001(self):
		key: str = 'set_get_frozenset_001'
		value: frozenset[str] = frozenset(SmokeTests.get_random_string() for _ in range(randint(5, 10)))
		self.assertIsNone(SmokeTests.r.r_set(key, value))
		res: set[str] = SmokeTests.r.r_get(key)
		self.assertEqual(set(value), res)

	def test_set_get_frozenset_002(self):  # convert_to_type
		key: str = 'set_get_frozenset_002'
		value: frozenset[int] = frozenset(SmokeTests.get_random_integer() for _ in range(randint(25, 50)))
		self.assertIsNone(SmokeTests.r.r_set(key, value))
		res: set[int] = SmokeTests.r.r_get(key, convert_to_type='integer')
		self.assertEqual(set(value), res)

	def test_set_get_frozenset_003(self):  # convert_to_type
		key: str = 'set_get_frozenset_003'
		value: frozenset[float] = frozenset(float(SmokeTests.get_random_integer()) for _ in range(randint(25, 50)))
		self.assertIsNone(SmokeTests.r.r_set(key, value))
		res: set[float] = SmokeTests.r.r_get(key, convert_to_type='numeric')
		self.assertEqual(set(value), res)

	def test_set_get_frozenset_004(self):  # convert_to_type
		key: str = 'set_get_frozenset_004'
		value_1: frozenset[int] = frozenset(SmokeTests.get_random_integer() for _ in range(randint(25, 50)))
		self.assertIsNone(SmokeTests.r.r_set(key, value_1))
		res_1: set[int] = SmokeTests.r.r_get(key, convert_to_type='integer')
		self.assertEqual(set(value_1), res_1, f'len(value_1) = {len(value_1)}; len(res_1) = {len(res_1)}')

		# rewrite
		value_2: frozenset[str] = frozenset(SmokeTests.get_random_string() for _ in range(randint(5, 10)))
		self.assertIsNone(SmokeTests.r.r_set(key, value_2))
		res_2: set[str] = SmokeTests.r.r_get(key)
		self.assertEqual(set(value_2), res_2)

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

	# TODO - get without set

	# delete ###########################################################################################################

	def test_delete_001(self):
		key: str = 'delete_001'
		# doesn't set the value
		# delete
		self.assertIsNone(SmokeTests.r.r_delete(key))

	def test_delete_002(self):
		key: str = 'delete_002'
		# doesn't set the value
		# delete
		self.assertIsNone(SmokeTests.r.r_delete(key, returning=False))

	def test_delete_003(self):
		key: str = 'delete_003'
		# doesn't set the value
		# delete (with returning)
		self.assertIsNone(SmokeTests.r.r_delete(key, returning=True))

	def test_delete_004(self):
		key: str = 'delete_004'
		# doesn't set the value
		# delete (with returning and convert)
		self.assertIsNone(SmokeTests.r.r_delete(key, returning=True), None)

	def test_delete_005(self):
		self.assertIsNone(SmokeTests.r.r_delete(''))

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

	def test_set_get_delete_convert_004(self):
		key: str = 'set_get_delete_convert_004'
		value: list[int] = [1, 2, 3, 4, 5]

		self.assertIsNone(SmokeTests.r.r_set(key, value))
		res_1 = SmokeTests.r.r_get(key, convert_to_type='int')
		self.assertEqual(res_1, value)

		res_2 = SmokeTests.r.r_delete(key, returning=True, convert_to_type_for_return='int')
		self.assertEqual(res_2, value)

	def test_set_get_delete_convert_005(self):
		key: str = 'set_get_delete_convert_005'
		value: set[int] = {1, 2, 3, 4, 5}

		self.assertIsNone(SmokeTests.r.r_set(key, value))
		res_1 = SmokeTests.r.r_get(key, convert_to_type='int')
		self.assertEqual(res_1, value)

		res_2 = SmokeTests.r.r_delete(key, returning=True, convert_to_type_for_return='int')
		self.assertEqual(res_2, value)

	def test_set_get_delete_convert_006(self):
		key: str = 'test_set_get_delete_convert_006'
		value: list[bytes] = [b'1', b'2', b'3', b'4', b'5']

		self.assertIsNone(SmokeTests.r.r_set(key, [i.decode('utf-8') for i in value]))
		res_1 = SmokeTests.r.r_get(key, convert_to_type='bytes_utf-8')
		self.assertEqual(res_1, value)

		res_2 = SmokeTests.r.r_delete(key, returning=True, convert_to_type_for_return='bytes_utf-8')
		self.assertEqual(res_2, value)

	def test_set_get_delete_convert_007(self):
		key: str = 'test_set_get_delete_convert_007'
		value: set[bytes] = {b'1', b'2', b'3', b'4', b'5'}

		self.assertIsNone(SmokeTests.r.r_set(key, {i.decode('ascii') for i in value}))
		res_1 = SmokeTests.r.r_get(key, convert_to_type='bytes_ascii')
		self.assertEqual(res_1, value)

		res_2 = SmokeTests.r.r_delete(key, returning=True, convert_to_type_for_return='bytes_ascii')
		self.assertEqual(res_2, value)

	def test_set_get_delete_convert_008(self):
		key: str = 'test_set_get_delete_convert_008'
		value: set[bytes] = {b'1', b'2', b'3', b'4', b'5'}

		value_decode = {i.decode('ascii') for i in value}
		self.assertIsNone(SmokeTests.r.r_set(key, value_decode))
		res_1 = SmokeTests.r.r_get(key, convert_to_type='any_bytes_ascii')  # wrong format for convert type
		self.assertEqual(res_1, value_decode)

		res_2 = SmokeTests.r.r_delete(key, returning=True, convert_to_type_for_return='any_bytes_ascii')
		self.assertEqual(res_2, value_decode)

	def test_set_get_delete_convert_009(self):
		key: str = 'test_set_get_delete_convert_009'
		value_bytes: list[bytes] = [b'1', b'2', b'3', b'4', b'5']
		value: list[str] = [i.decode('utf-8') for i in value_bytes]

		self.assertIsNone(SmokeTests.r.r_set(key, value))
		res_1 = SmokeTests.r.r_get(key, convert_to_type='bytes_utf-8')
		self.assertEqual(res_1, value_bytes)

		res_2 = SmokeTests.r.r_delete(key, returning=True, convert_to_type_for_return='bytes_utf-8')
		self.assertEqual(res_2, value_bytes)

	# unlink ###########################################################################################################

	def test_unlink_001(self):
		key: str = 'unlink_001'
		# doesn't set the value
		# delete
		self.assertIsNone(SmokeTests.r.r_unlink(key))

	def test_unlink_002(self):
		key: str = 'delete_002'
		# doesn't set the value
		# delete
		self.assertIsNone(SmokeTests.r.r_unlink(key, returning=False))

	def test_unlink_003(self):
		key: str = 'delete_003'
		# doesn't set the value
		# delete (with returning)
		self.assertIsNone(SmokeTests.r.r_unlink(key, returning=True))

	def test_unlink_004(self):
		key: str = 'delete_004'
		# doesn't set the value
		# delete (with returning and convert)
		self.assertIsNone(SmokeTests.r.r_unlink(key, returning=True), None)

	def test_unlink_005(self):
		self.assertIsNone(SmokeTests.r.r_unlink(''))

	# set/get/unlink ###################################################################################################

	def test_set_get_unlink_str_001(self):
		""" without returning """
		key: str = 'set_get_unlink_str_001'
		value: str = SmokeTests.get_random_string()

		self.assertIsNone(SmokeTests.r.r_set(key, value))
		res_1: str = SmokeTests.r.r_get(key)
		self.assertEqual(res_1, value)

		# delete (without returning - None)
		self.assertIsNone(SmokeTests.r.r_unlink(key))
		self.assertIsNone(SmokeTests.r.r_get(key))

	def test_set_get_unlink_str_002(self):
		""" with returning """
		key: str = 'set_get_unlink_str_002'
		value: str = SmokeTests.get_random_string()

		self.assertIsNone(SmokeTests.r.r_set(key, value))
		res_1: str = SmokeTests.r.r_get(key)
		self.assertEqual(res_1, value)

		# delete (without returning - None)
		res_2: str = SmokeTests.r.r_unlink(key, returning=True)
		self.assertEqual(res_1, res_2)
		self.assertIsNone(SmokeTests.r.r_get(key))

	def test_set_get_unlink_str_003(self):
		""" with returning and convert to wrong type """
		key: str = 'set_get_unlink_str_003'
		value: str = SmokeTests.get_random_string()

		self.assertIsNone(SmokeTests.r.r_set(key, value))
		res_1: str = SmokeTests.r.r_get(key, convert_to_type='numeric')
		self.assertEqual(res_1, value)

		# delete (with returning)
		res_2: str = SmokeTests.r.r_unlink(key, returning=True)
		self.assertEqual(res_1, res_2)
		self.assertIsNone(SmokeTests.r.r_get(key))

	def test_set_get_unlink_int_001(self):
		""" without returning """
		key: str = 'set_get_unlink_int_001'
		value: int = SmokeTests.get_random_integer()

		self.assertIsNone(SmokeTests.r.r_set(key, value))
		res_1: str = SmokeTests.r.r_get(key, convert_to_type='int')
		self.assertEqual(res_1, value)

		# delete (without returning - None)
		self.assertIsNone(SmokeTests.r.r_unlink(key))
		self.assertIsNone(SmokeTests.r.r_get(key))

	def test_set_get_unlink_int_002(self):
		""" with returning """
		key: str = 'set_get_unlink_int_002'
		value: int = SmokeTests.get_random_integer()

		self.assertIsNone(SmokeTests.r.r_set(key, value))
		res_1: str = SmokeTests.r.r_get(key)
		self.assertEqual(res_1, str(value))

		# delete (with returning)
		res_2: int = SmokeTests.r.r_unlink(key, returning=True)
		self.assertEqual(res_1, res_2)
		self.assertIsNone(SmokeTests.r.r_get(key))

	def test_set_get_unlink_int_003(self):
		""" with returning and convert """
		key: str = 'set_get_unlink_int_003'
		value: int = SmokeTests.get_random_integer()

		self.assertIsNone(SmokeTests.r.r_set(key, value))
		res_1: int = SmokeTests.r.r_get(key, convert_to_type='int')
		self.assertEqual(res_1, value)

		# delete (with returning)
		res_2: int = SmokeTests.r.r_unlink(key, returning=True, convert_to_type_for_return='integer')
		self.assertEqual(res_1, res_2)
		self.assertIsNone(SmokeTests.r.r_get(key))

	def test_set_get_unlink_int_004(self):
		""" with returning and convert to wrong type """
		key: str = 'set_get_unlink_int_004'
		value: int = SmokeTests.get_random_integer()

		self.assertIsNone(SmokeTests.r.r_set(key, value))
		res_1: str = SmokeTests.r.r_get(key)
		self.assertEqual(res_1, str(value))

		# delete (with returning)
		res_2: int = SmokeTests.r.r_unlink(key, returning=True, convert_to_type_for_return='123')
		self.assertEqual(res_1, res_2)
		self.assertIsNone(SmokeTests.r.r_get(key))

	def test_set_get_unlink_float_001(self):
		""" without returning """
		key: str = 'set_get_unlink_float_001'
		value: float = float(SmokeTests.get_random_integer())

		self.assertIsNone(SmokeTests.r.r_set(key, value))
		res_1: float = SmokeTests.r.r_get(key, convert_to_type='float')
		self.assertEqual(res_1, value)

		# delete (without returning - None)
		self.assertIsNone(SmokeTests.r.r_unlink(key))
		self.assertIsNone(SmokeTests.r.r_get(key))

	def test_set_get_unlink_float_002(self):
		""" with returning """
		key: str = 'set_get_unlink_float_002'
		value: float = float(SmokeTests.get_random_integer())

		self.assertIsNone(SmokeTests.r.r_set(key, value))
		res_1: float = SmokeTests.r.r_get(key, convert_to_type='float')
		self.assertEqual(res_1, value)

		res_2: str = SmokeTests.r.r_unlink(key, returning=True)
		self.assertEqual(res_2, str(value))
		self.assertIsNone(SmokeTests.r.r_get(key))

	def test_set_get_unlink_float_003(self):
		""" with returning and convert """
		key: str = 'set_get_unlink_float_003'
		value: float = float(SmokeTests.get_random_integer())

		self.assertIsNone(SmokeTests.r.r_set(key, value))
		res_1: float = SmokeTests.r.r_get(key, convert_to_type='float')
		self.assertEqual(res_1, value)

		res_2: str = SmokeTests.r.r_unlink(key, returning=True, convert_to_type_for_return='double')
		self.assertEqual(res_2, value)
		self.assertIsNone(SmokeTests.r.r_get(key))

	def test_set_get_unlink_float_004(self):
		""" with returning and convert to wrong type """
		key: str = 'set_get_unlink_float_004'
		value: float = float(SmokeTests.get_random_integer())

		self.assertIsNone(SmokeTests.r.r_set(key, value))
		res_1: float = SmokeTests.r.r_get(key, convert_to_type='float')
		self.assertEqual(res_1, value)

		res_2: str = SmokeTests.r.r_unlink(key, returning=True, convert_to_type_for_return='wrong type')
		self.assertEqual(res_2, str(value))
		self.assertIsNone(SmokeTests.r.r_get(key))

	def test_set_get_unlink_bool_001(self):
		key: str = 'set_get_unlink_bool_001'
		value: bool = True

		self.assertIsNone(SmokeTests.r.r_set(key, value))
		res_1: bool = SmokeTests.r.r_get(key, convert_to_type='bool')
		self.assertEqual(res_1, value)

		res_2: str = SmokeTests.r.r_unlink(key, returning=True, convert_to_type_for_return='boolean')
		self.assertEqual(res_2, value)
		self.assertIsNone(SmokeTests.r.r_get(key))

	def test_set_get_unlink_bool_002(self):
		key: str = 'set_get_unlink_bool_002'
		value: bool = False

		self.assertIsNone(SmokeTests.r.r_set(key, value))
		res_1: bool = SmokeTests.r.r_get(key, convert_to_type='bool')
		self.assertEqual(res_1, value)

		res_2: str = SmokeTests.r.r_unlink(key, returning=True, convert_to_type_for_return='boolean')
		self.assertEqual(res_2, value)
		self.assertIsNone(SmokeTests.r.r_get(key))

	# TODO - set_get_unlink for arrays

	# rename ###########################################################################################################

	def test_rename_key_001(self):
		""" Lua - string """
		key: str = 'rename_key_001'
		new_key: str = 'rename_key_001-new'
		value: str = SmokeTests.get_random_string()
		self.assertIsNone(self.r.r_set(key, value))
		self.assertEqual(self.r.r_get(key), value)
		self.r.rename_key(key, new_key)
		self.assertIsNone(self.r.r_get(key))
		self.assertEqual(self.r.r_get(new_key), value)

	def test_rename_key_002(self):
		""" Lua - boolean """
		key: str = 'rename_key_002'
		new_key: str = 'rename_key_002-new'
		value: bool = True if SmokeTests.get_random_integer() % 2 == 0 else False
		self.assertIsNone(self.r.r_set(key, value))
		self.assertEqual(self.r.r_get(key, convert_to_type='bool'), value)
		self.r.rename_key(key, new_key)
		self.assertIsNone(self.r.r_get(key))
		self.assertEqual(self.r.r_get(new_key, convert_to_type='bool'), value)

	def test_rename_key_003(self):
		""" Lua - integer """
		key: str = 'rename_key_003'
		new_key: str = 'rename_key_003-new'
		value: int = SmokeTests.get_random_integer()
		self.assertIsNone(self.r.r_set(key, value))
		self.assertEqual(self.r.r_get(key, convert_to_type='int'), value)
		self.r.rename_key(key, new_key)
		self.assertIsNone(self.r.r_get(key))
		self.assertEqual(self.r.r_get(new_key, convert_to_type='int'), value)

	def test_rename_key_004(self):
		""" Lua - float """
		key: str = 'rename_key_004'
		new_key: str = 'rename_key_004-new'
		value: float = float(SmokeTests.get_random_integer()) + random()
		self.assertIsNone(self.r.r_set(key, value))
		self.assertEqual(self.r.r_get(key, convert_to_type='float'), value)
		self.r.rename_key(key, new_key)
		self.assertIsNone(self.r.r_get(key))
		self.assertEqual(self.r.r_get(new_key, convert_to_type='float'), value)

	def test_rename_key_005(self):
		""" Lua - list """
		key: str = 'rename_key_005'
		new_key: str = 'rename_key_005-new'
		value: list[int] = [SmokeTests.get_random_integer() for _ in range(randint(10, 20))]
		self.assertIsNone(self.r.r_set(key, value))
		self.assertEqual(self.r.r_get(key, convert_to_type='int'), value)
		self.r.rename_key(key, new_key)
		self.assertIsNone(self.r.r_get(key))
		self.assertEqual(self.r.r_get(new_key, convert_to_type='int'), value)

	def test_rename_key_006(self):
		""" Lua - tuple """
		key: str = 'rename_key_006'
		new_key: str = 'rename_key_006-new'
		value: tuple = tuple(float(SmokeTests.get_random_integer()) + random() for _ in range(randint(10, 20)))
		self.assertIsNone(self.r.r_set(key, value))
		self.assertEqual(tuple(self.r.r_get(key, convert_to_type='float')), value)
		self.r.rename_key(key, new_key)
		self.assertIsNone(self.r.r_get(key))
		self.assertEqual(tuple(self.r.r_get(new_key, convert_to_type='float')), value)

	def test_rename_key_007(self):
		""" Lua - set """
		key: str = 'rename_key_007'
		new_key: str = 'rename_key_007-new'
		value: set = {SmokeTests.get_random_integer() for _ in range(randint(5, 10))}
		self.assertIsNone(self.r.r_set(key, value))
		self.assertEqual(set(self.r.r_get(key, convert_to_type='int')), value)
		self.r.rename_key(key, new_key)
		self.assertIsNone(self.r.r_get(key))
		self.assertEqual(set(self.r.r_get(new_key, convert_to_type='int')), value)

	def test_rename_key_008(self):
		""" Lua - frozenset """
		key: str = 'rename_key_008'
		new_key: str = 'rename_key_008-new'
		value: frozenset = frozenset(SmokeTests.get_random_string() for _ in range(randint(5, 10)))
		self.assertIsNone(self.r.r_set(key, value))
		self.assertEqual(frozenset(self.r.r_get(key)), value)
		self.r.rename_key(key, new_key)
		self.assertIsNone(self.r.r_get(key))
		self.assertEqual(frozenset(self.r.r_get(new_key)), value)

	# remove all keys ##################################################################################################

	def test_r_remove_all_keys_local_001(self):
		""" Lua """
		self.assertIsNone(SmokeTests.r.r_remove_all_keys_local())
		key_count: int = randint(5, 10)
		for key in range(key_count):
			SmokeTests.r.r_set(str(key), key)
		res = SmokeTests.r.r_remove_all_keys_local(get_count_keys=True)
		self.assertEqual(res, key_count)

	def test_r_remove_all_keys_local_002(self):
		""" Lua """
		self.assertIsNone(SmokeTests.r.r_remove_all_keys_local())
		key_count: int = randint(5, 10)
		for key in range(key_count):
			SmokeTests.r.r_set(str(key), [key])
		res = SmokeTests.r.r_remove_all_keys_local(get_count_keys=True)
		self.assertEqual(res, key_count)

	def test_r_remove_all_keys_local_003(self):
		""" Lua """
		self.assertIsNone(SmokeTests.r.r_remove_all_keys_local())
		key_count: int = randint(25, 50)
		for key in range(key_count):
			SmokeTests.r.r_set(str(key), str(key))
		res = SmokeTests.r.r_remove_all_keys_local(get_count_keys=True)
		self.assertEqual(res, key_count)

	def test_r_remove_all_keys_local_004(self):
		""" Lua  - integer - without get_count_keys param """
		self.assertIsNone(SmokeTests.r.r_remove_all_keys_local())
		key_count: int = randint(50, 100)
		for key in range(key_count):
			SmokeTests.r.r_set(str(key), key)
		self.assertIsNone(SmokeTests.r.r_remove_all_keys_local())

	def test_r_remove_all_keys_local_005(self):
		""" Lua  - str - without get_count_keys param """
		self.assertIsNone(SmokeTests.r.r_remove_all_keys_local())
		key_count: int = randint(50, 100)
		for key in range(key_count):
			SmokeTests.r.r_set(str(key), str(key))
		self.assertIsNone(SmokeTests.r.r_remove_all_keys_local())

	# check_keys_and_get_values ########################################################################################

	def test_check_keys_and_get_values_001(self):
		""" key is integer """
		self.assertIsNone(SmokeTests.r.r_remove_all_keys_local())
		exists_keys: tuple = tuple([i for i in range(randint(50, 100)) if i % randint(2, 5) == 0])
		for key in exists_keys:
			SmokeTests.r.r_set(str(key), key)
		res: dict = SmokeTests.r.check_keys_and_get_values(exists_keys)
		self.assertEqual(sorted(res.keys()), sorted(exists_keys))

	def test_check_keys_and_get_values_002(self):
		""" key is string """
		self.assertIsNone(SmokeTests.r.r_remove_all_keys_local())
		exists_keys: tuple = tuple([str(i) for i in range(randint(50, 100)) if i % randint(2, 5) == 0])
		for key in exists_keys:
			SmokeTests.r.r_set(key, key)
		res: dict = SmokeTests.r.check_keys_and_get_values(exists_keys)
		self.assertEqual(sorted(res.keys()), sorted(exists_keys))

	def test_check_keys_and_get_values_003(self):
		""" check each key - value """
		self.assertIsNone(SmokeTests.r.r_remove_all_keys_local())
		exists_keys: tuple = tuple([i for i in range(randint(50, 100)) if i % randint(2, 5) == 0])
		for key in exists_keys:
			SmokeTests.r.r_set(str(key), key)
		res: dict = SmokeTests.r.check_keys_and_get_values(exists_keys)
		self.assertEqual(sorted(res.keys()), sorted(exists_keys))
		for key in res.keys():
			self.assertEqual(str(key), res[key])

	# r_mass_delete ####################################################################################################

	def test_r_mass_delete_001(self):
		self.assertIsNone(SmokeTests.r.r_remove_all_keys_local())
		keys: tuple = tuple([i for i in range(randint(50, 100))])
		for key in keys:
			SmokeTests.r.r_set(key, int(key))
		res = SmokeTests.r.r_mass_delete(keys)
		self.assertEqual(res,  ((), (), {}))

	def test_r_mass_delete_002(self):
		""" Don't write down all the keys """
		self.assertIsNone(SmokeTests.r.r_remove_all_keys_local())
		keys: tuple = tuple([str(i) for i in range(randint(50, 100))])
		for key in keys[:randint(5, 10)]:
			SmokeTests.r.r_set(key, key)
		res = SmokeTests.r.r_mass_delete(keys)
		self.assertEqual(res,  ((), (), {}))

	def test_r_mass_delete_003(self):
		""" Don't write down all the keys """
		self.assertIsNone(SmokeTests.r.r_remove_all_keys_local())
		keys: tuple = tuple([str(i) for i in range(randint(50, 100))])
		for key in keys[:len(keys)//2]:
			SmokeTests.r.r_set(key, key)
		res = SmokeTests.r.r_mass_delete(keys, return_non_exists=True)
		self.assertTrue(isinstance(res, tuple))
		self.assertEqual(res[0], ())
		self.assertEqual(sorted(res[1]),  sorted(keys[len(keys)//2:]))
		self.assertEqual(res[2], {})

	def test_r_mass_delete_004(self):
		""" Don't write down all the keys """
		self.assertIsNone(SmokeTests.r.r_remove_all_keys_local())
		keys: tuple = tuple([str(i) for i in range(randint(50, 100))])
		exists_keys: tuple = keys[:len(keys) // randint(2, 5)]
		for key in exists_keys:
			SmokeTests.r.r_set(str(key), key)
		res = SmokeTests.r.r_mass_delete(keys, return_exists=True)
		self.assertTrue(isinstance(res, tuple))
		self.assertEqual(sorted(res[0]), sorted(exists_keys))
		self.assertEqual(res[1], ())
		self.assertEqual(res[2], {})

	def test_r_mass_delete_005(self):
		""" Don't write down all the keys """
		self.assertIsNone(SmokeTests.r.r_remove_all_keys_local())
		keys: tuple = tuple([str(i) for i in range(randint(50, 100))])
		_slice: int = randint(2, 5)
		exists_keys: tuple = keys[:len(keys) // _slice]
		key_value: dict = {key: SmokeTests.get_random_string() for key in exists_keys}
		for key, value in key_value.items():
			SmokeTests.r.r_set(key, value)

		res = SmokeTests.r.r_mass_delete(
			keys, return_exists=True, return_non_exists=True, get_dict_key_value_exists=True
		)

		self.assertTrue(isinstance(res, tuple))
		self.assertEqual(sorted(res[0]), sorted(exists_keys))  # return_exists
		self.assertEqual(sorted(res[1]),  sorted(keys[len(keys)//_slice:]))  # return_non_exists
		self.assertEqual(dict(sorted(res[2].items())), dict(sorted(key_value.items())))  # get_dict_key_value_exists

	def test_r_mass_delete_006(self):
		self.assertIsNone(SmokeTests.r.r_remove_all_keys_local())
		keys: tuple = tuple([str(i) for i in range(randint(50, 100))])
		key_value: dict = {key: SmokeTests.get_random_string() for key in keys}
		for key, value in key_value.items():
			SmokeTests.r.r_set(key, value)

		res = SmokeTests.r.r_mass_delete(
			keys, return_exists=True, return_non_exists=True, get_dict_key_value_exists=True,
		)

		self.assertTrue(isinstance(res, tuple))
		self.assertEqual(sorted(res[0]), sorted(keys))  # return_exists
		self.assertEqual(res[1],  ())  # return_non_exists
		self.assertEqual(dict(sorted(res[2].items())), dict(sorted(key_value.items())))  # get_dict_key_value_exists

	def test_r_mass_delete_007(self):
		""" get key-value with converting type """
		self.assertIsNone(SmokeTests.r.r_remove_all_keys_local())
		keys: tuple = tuple([str(i) for i in range(randint(50, 100))])
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
		self.assertIsNone(SmokeTests.r.r_remove_all_keys_local())
		keys: tuple = tuple([str(i) for i in range(randint(50, 100))])
		key_value: dict = {key: bool(randint(0, 1)) for key in keys}
		for key, value in key_value.items():
			SmokeTests.r.r_set(key, value)

		res = SmokeTests.r.r_mass_delete(keys, get_dict_key_value_exists=True, convert_to_type_dict_key='boolean')

		self.assertTrue(isinstance(res, tuple))
		self.assertEqual(res[0], ())  # return_exists
		self.assertEqual(res[1], ())  # return_non_exists
		self.assertEqual(dict(sorted(res[2].items())), dict(sorted(key_value.items())))  # get_dict_key_value_exists

	def test_r_mass_delete_009(self):
		""" get key-value with converting type """
		self.assertIsNone(SmokeTests.r.r_remove_all_keys_local())
		keys: tuple = tuple([str(i) for i in range(randint(50, 100))])
		key_value: dict = {key: bool(randint(0, 1)) for key in keys}
		for key, value in key_value.items():
			SmokeTests.r.r_set(key, value)

		res = SmokeTests.r.r_mass_delete(
			keys, return_exists=True, get_dict_key_value_exists=True, convert_to_type_dict_key='bool'
		)

		self.assertTrue(isinstance(res, tuple))
		self.assertEqual(res[0], tuple(sorted(list(keys))))  # return_exists
		self.assertEqual(res[1], ())  # return_non_exists
		self.assertEqual(dict(sorted(res[2].items())), dict(sorted(key_value.items())))  # get_dict_key_value_exists

	def test_r_mass_delete_010(self):
		""" get key-value with converting type """
		self.assertIsNone(SmokeTests.r.r_remove_all_keys_local())
		keys: tuple = tuple([str(i) for i in range(randint(50, 100))])
		key_value: dict = {key: randint(0, 1_000) for key in keys}
		for key, value in key_value.items():
			SmokeTests.r.r_set(key, value)

		res = SmokeTests.r.r_mass_delete(
			keys, return_exists=True, get_dict_key_value_exists=True, convert_to_type_dict_key='integer'
		)

		self.assertTrue(isinstance(res, tuple))
		self.assertEqual(res[0], tuple(sorted(list(keys))))  # return_exists
		self.assertEqual(res[1], ())  # return_non_exists
		self.assertEqual(dict(sorted(res[2].items())), dict(sorted(key_value.items())))  # get_dict_key_value_exists

	def test_r_mass_delete_011(self):
		""" get key-value with converting type (integer) and without other params """
		self.assertIsNone(SmokeTests.r.r_remove_all_keys_local())
		keys: tuple = tuple([str(i) for i in range(randint(50, 100))])
		key_value: dict = {key: randint(0, 1_000) for key in keys}
		for key, value in key_value.items():
			SmokeTests.r.r_set(key, value)

		res = SmokeTests.r.r_mass_delete(
			keys, convert_to_type_dict_key='integer'
		)

		self.assertTrue(isinstance(res, tuple))
		self.assertEqual(res[0], ())  # return_exists
		self.assertEqual(res[1], ())  # return_non_exists
		self.assertEqual(res[2], {})  # get_dict_key_value_exists

	def test_r_mass_delete_012(self):
		""" get key-value with converting type (boolean) and without other params """
		self.assertIsNone(SmokeTests.r.r_remove_all_keys_local())
		keys: tuple = tuple([str(i) for i in range(randint(50, 100))])
		key_value: dict = {key: randint(0, 1_000) for key in keys}
		for key, value in key_value.items():
			SmokeTests.r.r_set(key, value)

		res = SmokeTests.r.r_mass_delete(
			keys, convert_to_type_dict_key='boolean'
		)

		self.assertTrue(isinstance(res, tuple))
		self.assertEqual(res[0], ())  # return_exists
		self.assertEqual(res[1], ())  # return_non_exists
		self.assertEqual(res[2], {})  # get_dict_key_value_exists

	def test_r_mass_delete_013(self):
		self.assertEqual(SmokeTests.r.r_mass_delete([]), ((), (), {}))

	def test_r_mass_delete_014(self):
		self.assertEqual(SmokeTests.r.r_mass_delete(tuple()), ((), (), {}))

	def test_r_mass_delete_015(self):
		self.assertEqual(SmokeTests.r.r_mass_delete(set()), ((), (), {}))

	def test_r_mass_delete_016(self):
		self.assertEqual(SmokeTests.r.r_mass_delete(frozenset()), ((), (), {}))

	# r_mass_unlink ####################################################################################################

	def test_r_mass_unlink_001(self):
		self.assertEqual(SmokeTests.r.r_mass_unlink([]), ((), (), {}))

	def test_r_mass_unlink_002(self):
		self.assertEqual(SmokeTests.r.r_mass_unlink(tuple()), ((), (), {}))

	def test_r_mass_unlink_003(self):
		self.assertEqual(SmokeTests.r.r_mass_unlink(set()), ((), (), {}))

	def test_r_mass_unlink_004(self):
		self.assertEqual(SmokeTests.r.r_mass_unlink(frozenset()), ((), (), {}))

	# r_set function with 'if_exists' parameter ########################################################################

	def test_r_set_if_exists_001(self):
		key: str = 'r_set_if_exists_001'
		value_1: str = SmokeTests.get_random_string()
		SmokeTests.r.r_set(key, value_1)

		value_2: str = SmokeTests.get_random_string()
		SmokeTests.r.r_set(key, value_2, if_exist=True)

		res: str = SmokeTests.r.r_get(key)
		self.assertEqual(res, value_2)

	def test_r_set_if_exists_002(self):
		key: str = 'r_set_if_exists_002'
		value_1: str = SmokeTests.get_random_string()
		SmokeTests.r.r_set(key, value_1)

		value_lst: list = [SmokeTests.get_random_integer() for _ in range(randint(10, 15))]
		SmokeTests.r.r_set(key, value_lst, if_exist=True)

		res: str = SmokeTests.r.r_get(key, convert_to_type='int')
		self.assertEqual(res, value_lst)

	def test_r_set_if_exists_003(self):
		key: str = 'r_set_if_exists_003'
		value_1: str = SmokeTests.get_random_string()
		SmokeTests.r.r_set(key, value_1, if_exist=True)
		res: str = SmokeTests.r.r_get(key)
		self.assertIsNone(res)

	# r_set function with 'if_not_exists' parameter ####################################################################

	def test_r_set_if_not_exists_001(self):
		key: str = 'r_set_if_not_exists_001'
		value_1: int = SmokeTests.get_random_integer()
		SmokeTests.r.r_set(key, value_1)

		value_2: str = SmokeTests.get_random_string()
		SmokeTests.r.r_set(key, value_2, if_not_exist=True)

		res: str = SmokeTests.r.r_get(key, convert_to_type='integer')
		self.assertEqual(res, value_1)

	def test_r_set_if_not_exists_002(self):
		key: str = 'r_set_if_not_exists_002'
		value_1: str = SmokeTests.get_random_string()
		SmokeTests.r.r_set(key, value_1)
		value_2: str = SmokeTests.get_random_string()
		SmokeTests.r.r_set(key, value_2, if_not_exist=True)
		res: str = SmokeTests.r.r_get(key)
		self.assertEqual(res, value_1)

	def test_r_set_if_not_exists_003(self):
		key: str = 'r_set_if_not_exists_003'
		value_1: str = SmokeTests.get_random_string()
		SmokeTests.r.r_set(key, value_1)

		value_lst: list = [SmokeTests.get_random_integer() for _ in range(randint(10, 15))]
		SmokeTests.r.r_set(key, value_lst, if_not_exist=True)
		res: str = SmokeTests.r.r_get(key)
		self.assertEqual(res, value_1)

	def test_get_redis_info_001(self):
		self.assertTrue(len(SmokeTests.r.get_redis_info()) > 0)

	def test_get_redis_info_002(self):
		self.assertTrue(SmokeTests.r.get_redis_info().get('uptime_in_seconds'))

	def test_get_redis_info_003(self):
		self.assertTrue(SmokeTests.r.get_redis_info().get('redis_version'))

	def test_get_redis_info_004(self):
		self.assertTrue(SmokeTests.r.get_redis_info().get('gcc_version'))

	def test_get_redis_info_005(self):
		self.assertTrue(SmokeTests.r.get_redis_info().get('arch_bits'))

	def test_get_redis_info_006(self):
		self.assertTrue(SmokeTests.r.get_redis_info().get('os'))

	def test_get_key_memory_usage_001(self):
		key: str = 'get_key_memory_usage_001'
		SmokeTests.r.r_set(key, key)
		self.assertTrue(SmokeTests.r.get_key_memory_usage(key) > 0)

	def test_get_key_memory_usage_002(self):
		key: str = 'get_key_memory_usage_002'
		# without set
		self.assertEqual(SmokeTests.r.get_key_memory_usage(key), 0)

	# r_pop ############################################################################################################

	def test_r_pop_001(self):
		key: str = self.test_r_pop_001.__name__
		_len: int = randint(5, 10)
		_list: list = [i for i in range(_len)]
		SmokeTests.r.r_set(key, _list)

		res_1: tuple = SmokeTests.r.r_pop(key)
		self.assertTrue(len(res_1) == 1, f'len = {len(res_1)}')
		self.assertTrue(int(res_1[0]) == _list[-1], f'res[0] = {res_1[0]} | _len[-1] = {_list[-1]}')
		self.assertEqual(
			list(map(int, SmokeTests.r.r_get(key))), _list[:-1], f'r_get(key) = {SmokeTests.r.r_get(key)}'
		)

	def test_r_pop_002(self):
		# test_r_pop_001 with convert to type
		key: str = self.test_r_pop_002.__name__
		_len: int = randint(5, 10)
		_list: list = [i for i in range(_len)]
		SmokeTests.r.r_set(key, _list)

		res_1: tuple = SmokeTests.r.r_pop(key, convert_to_type='int')
		self.assertTrue(len(res_1) == 1, f'len = {len(res_1)}')
		self.assertEqual(res_1[0], _list[-1])
		self.assertEqual(
			SmokeTests.r.r_get(key, convert_to_type='integer'), _list[:-1], f'r_get(key) = {SmokeTests.r.r_get(key)}'
		)

	def test_r_pop_003(self):
		"""
		List
		Count == Len
		Checking if a key is deleted if there are no elements left
		"""
		key: str = self.test_r_pop_003.__name__
		_len: int = randint(10, 20)
		_list: list = [str(SmokeTests.get_random_integer()) for _ in range(_len)]
		SmokeTests.r.r_set(key, _list)

		res_1: tuple = SmokeTests.r.r_pop(key, count=_len)
		self.assertIsNone(SmokeTests.r.r_get(key))  # deleted after r_pop
		self.assertEqual(len(res_1), _len)
		self.assertEqual(sorted(list(res_1)), sorted(_list))

	def test_r_pop_004(self):
		"""
		List
		Count != Len
		Checking if a key is deleted if there are no elements left
		"""
		key: str = self.test_r_pop_004.__name__
		_len: int = randint(10, 20)
		_len_pop: int = randint(3, 5)
		_list: list = [str(SmokeTests.get_random_integer()) for _ in range(_len)]
		SmokeTests.r.r_set(key, _list)

		res_1: tuple = SmokeTests.r.r_pop(key, count=_len_pop)
		self.assertIsNotNone(SmokeTests.r.r_get(key))  # not deleted after r_pop
		self.assertEqual(len(res_1), _len_pop)
		self.assertEqual(sorted(list(res_1)), sorted(_list[-_len_pop:]))
		_new_list: list = list(SmokeTests.r.r_get(key))
		self.assertEqual(sorted(_new_list), sorted(_list[:-_len_pop]))

	def test_r_pop_005(self):
		"""
		Tuple
		Count == Len
		Checking if a key is deleted if there are no elements left
		"""
		key: str = self.test_r_pop_005.__name__
		_len: int = randint(10, 20)
		_tuple: tuple = tuple(str(SmokeTests.get_random_integer()) for _ in range(_len))
		SmokeTests.r.r_set(key, _tuple)

		res_1: tuple = SmokeTests.r.r_pop(key, count=_len)
		self.assertIsNone(SmokeTests.r.r_get(key))  # deleted after r_pop
		self.assertEqual(len(res_1), _len)
		self.assertEqual(sorted(list(res_1)), sorted(list(_tuple)))

	def test_r_pop_006(self):
		"""
		Tuple
		Count != Len
		Checking if a key is deleted if there are no elements left
		"""
		key: str = self.test_r_pop_006.__name__
		_len: int = randint(10, 20)
		_tuple_pop: int = randint(3, 5)
		_tuple: tuple = tuple(str(SmokeTests.get_random_integer()) for _ in range(_len))
		SmokeTests.r.r_set(key, _tuple)

		res_1: tuple = SmokeTests.r.r_pop(key, count=_tuple_pop)
		self.assertIsNotNone(SmokeTests.r.r_get(key))  # not deleted after r_pop
		self.assertEqual(len(res_1), _tuple_pop)
		self.assertEqual(sorted(list(res_1)), sorted(list(_tuple[-_tuple_pop:])))
		_new_tuple: tuple = tuple(SmokeTests.r.r_get(key))
		self.assertEqual(sorted(list(_new_tuple)), sorted(list(_tuple[:-_tuple_pop])))

	def test_r_pop_007(self):
		"""
		Set
		Count == Len
		Checking if a key is deleted if there are no elements left
		"""
		key: str = self.test_r_pop_007.__name__
		_len: int = randint(10, 20)
		_set: set = set(str(SmokeTests.get_random_integer()) for _ in range(_len))
		SmokeTests.r.r_set(key, _set)

		res_1: tuple = SmokeTests.r.r_pop(key, count=_len)
		self.assertIsNone(SmokeTests.r.r_get(key))  # deleted after r_pop
		self.assertEqual(len(res_1), _len)
		self.assertEqual(sorted(list(res_1)), sorted(list(_set)))

	def test_r_pop_008(self):
		"""
		Set
		Count != Len
		Checking if a key is deleted if there are no elements left
		"""
		key: str = self.test_r_pop_008.__name__
		_len: int = randint(10, 20)
		_set_pop: int = randint(3, 5)
		_set: set = set(str(SmokeTests.get_random_integer()) for _ in range(_len))
		SmokeTests.r.r_set(key, _set)

		res_1: tuple = SmokeTests.r.r_pop(key, count=_set_pop)
		self.assertIsNotNone(SmokeTests.r.r_get(key))  # not deleted after r_pop
		self.assertEqual(len(res_1), _set_pop)
		_new_set: set = set(SmokeTests.r.r_get(key))
		self.assertEqual(len(_new_set), _len - _set_pop)
		# There is no point in comparing the remaining values here - sets do not store the order of values
		# This means that we will get false results

	def test_r_pop_009(self):
		"""
		Frozenset
		Count == Len
		Checking if a key is deleted if there are no elements left
		"""
		key: str = self.test_r_pop_009.__name__
		_len: int = randint(10, 20)
		_frozenset: frozenset = frozenset(str(SmokeTests.get_random_integer()) for _ in range(_len))
		SmokeTests.r.r_set(key, _frozenset)

		res_1: tuple = SmokeTests.r.r_pop(key, count=_len)

		self.assertIsNone(SmokeTests.r.r_get(key))  # deleted after r_pop
		self.assertEqual(len(res_1), _len)
		self.assertEqual(sorted(list(res_1)), sorted(list(_frozenset)))

	def test_r_pop_010(self):
		"""
		Frozenset
		Count != Len
		Checking if a key is deleted if there are no elements left
		"""
		key: str = self.test_r_pop_010.__name__
		_len: int = randint(10, 20)
		_set_pop: int = randint(3, 5)
		_frozenset: frozenset = frozenset(str(SmokeTests.get_random_integer()) for _ in range(_len))
		SmokeTests.r.r_set(key, _frozenset)

		res_1: tuple = SmokeTests.r.r_pop(key, count=_set_pop)
		self.assertIsNotNone(SmokeTests.r.r_get(key))  # not deleted after r_pop
		self.assertEqual(len(res_1), _set_pop)
		_new_frozenset: frozenset = frozenset(SmokeTests.r.r_get(key))
		self.assertEqual(len(_new_frozenset), _len - _set_pop)
		# There is no point in comparing the remaining values here - frozensets do not store the order of values
		# This means that we will get false results

	def test_r_pop_011(self):
		"""
		List
		Len == 1
		Checking if a key is deleted if there are no elements left
		"""
		key: str = self.test_r_pop_011.__name__
		_list: list = [randint(1, 100)]
		SmokeTests.r.r_set(key, _list)
		_pop: tuple = SmokeTests.r.r_pop(key, convert_to_type='int')
		self.assertIsNone(SmokeTests.r.r_get(key))  # deleted after r_pop
		self.assertEqual(_pop, tuple(_list))

	def test_r_pop_012(self):
		"""
		Tuple
		Len == 1
		Checking if a key is deleted if there are no elements left
		"""
		key: str = self.test_r_pop_012.__name__
		_tuple: tuple = (randint(1, 100),)
		SmokeTests.r.r_set(key, _tuple)
		_pop: tuple = SmokeTests.r.r_pop(key, convert_to_type='int')
		self.assertIsNone(SmokeTests.r.r_get(key))  # deleted after r_pop
		self.assertEqual(_pop, _tuple)

	def test_r_pop_013(self):
		"""
		Set
		Len == 1
		Checking if a key is deleted if there are no elements left
		"""
		key: str = self.test_r_pop_013.__name__
		_set: set = {randint(1, 100)}
		SmokeTests.r.r_set(key, _set)
		_pop: tuple = SmokeTests.r.r_pop(key, convert_to_type='int')
		self.assertIsNone(SmokeTests.r.r_get(key))  # deleted after r_pop
		self.assertEqual(_pop, tuple(_set))

	def test_r_pop_014(self):
		"""
		Frozenset
		Len == 1
		Checking if a key is deleted if there are no elements left
		"""
		key: str = self.test_r_pop_014.__name__
		_frozenset: frozenset = frozenset([randint(1, 100)])
		SmokeTests.r.r_set(key, _frozenset)
		_pop: tuple = SmokeTests.r.r_pop(key, convert_to_type='int')
		self.assertIsNone(SmokeTests.r.r_get(key))  # deleted after r_pop
		self.assertEqual(_pop, tuple(_frozenset))

	def test_r_pop_015(self):
		"""
		List
		Len == 1 (reverse)
		Checking if a key is deleted if there are no elements left
		"""
		key: str = self.test_r_pop_015.__name__
		_list: list = [randint(1, 100)]
		SmokeTests.r.r_set(key, _list)
		_pop: tuple = SmokeTests.r.r_pop(key, reverse=True, convert_to_type='int')
		self.assertIsNone(SmokeTests.r.r_get(key))  # deleted after r_pop
		self.assertEqual(_pop, tuple(_list))

	def test_r_pop_016(self):
		"""
		Tuple
		Len == 1 (reverse)
		Checking if a key is deleted if there are no elements left
		"""
		key: str = self.test_r_pop_016.__name__
		_tuple: tuple = (randint(1, 100),)
		SmokeTests.r.r_set(key, _tuple)
		_pop: tuple = SmokeTests.r.r_pop(key, reverse=True, convert_to_type='int')
		self.assertIsNone(SmokeTests.r.r_get(key))  # deleted after r_pop
		self.assertEqual(_pop, _tuple)

	def test_r_pop_017(self):
		"""
		Set
		Len == 1 (reverse)
		Checking if a key is deleted if there are no elements left
		"""
		key: str = self.test_r_pop_017.__name__
		_set: set = {randint(1, 100)}
		SmokeTests.r.r_set(key, _set)
		_pop: tuple = SmokeTests.r.r_pop(key, reverse=True, convert_to_type='int')
		self.assertIsNone(SmokeTests.r.r_get(key))  # deleted after r_pop
		self.assertEqual(_pop, tuple(_set))

	def test_r_pop_018(self):
		"""
		Frozenset
		Len == 1 (reverse)
		Checking if a key is deleted if there are no elements left
		"""
		key: str = self.test_r_pop_018.__name__
		_frozenset: frozenset = frozenset([randint(1, 100)])
		SmokeTests.r.r_set(key, _frozenset)
		_pop: tuple = SmokeTests.r.r_pop(key, reverse=True, convert_to_type='int')
		self.assertIsNone(SmokeTests.r.r_get(key))  # deleted after r_pop
		self.assertEqual(_pop, tuple(_frozenset))

	def test_r_pop_019(self):
		"""
		Get all elements except the last one
		List
		"""
		key: str = self.test_r_pop_019.__name__
		_len: int = randint(10, 20)
		_len_pop: int = _len - 1
		_list: list = [str(SmokeTests.get_random_integer()) for _ in range(_len)]
		SmokeTests.r.r_set(key, _list)

		res_1: tuple = SmokeTests.r.r_pop(key, count=_len_pop)
		self.assertIsNotNone(SmokeTests.r.r_get(key))  # not deleted after r_pop
		self.assertEqual(len(res_1), _len_pop)
		self.assertEqual(sorted(list(res_1)), sorted(_list[1:]))
		_new_list: list = list(SmokeTests.r.r_get(key))
		self.assertEqual(sorted(_new_list), sorted([_list[0]]))

	def test_r_pop_020(self):
		"""
		Get all elements except the last one
		Tuple
		"""
		key: str = self.test_r_pop_020.__name__

	def test_r_pop_021(self):
		"""
		Get all elements except the last one
		Set
		"""
		key: str = self.test_r_pop_021.__name__

	def test_r_pop_022(self):
		"""
		Get all elements except the last one
		Frozenset
		"""
		key: str = self.test_r_pop_022.__name__

	def test_r_pop_023(self):
		"""
		Get all elements except the last one (reverse)
		"""
		key: str = self.test_r_pop_023.__name__

	def test_r_pop_024(self):
		"""
		Get all elements except the last one (reverse)
		List
		"""
		key: str = self.test_r_pop_024.__name__

	def test_r_pop_025(self):
		"""
		Get all elements except the last one (reverse)
		Tuple
		"""
		key: str = self.test_r_pop_025.__name__

	def test_r_pop_026(self):
		"""
		Get all elements except the last one (reverse)
		Set
		"""
		key: str = self.test_r_pop_026.__name__

	def test_r_pop_027(self):
		"""
		Get all elements except the last one (reverse)
		Frozenset
		"""
		key: str = self.test_r_pop_027.__name__

	# TODO - r_pop: count, reverse, все кроме последнего элемента


if __name__ == '__main__':
	unittest.main()
