import unittest
from random import randint, choice, random, shuffle
from string import ascii_letters, digits
from sys import path as sys_path

sys_path.append('../')
from src.client import PyRedis


class PrivateStaticFuncTests(unittest.TestCase):
	""" Checking private functions of PyRedis class """

	load_lua_func_obj = PyRedis._PyRedis__load_lua_script  # noqa
	time_func_obj = PyRedis._PyRedis__compare_and_select_sec_ms  # noqa
	remove_duplicates_func_obj = PyRedis._PyRedis__remove_duplicates  # noqa
	convert_func_obj = PyRedis._PyRedis__convert_to_type  # noqa
	helper_convert_func_obj = PyRedis._PyRedis__helper_convert_to_type  # noqa

	@staticmethod
	def get_random_integer(_min: int = 0, _max: int = 100):
		return randint(_min, _max)

	@staticmethod
	def get_random_string(length: int = randint(5, 10)):
		return ''.join(choice(ascii_letters + digits) for _ in range(length))

	# __compare_and_select_sec_ms ######################################################################################

	def test_compare_and_select_sec_ms_001(self):
		res = PrivateStaticFuncTests.time_func_obj(1, 1_000)
		self.assertEqual(res, 1_000)

	def test_compare_and_select_sec_ms_002(self):
		res = PrivateStaticFuncTests.time_func_obj(1, 1_200)
		self.assertEqual(res, 1_000)

	def test_compare_and_select_sec_ms_003(self):
		res = PrivateStaticFuncTests.time_func_obj(2, 250)
		self.assertEqual(res, 250)

	def test_compare_and_select_sec_ms_004(self):
		res = PrivateStaticFuncTests.time_func_obj(0, 250)
		self.assertEqual(res, 250)

	def test_compare_and_select_sec_ms_005(self):
		res = PrivateStaticFuncTests.time_func_obj(1, 0)
		self.assertEqual(res, 1_000)

	def test_compare_and_select_sec_ms_006(self):
		res = PrivateStaticFuncTests.time_func_obj(0, 0)
		self.assertEqual(res, 0)

	def test_compare_and_select_sec_ms_007(self):
		res = PrivateStaticFuncTests.time_func_obj(1.5, 1_550)
		self.assertEqual(res, 1_500)

	def test_compare_and_select_sec_ms_008(self):
		res = PrivateStaticFuncTests.time_func_obj(1_000, 1_010)
		self.assertEqual(res, 1_010)

	def test_compare_and_select_sec_ms_009(self):
		res = PrivateStaticFuncTests.time_func_obj(1_000, 1_000_001)
		self.assertEqual(res, 1_000_000)

	def test_compare_and_select_sec_ms_010(self):
		res = PrivateStaticFuncTests.time_func_obj(0.001, 1)
		self.assertEqual(res, 1)

	def test_compare_and_select_sec_ms_011(self):
		res = PrivateStaticFuncTests.time_func_obj(0.0011, 1)
		self.assertEqual(res, 1)

	def test_compare_and_select_sec_ms_012(self):
		res = PrivateStaticFuncTests.time_func_obj(0.001, 0.99)
		self.assertEqual(res, 0.99)

	def test_compare_and_select_sec_ms_013(self):
		res = PrivateStaticFuncTests.time_func_obj(0, 1_000)
		self.assertEqual(res, 1_000)

	def test_compare_and_select_sec_ms_014(self):
		res = PrivateStaticFuncTests.time_func_obj(0.1, 0)
		self.assertEqual(res, 100)

	# __remove_duplicates ##############################################################################################

	def test_remove_duplicates_001(self):
		arr = [PrivateStaticFuncTests.get_random_integer(_min=0, _max=10) for _ in range(50)]
		res = PrivateStaticFuncTests.remove_duplicates_func_obj(arr)
		self.assertEqual(res, tuple(set(arr)))

	def test_remove_duplicates_002(self):
		arr = tuple([PrivateStaticFuncTests.get_random_integer() for _ in range(250)])
		res = PrivateStaticFuncTests.remove_duplicates_func_obj(arr)
		self.assertEqual(res, tuple(set(arr)))

	def test_remove_duplicates_003(self):
		arr = set([PrivateStaticFuncTests.get_random_integer(_min=25, _max=50) for _ in range(100)])
		res = PrivateStaticFuncTests.remove_duplicates_func_obj(arr)
		self.assertEqual(res, tuple(arr))

	def test_remove_duplicates_004(self):
		""" Empty list """
		arr = []
		res = PrivateStaticFuncTests.remove_duplicates_func_obj(arr)
		self.assertEqual(res, tuple(arr))

	def test_remove_duplicates_005(self):
		""" Empty tuple """
		arr = tuple()
		res = PrivateStaticFuncTests.remove_duplicates_func_obj(arr)
		self.assertEqual(res, arr)

	def test_remove_duplicates_006(self):
		""" Empty set """
		arr = set()
		res = PrivateStaticFuncTests.remove_duplicates_func_obj(arr)
		self.assertEqual(res, tuple(arr))

	def test_remove_duplicates_007(self):
		""" Empty frozenset """
		arr = frozenset()
		res = PrivateStaticFuncTests.remove_duplicates_func_obj(arr)
		self.assertEqual(res, tuple(arr))

	def test_remove_duplicates_008(self):
		arr = tuple([PrivateStaticFuncTests.get_random_string(length=1) for _ in range(1_000)])
		res = PrivateStaticFuncTests.remove_duplicates_func_obj(arr)
		self.assertEqual(res, tuple(set(arr)))

	def test_remove_duplicates_009(self):
		arr = [PrivateStaticFuncTests.get_random_string() for _ in range(500)]
		res = PrivateStaticFuncTests.remove_duplicates_func_obj(arr)
		self.assertEqual(res, tuple(set(arr)))

	def test_remove_duplicates_010(self):
		arr = tuple([PrivateStaticFuncTests.get_random_string(length=randint(1, 10)) for _ in range(250)])
		res = PrivateStaticFuncTests.remove_duplicates_func_obj(arr)
		self.assertEqual(res, tuple(set(arr)))

	def test_remove_duplicates_011(self):
		arr = tuple([0 for _ in range(100)])
		res = PrivateStaticFuncTests.remove_duplicates_func_obj(arr)
		self.assertEqual(res, tuple(set(arr)))

	def test_remove_duplicates_012(self):
		_int: int = randint(1, 100)
		arr = tuple([_int for _ in range(100)])
		res = PrivateStaticFuncTests.remove_duplicates_func_obj(arr)
		self.assertEqual(res, tuple(set(arr)))

	# __convert_to_type ################################################################################################

	def test_convert_to_type_001(self):
		value: int = 0
		res: int = PrivateStaticFuncTests.convert_func_obj(str(value), 'int')
		self.assertEqual(value, res)

	def test_convert_to_type_002(self):
		value: int = randint(1, 100)
		res: int = PrivateStaticFuncTests.convert_func_obj(str(value), 'int')
		self.assertEqual(value, res)

	def test_convert_to_type_003(self):
		value: int = randint(1, 100)
		res: int = PrivateStaticFuncTests.convert_func_obj(str(value), 'integer')
		self.assertEqual(value, res)

	def test_convert_to_type_004(self):
		value: bool = True
		res: bool = PrivateStaticFuncTests.convert_func_obj(str(value), 'bool')
		self.assertEqual(value, res)

	def test_convert_to_type_005(self):
		value: bool = False
		res: bool = PrivateStaticFuncTests.convert_func_obj(str(value), 'boolean')
		self.assertEqual(value, res)

	def test_convert_to_type_006(self):
		value: bool = False
		res: bool = PrivateStaticFuncTests.convert_func_obj(str(value), 'bool')
		self.assertEqual(value, res)

	def test_convert_to_type_007(self):
		value: bool = True
		res: bool = PrivateStaticFuncTests.convert_func_obj(str(value), 'boolean')
		self.assertEqual(value, res)

	def test_convert_to_type_008(self):
		value: bool = True
		res: str = PrivateStaticFuncTests.convert_func_obj(str(value), '')
		self.assertEqual(str(value), res)

	def test_convert_to_type_009(self):
		value: bool = False
		res: str = PrivateStaticFuncTests.convert_func_obj(str(value), '')
		self.assertEqual(str(value), res)

	def test_convert_to_type_010(self):
		value: int = randint(100_000, 1_000_000)
		res: str = PrivateStaticFuncTests.convert_func_obj(str(value), 'integer')
		self.assertEqual(value, res)

	def test_convert_to_type_011(self):
		value: float = float(randint(0, 100)) + random()
		res: str = PrivateStaticFuncTests.convert_func_obj(str(value), 'qwerty')
		self.assertEqual(str(value), res)

	def test_convert_to_type_012(self):
		value: float = float(randint(0, 100)) + random()
		res: str = PrivateStaticFuncTests.convert_func_obj(str(value), 'float')
		self.assertEqual(value, res)

	def test_convert_to_type_013(self):
		""" boolean array <-> bool """
		expected_res: list[bool] = [bool(randint(0, 1)) for _ in range(50)]
		value: list[str] = [str(val) for val in expected_res]
		res: list[bool] = PrivateStaticFuncTests.convert_func_obj(value, 'bool')
		self.assertEqual(res, expected_res)

	def test_convert_to_type_014(self):
		""" boolean array <-> boolean """
		expected_res: list[bool] = [bool(randint(0, 1)) for _ in range(50)]
		value: list[str] = [str(val) for val in expected_res]
		res: list[bool] = PrivateStaticFuncTests.convert_func_obj(value, 'boolean')
		self.assertEqual(res, expected_res)

	def test_convert_to_type_015(self):
		""" float array <-> float """
		expected_res: list[float] = [random() for _ in range(50)]
		value: list[str] = [str(val) for val in expected_res]
		res: list[float] = PrivateStaticFuncTests.convert_func_obj(value, 'float')
		self.assertEqual(res, expected_res)

	def test_convert_to_type_016(self):
		""" float array <-> numeric """
		expected_res: list[float] = [random() for _ in range(50)]
		value: list[str] = [str(val) for val in expected_res]
		res: list[float] = PrivateStaticFuncTests.convert_func_obj(value, 'numeric')
		self.assertEqual(res, expected_res)

	def test_convert_to_type_017(self):
		""" float array <-> double """
		expected_res: list[float] = [random() for _ in range(50)]
		value: list[str] = [str(val) for val in expected_res]
		res: list[float] = PrivateStaticFuncTests.convert_func_obj(value, 'double')
		self.assertEqual(res, expected_res)

	def test_convert_to_type_018(self):
		""" bool array -> int """
		expected_res: list[bool] = [bool(randint(0, 1)) for _ in range(50)]
		value: list[str] = [str(val) for val in expected_res]
		res: list[str] = PrivateStaticFuncTests.convert_func_obj(value, 'integer')
		self.assertEqual(res, value)

	def test_convert_to_type_019(self):
		""" integer values with str """
		int_lst: list[int] = [PrivateStaticFuncTests.get_random_integer() for _ in range(50)]
		str_lst: list[str] = [PrivateStaticFuncTests.get_random_string() for _ in range(50)]
		merge_lists: list = int_lst + str_lst
		shuffle(merge_lists)  # shuffle the values in the list
		value: list[str] = [str(val) for val in merge_lists]
		res: list[int | str] = PrivateStaticFuncTests.convert_func_obj(value, 'int')
		self.assertEqual(set(res), set(merge_lists))  # it`s more convenient to compare shuffled lists through sets

	def test_convert_to_type_020(self):
		""" integer values with bool """
		int_lst: list[int] = [PrivateStaticFuncTests.get_random_integer(_min=2) for _ in range(50)]
		bool_lst: list[bool] = [bool(randint(0, 1)) for _ in range(50)]
		merge_lists: list = int_lst + bool_lst
		shuffle(merge_lists)
		expected_res = [(str(val) if not isinstance(val, bool) else val) for val in merge_lists]
		value: list[str] = [str(val) for val in merge_lists]
		res: list[bool | str] = PrivateStaticFuncTests.convert_func_obj(value, 'bool')
		self.assertEqual(set(res), set(expected_res))  # because of set there will be 1 True and 1 False

	# __helper_convert_to_type #########################################################################################

	def test_helper_convert_to_type_001(self):
		value: int = 0
		res: int = PrivateStaticFuncTests.helper_convert_func_obj(str(value), 'int')
		self.assertEqual(value, res)

	def test_helper_convert_to_type_002(self):
		value: int = randint(1, 100)
		res: int = PrivateStaticFuncTests.helper_convert_func_obj(str(value), 'int')
		self.assertEqual(value, res)

	def test_helper_convert_to_type_003(self):
		value: int = randint(1, 100)
		res: int = PrivateStaticFuncTests.helper_convert_func_obj(str(value), 'integer')
		self.assertEqual(value, res)

	def test_helper_convert_to_type_004(self):
		value: bool = True
		res: bool = PrivateStaticFuncTests.helper_convert_func_obj(str(value), 'bool')
		self.assertEqual(value, res)

	def test_helper_convert_to_type_005(self):
		value: bool = False
		res: bool = PrivateStaticFuncTests.helper_convert_func_obj(str(value), 'boolean')
		self.assertEqual(value, res)

	def test_helper_convert_to_type_006(self):
		value: bool = False
		res: bool = PrivateStaticFuncTests.helper_convert_func_obj(str(value), 'bool')
		self.assertEqual(value, res)

	def test_helper_convert_to_type_007(self):
		value: bool = True
		res: bool = PrivateStaticFuncTests.helper_convert_func_obj(str(value), 'boolean')
		self.assertEqual(value, res)

	def test_helper_convert_to_type_008(self):
		value: bool = True
		res: str = PrivateStaticFuncTests.helper_convert_func_obj(str(value), '')
		self.assertEqual(str(value), res)

	def test_helper_convert_to_type_009(self):
		value: bool = False
		res: str = PrivateStaticFuncTests.helper_convert_func_obj(str(value), '')
		self.assertEqual(str(value), res)

	def test_helper_convert_to_type_010(self):
		value: bool = True
		res: str = PrivateStaticFuncTests.helper_convert_func_obj(str(value), 'integer')
		self.assertEqual(str(value), res)

	def test_helper_convert_to_type_011(self):
		value: bool = False
		res: str = PrivateStaticFuncTests.helper_convert_func_obj(str(value), 'float')
		self.assertEqual(str(value), res)

	def test_helper_convert_to_type_012(self):
		value: int = randint(100_000, 1_000_000)
		res: str = PrivateStaticFuncTests.helper_convert_func_obj(str(value), 'integer')
		self.assertEqual(value, res)

	def test_helper_convert_to_type_013(self):
		value: float = float(randint(0, 100)) + random()
		res: str = PrivateStaticFuncTests.helper_convert_func_obj(str(value), 'qwerty')
		self.assertEqual(str(value), res)

	def test_helper_convert_to_type_014(self):
		value: float = float(randint(0, 100)) + random()
		res: str = PrivateStaticFuncTests.helper_convert_func_obj(str(value), 'float')
		self.assertEqual(value, res)

	def test_helper_convert_to_type_015(self):
		value: float = float(randint(0, 100)) + random()
		res: str = PrivateStaticFuncTests.helper_convert_func_obj(str(value), 'numeric')
		self.assertEqual(value, res)

	def test_helper_convert_to_type_016(self):
		value: float = float(randint(0, 100)) + random()
		res: str = PrivateStaticFuncTests.helper_convert_func_obj(str(value), 'double')
		self.assertEqual(value, res)

	def test_helper_convert_to_type_017(self):
		value: float = float(0)
		res: str = PrivateStaticFuncTests.helper_convert_func_obj(str(value), 'double')
		self.assertEqual(value, res)

	def test_helper_convert_to_type_018(self):
		value: float = random()
		res: str = PrivateStaticFuncTests.helper_convert_func_obj(str(value), 'double')
		self.assertEqual(value, res)


if __name__ == '__main__':
	unittest.main()
