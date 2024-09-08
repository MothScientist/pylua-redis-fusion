from os import getenv
from dotenv import load_dotenv
import redis


load_dotenv()  # Load environment variables from .env file
redis_psw = getenv('REDIS_PSW')

r = redis.Redis(host='localhost', port=6379, db=0, password=redis_psw)

r.set('first', 1)
print(r.get('first'))

