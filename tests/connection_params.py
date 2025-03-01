from dotenv import load_dotenv
from os import getenv

load_dotenv('../src/redis.env')  # Load environment variables from redis.env file
REDIS_PWS: str = getenv('REDIS_PSW')
REDIS_HOST: str = getenv('REDIS_HOST') or 'localhost'
REDIS_PORT: int = int(getenv('REDIS_PORT') or 6379)
REDIS_USERNAME: str = getenv('REDIS_USERNAME') or 'default'
