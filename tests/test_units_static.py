import unittest
from random import randint, choice, random, shuffle
from string import ascii_letters, digits
from sys import path as sys_path

sys_path.append('../')
from pyluaredis.client import PyRedis


class PrivateStaticFuncTests(unittest.TestCase):
	""" Checking private functions of PyRedis class """

	time_func_obj = PyRedis._PyRedis__compare_and_select_sec_ms  # noqa
	remove_duplicates_func_obj = PyRedis._PyRedis__remove_duplicates  # noqa

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
		self.assertEqual(res, None)

	def test_compare_and_select_sec_ms_007(self):
		res = PrivateStaticFuncTests.time_func_obj(15, 1_550)
		self.assertEqual(res, 1_550)

	def test_compare_and_select_sec_ms_008(self):
		res = PrivateStaticFuncTests.time_func_obj(1_000, 1_010)
		self.assertEqual(res, 1_010)

	def test_compare_and_select_sec_ms_009(self):
		res = PrivateStaticFuncTests.time_func_obj(1_000, 1_000_001)
		self.assertEqual(res, 1_000_000)

	def test_compare_and_select_sec_ms_010(self):
		res = PrivateStaticFuncTests.time_func_obj(1, 2000)
		self.assertEqual(res, 1000)

	def test_compare_and_select_sec_ms_011(self):
		res = PrivateStaticFuncTests.time_func_obj(0, 1_000)
		self.assertEqual(res, 1_000)

	def test_compare_and_select_sec_ms_012(self):
		res = PrivateStaticFuncTests.time_func_obj(1, 0)
		self.assertEqual(res, 1000)

	def test_compare_and_select_sec_ms_013(self):
		res = PrivateStaticFuncTests.time_func_obj(1, None)
		self.assertEqual(res, 1000)

	def test_compare_and_select_sec_ms_014(self):
		res = PrivateStaticFuncTests.time_func_obj(None, 100)
		self.assertEqual(res, 100)

	def test_compare_and_select_sec_ms_015(self):
		res = PrivateStaticFuncTests.time_func_obj(None, None)
		self.assertEqual(res, None)

	def test_compare_and_select_sec_ms_016(self):
		res = PrivateStaticFuncTests.time_func_obj(0, None)
		self.assertEqual(res, None)

	def test_compare_and_select_sec_ms_017(self):
		res = PrivateStaticFuncTests.time_func_obj(None, 0)
		self.assertEqual(res, None)

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


if __name__ == '__main__':
	unittest.main()
