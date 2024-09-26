from os import getenv
from dotenv import load_dotenv
from redis import Redis


class PyRedis:
    def __init__(self, psw, db=0, port=6379, host='localhost'):
        self.psw = psw
        self.db = db
        self.port = port
        self.host = host
        self.r = self.connect()

    def connect(self) -> Redis:
        return Redis(host=self.host, port=self.port, db=self.db, password=self.psw)

    def set(self, key, value):
        self.r.set(key, value)


load_dotenv()  # Load environment variables from .env file
redis_psw = getenv('REDIS_PSW')

r = Redis(host='localhost', port=6379, db=0, password=redis_psw)

r.set('first', 1)
print(r.get('first'))
