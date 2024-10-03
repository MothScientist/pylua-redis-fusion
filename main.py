from os import getenv
from dotenv import load_dotenv
from redis import Redis

class PyRedis:
    def __init__(self, psw, db=0, port=6379, host='localhost'):
        self.psw = psw
        self.db = db  # database number
        self.port = port
        self.host = host
        self.redis = self._connect()

    def _connect(self) -> Redis:
        return Redis(host=self.host, port=self.port, db=self.db, password=self.psw)

    def set(self, key, value) -> None:
        self.redis.set(key, value)

    def get(self, key):
        return self.redis.get(key)

    def delete(self, key) -> None:
        self.redis.delete(key)


load_dotenv('redis.env')  # Load environment variables from redis.env file
redis_psw: str = getenv('REDIS_PSW')
redis_db: int = int(getenv('REDIS_DB'))
redis_host: str = getenv('REDIS_HOST')
redis_port: int = int(getenv('REDIS_PORT'))

r = Redis(host=redis_host, port=redis_port, db=redis_db, password=redis_psw)

r.set('first', 1)
print(r.get('first'))
r.delete('first')
print(r.get('first'))
