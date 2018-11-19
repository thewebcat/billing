# flake8: NOQA
import functools
import os

from pyswagger import App
from pyswagger.contrib.client.requests import Client

from test.base_conftest import * #NOQA


@pytest.fixture(autouse=True)
def client():
    c = Client()

    def init_request(self):
        self.request = functools.partial(self.request, opt={
            'url_netloc': 'test:8000'
        })
    c.init_request = functools.partial(init_request, c)

    c.init_request()

    return c


@pytest.fixture(autouse=True)
def app():
    spec_path = os.path.join(os.path.dirname(__file__), '..', '..', 'share', 'api', 'swagger.yaml')
    return App.create(spec_path)
