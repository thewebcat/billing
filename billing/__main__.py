import logging

import connexion

from billing.config import settings
# from billing.conversion.backend import rates_backend
# from billing.core.celery import make_celery
from billing.core.database import db, init_models
from billing.core.handlers import init_handlers
from billing.core.validators import init_validators

__all__ = [
    'app',
    'application',
]

logging.basicConfig(level=logging.INFO)


app = connexion.FlaskApp(__name__, specification_dir='../share/api/')
app.add_api('swagger.yaml', arguments={'title': 'Billing System API'}, strict_validation=True)


application = app.app
application.config.from_object(settings)

# Import DB models. Flask-SQLAlchemy doesn't do this automatically.
init_models()

# Initialize extensions/add-ons/plugins.
init_validators()
init_handlers(application)
db.init_app(application)
# celery = make_celery(application)

# @celery.task
# def send_async_email():
#     """Background task to send an email with Flask-Mail."""
#     with application.app_context():
#         rates_backend.update_rates()

if __name__ == '__main__':
    if settings.DEBUG:
        app.run(port=8000, debug=settings.DEBUG)
    else:
        app.run(port=8000, server='gevent')
