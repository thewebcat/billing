import logging

import connexion

from billing.config import settings
from billing.core.database import db, init_models

__all__ = [
    'app'
]

logging.basicConfig(level=logging.INFO)

app = connexion.App(__name__, specification_dir='../share/api/')
app.add_api('swagger.yaml', arguments={'title': 'Billing System API'})

application = app.app
application.config.from_object(settings)

# Import DB models. Flask-SQLAlchemy doesn't do this automatically.
init_models()

# Initialize extensions/add-ons/plugins.
db.init_app(application)

if __name__ == '__main__':
    if settings.DEBUG:
        app.run(port=8000, debug=settings.DEBUG)
    else:
        app.run(port=8000, server='gevent')
