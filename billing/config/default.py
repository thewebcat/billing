import os

DEBUG = False
LOGGING_LEVEL = 'ERROR'
MODELS_PATTERN = '**/models.py'

BASE_DIR = os.path.abspath(os.getcwd())

SQLALCHEMY_DATABASE_URI = 'sqlite://'
SQLALCHEMY_TRACK_MODIFICATIONS = True

LOGGERS = {}