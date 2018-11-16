from datetime import datetime

import requests

from billing.api.models import Rate
from billing.config import settings
from billing.conversion.exceptions import ImproperlyConfigured

__all__ = [
    'update_rates',
]


class BaseBackend:

    __slots__ = ('url', 'access_key')

    def get_params(self):
        return {'app_id': self.access_key}

    def get_response(self, **params):
        response = requests.get(self.url, params=params)
        return response.json()

    def get_rates(self, **params):
        return self.get_response(**params)['rates']

    def update_rates(self, base_currency=settings.BASE_CURRENCY, **kwargs):
        params = self.get_params()
        params.update(base_currency=base_currency, **kwargs)
        if not Rate.query.get(datetime.now().date()):
            Rate.create(date=datetime.now().date(), currency=self.get_rates(**params))

class OpenExchangeRatesBackend(BaseBackend):

    def __init__(self, url=settings.OPEN_EXCHANGE_RATES_URL, access_key=settings.OPEN_EXCHANGE_RATES_APP_ID):
        if access_key is None:
            raise ImproperlyConfigured(
                'settings.OPEN_EXCHANGE_RATES_APP_ID should be set'
            )
        self.url = url
        self.access_key = access_key

update_rates = OpenExchangeRatesBackend()