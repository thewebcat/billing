# flake8: noqa
import os

from celery.schedules import crontab


DEBUG = False
LOGGING_LEVEL = 'ERROR'
MODELS_PATTERN = '**/models.py'

BASE_DIR = os.path.abspath(os.getcwd())

SQLALCHEMY_DATABASE_URI = 'sqlite://'
SQLALCHEMY_TRACK_MODIFICATIONS = True

CELERY_BROKER_URL='redis://billing-redis:6379/0',
CELERY_RESULT_BACKEND='redis://billing-redis:6379/0'
CELERYBEAT_SCHEDULE = {
    'one-day-update-rates': {
        'task': 'billing.conversion.tasks.update_rates',
        # Every night at 00:01
        'schedule': crontab(minute='1', hour='0'),
    }
}

LOGGERS = {}

BASE_CURRENCY = 'USD'
OPEN_EXCHANGE_RATES_URL = os.getenv('OPEN_EXCHANGE_RATES_URL', 'https://openexchangerates.org/api/latest.json')
OPEN_EXCHANGE_RATES_URL_HISTORICAL = os.getenv('OPEN_EXCHANGE_RATES_URL', 'https://openexchangerates.org/api/historical/*.json')
OPEN_EXCHANGE_RATES_APP_ID = os.getenv('OPEN_EXCHANGE_RATES_APP_ID', '8682a71e8e0345e4ad8c83b095bfddec')
RATES_CACHE_TIMEOUT = os.getenv('RATES_CACHE_TIMEOUT', 60 * 60)

REDIS_URL = 'billing-redis'
