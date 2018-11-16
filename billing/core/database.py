import os
from glob import glob
from importlib import import_module

from flask_sqlalchemy import SQLAlchemy

from billing.config import settings
from billing.core.log import logger


__all__ = [
    'db',
    'init_models'
]

db = SQLAlchemy()


def init_models():
    for path in glob(settings.MODELS_PATTERN, recursive=True):
        path = os.path.splitext(path)[0]
        path = path.strip('./').replace('/', '.')
        try:
            import_module(path)
        except ImportError as e:
            logger.warning('models module %s not found' % path, str(e))
