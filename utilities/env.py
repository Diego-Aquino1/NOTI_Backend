import os
from dotenv import load_dotenv

load_dotenv('.env')
print('Loading environment variables...')

# database configuration
#DB_USER = os.getenv('DB_USER', '')
#DB_PASSWORD = os.getenv('DB_PASSWORD', '')
#DB_NAME = os.getenv('DB_NAME', '')
#DB_HOST = os.getenv('DB_HOST', 'localhost')

DB_USER = "postgres"
DB_PASSWORD = "root"
DB_NAME = "noti00"
DB_HOST = "localhost"

# jwt configuration
# JWT_SECRET = os.getenv('JWT_SECRET', '')
# JWT_EXPIRES_IN = int(os.getenv('JWT_EXPIRES_IN', 1))