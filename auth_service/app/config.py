import os 

DB_USERNAME = os.environ.get('MONGO_USERNAME')
DB_PASSWORD = os.environ.get('MONGO_PASSWORD')
DB_HOST = 'mongodb'
DB_PORT = '27017'
DB_URI = f'mongodb://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/'

DB_NAME = 'ZEST_DB'
USERS_COLLECTION = 'users'
JWT_ALGORITHM = 'HS256'
JWT_TTL = 3600 * 12  # 12 hours in seconds - half a day