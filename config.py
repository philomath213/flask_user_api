import os


DEBUG = 'false'
SECRET_KEY = 'secret_key'

MONGODB_HOST = os.environ.get(
    'MONGODB_HOST',
    'mongodb://127.0.0.1:27017/hackini'
)
