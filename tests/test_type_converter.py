import unittest
from redis import Redis, ConnectionPool
from random import randint, choice, random, shuffle
from string import ascii_letters, digits
from sys import path as sys_path

from connection_params import REDIS_PWS, REDIS_HOST, REDIS_PORT, REDIS_USERNAME

sys_path.append('../')
from src.data_type_converter import TypeConverter
from src.client import PyRedis

redis_db: int = 0


class TypeConverterTest(unittest.TestCase):
	""" Checking private functions of PyRedis class """

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

	t = TypeConverter()

	original_redis = Redis(connection_pool=ConnectionPool(
		host=REDIS_HOST, port=REDIS_PORT, db=redis_db, password=REDIS_PWS, username=REDIS_USERNAME
	))

	@staticmethod
	def clear_dictionaries():
		TypeConverterTest.r.lua_scripts_sha.clear()
		TypeConverterTest.r.user_lua_scripts_buffer.clear()

	@classmethod
	def setUpClass(cls):
		cls.clear_dictionaries()
		TypeConverterTest.original_redis.flushdb()  # clear the database before tests

	@classmethod
	def tearDownClass(cls):
		cls.clear_dictionaries()
		TypeConverterTest.original_redis.flushdb()  # clear the database after tests

	@staticmethod
	def get_random_integer():
		return randint(0, 1_000_000)

	@staticmethod
	def get_random_string(length: int = randint(10, 20)):
		return ''.join(choice(ascii_letters + digits) for _ in range(length))

	def test_ping(self):
		""" Service is available """
		self.assertTrue(TypeConverterTest.r.r_ping())

	# converter ################################################################################################

	def test_convert_to_type_001(self):
		value: int = 0
		res: int = TypeConverterTest.t.converter(str(value), 'int')
		self.assertEqual(value, res)

	def test_convert_to_type_002(self):
		value: int = randint(1, 100)
		res: int = TypeConverterTest.t.converter(str(value), 'int')
		self.assertEqual(value, res)

	def test_convert_to_type_003(self):
		value: int = randint(1, 100)
		res: int = TypeConverterTest.t.converter(str(value), 'integer')
		self.assertEqual(value, res)

	def test_convert_to_type_004(self):
		value: bool = True
		res: bool = TypeConverterTest.t.converter(str(value), 'bool')
		self.assertEqual(value, res)

	def test_convert_to_type_005(self):
		value: bool = False
		res: bool = TypeConverterTest.t.converter(str(value), 'boolean')
		self.assertEqual(value, res)

	def test_convert_to_type_006(self):
		value: bool = False
		res: bool = TypeConverterTest.t.converter(str(value), 'bool')
		self.assertEqual(value, res)

	def test_convert_to_type_007(self):
		value: bool = True
		res: bool = TypeConverterTest.t.converter(str(value), 'boolean')
		self.assertEqual(value, res)

	def test_convert_to_type_008(self):
		value: bool = True
		res: str = TypeConverterTest.t.converter(str(value), '')
		self.assertEqual(str(value), res)

	def test_convert_to_type_009(self):
		value: bool = False
		res: str = TypeConverterTest.t.converter(str(value), '')
		self.assertEqual(str(value), res)

	def test_convert_to_type_010(self):
		value: int = randint(100_000, 1_000_000)
		res: str = TypeConverterTest.t.converter(str(value), 'integer')
		self.assertEqual(value, res)

	def test_convert_to_type_011(self):
		value: float = float(randint(0, 100)) + random()
		res: str = TypeConverterTest.t.converter(str(value), 'qwerty')
		self.assertEqual(str(value), res)

	def test_convert_to_type_012(self):
		value: float = float(randint(0, 100)) + random()
		res: str = TypeConverterTest.t.converter(str(value), 'float')
		self.assertEqual(value, res)

	def test_convert_to_type_013(self):
		""" boolean array <-> bool """
		expected_res: list[bool] = [bool(randint(0, 1)) for _ in range(50)]
		value: list[str] = [str(val) for val in expected_res]
		res: list[bool] = TypeConverterTest.t.converter(value, 'bool')
		self.assertEqual(res, expected_res)

	def test_convert_to_type_014(self):
		""" boolean array <-> boolean """
		expected_res: list[bool] = [bool(randint(0, 1)) for _ in range(50)]
		value: list[str] = [str(val) for val in expected_res]
		res: list[bool] = TypeConverterTest.t.converter(value, 'boolean')
		self.assertEqual(res, expected_res)

	def test_convert_to_type_015(self):
		""" float array <-> float """
		expected_res: list[float] = [random() for _ in range(50)]
		value: list[str] = [str(val) for val in expected_res]
		res: list[float] = TypeConverterTest.t.converter(value, 'float')
		self.assertEqual(res, expected_res)

	def test_convert_to_type_016(self):
		""" float array <-> numeric """
		expected_res: list[float] = [random() for _ in range(50)]
		value: list[str] = [str(val) for val in expected_res]
		res: list[float] = TypeConverterTest.t.converter(value, 'numeric')
		self.assertEqual(res, expected_res)

	def test_convert_to_type_017(self):
		""" float array <-> double """
		expected_res: list[float] = [random() for _ in range(50)]
		value: list[str] = [str(val) for val in expected_res]
		res: list[float] = TypeConverterTest.t.converter(value, 'double')
		self.assertEqual(res, expected_res)

	def test_convert_to_type_018(self):
		""" bool array -> int """
		expected_res: list[bool] = [bool(randint(0, 1)) for _ in range(50)]
		value: list[str] = [str(val) for val in expected_res]
		res: list[str] = TypeConverterTest.t.converter(value, 'integer')
		self.assertEqual(res, value)

	def test_convert_to_type_019(self):
		""" integer values with str """
		int_lst: list[int] = [TypeConverterTest.get_random_integer() for _ in range(50)]
		str_lst: list[str] = [TypeConverterTest.get_random_string() for _ in range(50)]
		merge_lists: list = int_lst + str_lst
		shuffle(merge_lists)  # shuffle the values in the list
		value: list[str] = [str(val) for val in merge_lists]
		res: list[int | str] = TypeConverterTest.t.converter(value, 'int_any')
		self.assertEqual(set(res), set(merge_lists))  # it`s more convenient to compare shuffled lists through sets

	def test_convert_to_type_020(self):
		""" integer values with bool """
		int_lst: list[int] = [TypeConverterTest.get_random_integer() for _ in range(50)]
		bool_lst: list[bool] = [bool(randint(0, 1)) for _ in range(50)]
		merge_lists: list = int_lst + bool_lst
		shuffle(merge_lists)
		expected_res = [(str(val) if not isinstance(val, bool) else val) for val in merge_lists]
		value: list[str] = [str(val) for val in merge_lists]
		res: list[bool | str] = TypeConverterTest.t.converter(value, 'bool')
		self.assertEqual(set(res), set(expected_res))  # because of set there will be 1 True and 1 False

	def test_convert_to_type_021(self):
		""" Check extended """
		value: list[str] = ['1', 'abc', '0', 'qwerty', '123']

		res = TypeConverterTest.t.converter(value, 'int')
		self.assertEqual(res, value)

		res = TypeConverterTest.t.converter(value, 'int_any')
		self.assertEqual(res, [1, 'abc', 0, 'qwerty', 123])

		res = TypeConverterTest.t.converter(value, 'float_any')
		self.assertEqual(res, [1.0, 'abc', 0.0, 'qwerty', 123.0])

		res = TypeConverterTest.t.converter(value, 'bool')
		self.assertEqual(res, [True, 'abc', False, 'qwerty', '123'])

		res = TypeConverterTest.t.converter(value, 'bool_any')
		self.assertEqual(res, [True, 'abc', False, 'qwerty', '123'])

	def test_convert_to_type_022(self):
		""" Check extended """
		value: list[str] = ['1', 'key', '0.5', 'jquery', 'reactOS', '12_500', 'True', 'False', 'cat_and_dog']

		res = TypeConverterTest.t.converter(value, 'integer')
		self.assertEqual(res, value)

		res = TypeConverterTest.t.converter(value, 'integer_any')
		self.assertEqual(res, [1, 'key', 0, 'jquery', 'reactOS', 12500, 'True', 'False', 'cat_and_dog'])

		res = TypeConverterTest.t.converter(value, 'numeric')
		self.assertEqual(res, value)

		res = TypeConverterTest.t.converter(value, 'double_any')
		self.assertEqual(res, [1.0, 'key', 0.5, 'jquery', 'reactOS', 12500.0, 'True', 'False', 'cat_and_dog'])

		res = TypeConverterTest.t.converter(value, 'bool')
		self.assertEqual(res, [True, 'key', '0.5', 'jquery', 'reactOS', '12_500', True, False, 'cat_and_dog'])

		res = TypeConverterTest.t.converter(value, 'bool_any')
		self.assertEqual(res, [True, 'key', '0.5', 'jquery', 'reactOS', '12_500', True, False, 'cat_and_dog'])

	def test_helper_convert_to_type_001(self):
		value: int = 0
		res: int = TypeConverterTest.t.converter(str(value), 'int')
		self.assertEqual(value, res)

	def test_helper_convert_to_type_002(self):
		value: int = randint(1, 100)
		res: int = TypeConverterTest.t.converter(str(value), 'int')
		self.assertEqual(value, res)

	def test_helper_convert_to_type_003(self):
		value: int = randint(1, 100)
		res: int = TypeConverterTest.t.converter(str(value), 'integer')
		self.assertEqual(value, res)

	def test_helper_convert_to_type_004(self):
		value: bool = True
		res: bool = TypeConverterTest.t.converter(str(value), 'bool')
		self.assertEqual(value, res)

	def test_helper_convert_to_type_005(self):
		value: bool = False
		res: bool = TypeConverterTest.t.converter(str(value), 'boolean')
		self.assertEqual(value, res)

	def test_helper_convert_to_type_006(self):
		value: bool = False
		res: bool = TypeConverterTest.t.converter(str(value), 'bool')
		self.assertEqual(value, res)

	def test_helper_convert_to_type_007(self):
		value: bool = True
		res: bool = TypeConverterTest.t.converter(str(value), 'boolean')
		self.assertEqual(value, res)

	def test_helper_convert_to_type_008(self):
		value: bool = True
		res: str = TypeConverterTest.t.converter(str(value), '')
		self.assertEqual(str(value), res)

	def test_helper_convert_to_type_009(self):
		value: bool = False
		res: str = TypeConverterTest.t.converter(str(value), '')
		self.assertEqual(str(value), res)

	def test_helper_convert_to_type_010(self):
		value: bool = True
		res: str = TypeConverterTest.t.converter(str(value), 'integer')
		self.assertEqual(str(value), res)

	def test_helper_convert_to_type_011(self):
		value: bool = False
		res: str = TypeConverterTest.t.converter(str(value), 'float')
		self.assertEqual(str(value), res)

	def test_helper_convert_to_type_012(self):
		value: int = randint(100_000, 1_000_000)
		res: str = TypeConverterTest.t.converter(str(value), 'integer')
		self.assertEqual(value, res)

	def test_helper_convert_to_type_013(self):
		value: float = float(randint(0, 100)) + random()
		res: str = TypeConverterTest.t.converter(str(value), 'qwerty')
		self.assertEqual(str(value), res)

	def test_helper_convert_to_type_014(self):
		value: float = float(randint(0, 100)) + random()
		res: str = TypeConverterTest.t.converter(str(value), 'float')
		self.assertEqual(value, res)

	def test_helper_convert_to_type_015(self):
		value: float = float(randint(0, 100)) + random()
		res: str = TypeConverterTest.t.converter(str(value), 'numeric')
		self.assertEqual(value, res)

	def test_helper_convert_to_type_016(self):
		value: float = float(randint(0, 100)) + random()
		res: str = TypeConverterTest.t.converter(str(value), 'double')
		self.assertEqual(value, res)

	def test_helper_convert_to_type_017(self):
		value: float = float(0)
		res: str = TypeConverterTest.t.converter(str(value), 'float')
		self.assertEqual(value, res)

	def test_helper_convert_to_type_018(self):
		value: float = float(0)
		res: str = TypeConverterTest.t.converter(str(value), 'numeric')
		self.assertEqual(value, res)

	def test_helper_convert_to_type_019(self):
		value: float = float(0)
		res: str = TypeConverterTest.t.converter(str(value), 'double')
		self.assertEqual(value, res)

	def test_helper_convert_to_type_020(self):
		value: float = random()
		res: str = TypeConverterTest.t.converter(str(value), 'double')
		self.assertEqual(value, res)


if __name__ == '__main__':
	unittest.main()
