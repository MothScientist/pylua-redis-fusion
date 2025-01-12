import unittest

from ..src.client import PyRedis, redis_psw, redis_db, redis_host, redis_port


class SmokeTests(unittest.TestCase):
	r = PyRedis(redis_host, redis_port, redis_psw, db=redis_db, socket_timeout=.001)

	def test_ping(self):
		self.assertTrue(SmokeTests.r.r_ping())


if __name__ == '__main__':
	unittest.main()
