import unittest

from src.client import PyRedis, redis_psw, redis_db, redis_host, redis_port


class SmokeTests(unittest.TestCase):
	def test_ping_001(self):
		r = PyRedis(redis_host, redis_port, redis_psw, db=redis_db, socket_timeout=.001)
		self.assertTrue(r.r_ping())


if __name__ == '__main__':
	unittest.main()
