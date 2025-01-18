import unittest
from random import randint, choice
from string import ascii_letters, digits

from sys import path as sys_path
sys_path.append('../')
from src.client import PyRedis, redis_psw, redis_db, redis_host, redis_port


class SmokeTests(unittest.TestCase):
	r = PyRedis(redis_host, redis_port, redis_psw, db=redis_db, socket_timeout=.001)

	@staticmethod
	def get_random_integer():
		return randint(0, 1_000_000)

	@staticmethod
	def get_random_string(length: int = 10):
		return ''.join(choice(ascii_letters + digits) for _ in range(length))

	def test_ping(self):
		self.assertTrue(SmokeTests.r.r_ping())

	def test_set_get_001(self):
		value: int = SmokeTests.get_random_integer()
		self.assertIsNone(SmokeTests.r.r_set('test_1', value))
		res = SmokeTests.r.r_get('test_1')
		self.assertEqual(res, str(value).encode('utf-8'))
		self.assertEqual(int(res), value)

	def test_set_get_002(self):
		value: int = SmokeTests.get_random_integer()
		self.assertIsNone(SmokeTests.r.r_set('test_2', value))
		res = SmokeTests.r.r_get('test_2')
		self.assertEqual(res, str(value).encode('utf-8'))
		self.assertEqual(int(res), value)

	def test_set_get_003(self):
		value_1: str = SmokeTests.get_random_string()
		self.assertIsNone(SmokeTests.r.r_set('test_3', value_1))
		res_1 = SmokeTests.r.r_get('test_3')
		self.assertEqual(res_1, value_1.encode('utf-8'))

		# rewrite
		value_2: str = SmokeTests.get_random_string()
		self.assertIsNone(SmokeTests.r.r_set('test_3', value_2))
		res_2 = SmokeTests.r.r_get('test_3')
		self.assertEqual(res_2, value_2.encode('utf-8'))

	def test_set_get_delete_004(self):
		value: int = SmokeTests.get_random_integer()

		self.assertIsNone(SmokeTests.r.r_set('test_004', value))
		res_1 = SmokeTests.r.r_get('test_004')
		self.assertEqual(res_1, str(value).encode('utf-8'))
		self.assertEqual(int(res_1), value)

		# delete (without returning - None)
		self.assertIsNone(SmokeTests.r.r_delete('test_004'))
		self.assertIsNone(SmokeTests.r.r_get('test_004'))

		res_2 = SmokeTests.r.r_get('test_004')
		self.assertIsNone(res_2)

	def test_set_get_delete_005(self):
		value: int = SmokeTests.get_random_integer()

		self.assertIsNone(SmokeTests.r.r_set('test_005', value))
		res_1 = SmokeTests.r.r_get('test_005')
		self.assertEqual(res_1, str(value).encode('utf-8'))
		self.assertEqual(int(res_1), value)

		# delete (without returning - False)
		self.assertIsNone(SmokeTests.r.r_delete('test_005', returning=False))
		self.assertIsNone(SmokeTests.r.r_get('test_005'))

		res_2 = SmokeTests.r.r_get('test_005')
		self.assertIsNone(res_2)

	def test_set_get_delete_006(self):
		value: str = SmokeTests.get_random_string()

		self.assertIsNone(SmokeTests.r.r_set('test_006', value))
		res_1 = SmokeTests.r.r_get('test_006')
		self.assertEqual(res_1, value.encode('utf-8'))

		# delete (with returning)
		self.assertEqual(SmokeTests.r.r_delete('test_006', returning=True), value.encode('utf-8'))
		self.assertIsNone(SmokeTests.r.r_get('test_006'))

		res_2 = SmokeTests.r.r_get('test_006')
		self.assertIsNone(res_2)


if __name__ == '__main__':
	unittest.main()
