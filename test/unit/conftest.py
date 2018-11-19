# flake8: NOQA
import functools
import os

from flask import Flask

from flask_sqlalchemy import SQLAlchemy

from billing.config import settings

from test.base_conftest import * # NOQA


@pytest.fixture(scope='function')
def app():
    db = SQLAlchemy()

    def create_app():
        app = Flask(__name__)
        app.config.from_object(settings)
        db.init_app(app)
        return app

    app = create_app()
    app.app_context().push()
    return db


