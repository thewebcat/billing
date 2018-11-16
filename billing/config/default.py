import os

DEBUG = False
LOGGING_LEVEL = 'ERROR'
MODELS_PATTERN = '**/models.py'

BASE_DIR = os.path.abspath(os.getcwd())

SQLALCHEMY_DATABASE_URI = 'sqlite://'
SQLALCHEMY_TRACK_MODIFICATIONS = True

LOGGERS = {}

BASE_CURRENCY = 'USD'
OPEN_EXCHANGE_RATES_URL = os.getenv('OPEN_EXCHANGE_RATES_URL', 'https://openexchangerates.org/api/latest.json')
OPEN_EXCHANGE_RATES_APP_ID = os.getenv('OPEN_EXCHANGE_RATES_APP_ID', '8682a71e8e0345e4ad8c83b095bfddec')
RATES_CACHE_TIMEOUT = os.getenv('RATES_CACHE_TIMEOUT', 60 * 60)

REDIS_URL = 'billing-redis'
