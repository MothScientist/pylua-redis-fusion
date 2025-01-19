import unittest
from dotenv import load_dotenv
from os import getenv
from random import randint, choice
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
	def get_random_string(length: int = 10):
		return ''.join(choice(ascii_letters + digits) for _ in range(length))

	def test_ping(self):
		self.assertTrue(SmokeTests.r.r_ping())

	def test_set_get_001(self):
		value: int = SmokeTests.get_random_integer()
		self.assertIsNone(SmokeTests.r.r_set('test_1', value))
		res = SmokeTests.r.r_get('test_1')
		self.assertEqual(int(res), value)

	def test_set_get_002(self):
		value: int = SmokeTests.get_random_integer()
		self.assertIsNone(SmokeTests.r.r_set('test_2', value))
		res = SmokeTests.r.r_get('test_2')
		self.assertEqual(int(res), value)

	def test_set_get_003(self):
		value_1: str = SmokeTests.get_random_string()
		self.assertIsNone(SmokeTests.r.r_set('test_3', value_1))
		res_1 = SmokeTests.r.r_get('test_3')
		self.assertEqual(res_1, value_1)

		# rewrite
		value_2: str = SmokeTests.get_random_string()
		self.assertIsNone(SmokeTests.r.r_set('test_3', value_2))
		res_2 = SmokeTests.r.r_get('test_3')
		self.assertEqual(res_2, value_2)

	def test_set_get_delete_004(self):
		value: int = SmokeTests.get_random_integer()

		self.assertIsNone(SmokeTests.r.r_set('test_004', value))
		res_1 = SmokeTests.r.r_get('test_004')
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
		self.assertEqual(res_1, value)

		# delete (without returning - False)
		self.assertIsNone(SmokeTests.r.r_delete('test_006', returning=False))
		self.assertIsNone(SmokeTests.r.r_get('test_006'))

		res_2 = SmokeTests.r.r_get('test_006')
		self.assertIsNone(res_2)

	def test_set_get_delete_007(self):
		value: int = SmokeTests.get_random_integer()

		self.assertIsNone(SmokeTests.r.r_set('test_007', value))
		res_1 = SmokeTests.r.r_get('test_007')
		self.assertEqual(res_1, str(value))

		# delete (with returning)
		self.assertEqual(SmokeTests.r.r_delete('test_007', returning=True), str(value))
		self.assertIsNone(SmokeTests.r.r_get('test_007'))

		res_2 = SmokeTests.r.r_get('test_007')
		self.assertIsNone(res_2)

	def test_set_get_delete_008(self):
		value: str = SmokeTests.get_random_string()

		self.assertIsNone(SmokeTests.r.r_set('test_008', value))
		res_1 = SmokeTests.r.r_get('test_008')
		self.assertEqual(res_1, value)

		# delete (with returning)
		self.assertEqual(SmokeTests.r.r_delete('test_008', returning=True), value)
		self.assertIsNone(SmokeTests.r.r_get('test_008'))

		res_2 = SmokeTests.r.r_get('test_008')
		self.assertIsNone(res_2)

	def test_cycle_set_get_delete_009(self):
		for value, key in enumerate([i for i in range(100_000_000, 100_000_000 + randint(500, 1_000))]):
			key = str(key)
			str_value = str(value)
			self.assertIsNone(SmokeTests.r.r_set(key, value))
			self.assertEqual(SmokeTests.r.r_get(key), str_value)
			self.assertEqual(SmokeTests.r.r_delete(key, returning=True), str_value)
			self.assertIsNone(SmokeTests.r.r_get(key))

	def test_r_mass_check_keys_exists_010(self):
		keys: list = list({SmokeTests.get_random_string(length=randint(5, 15)) for _ in range(randint(50, 100))})
		for key in keys:
			SmokeTests.r.r_set(key, randint(0, 10_000))
		non_exist: tuple = tuple({SmokeTests.get_random_string(length=randint(1, 3)) for _ in range(randint(5, 10))})
		res: list = list(SmokeTests.r.r_mass_check_keys_exists({*keys, *non_exist}))

		keys.sort()
		res.sort()

		self.assertEqual(res, keys, f'len(res) = {len(res)}; len(keys) = {len(keys)}')


if __name__ == '__main__':
	unittest.main()
