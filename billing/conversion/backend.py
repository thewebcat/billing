from datetime import datetime

import requests

from billing.config import settings
from billing.conversion.exceptions import ImproperlyConfigured

__all__ = [
    'rates_backend',
]


class BaseBackend:
    __slots__ = ('url', 'url_historical', 'access_key', 'date')

    def __init__(self):
        self.date = None

    def get_params(self):
        return {'app_id': self.access_key}

    def get_response(self, **params):
        if not self.date:
            response = requests.get(self.url, params=params)
        else:
            response = requests.get(self.url_historical.replace('*', str(self.date)), params=params)
        return response.json()

    def get_rates(self, **params):
        return self.get_response(**params)['rates']

    def update_rates(self, base_currency=settings.BASE_CURRENCY, date=datetime.now().date(), **kwargs):
        from billing.api.models import Rate
        self.date = date
        params = self.get_params()
        params.update(base_currency=base_currency, **kwargs)
        Rate.create(date=date, currency=self.get_rates(**params))


class OpenExchangeRatesBackend(BaseBackend):

    def __init__(self, url=settings.OPEN_EXCHANGE_RATES_URL,
                 url_historical=settings.OPEN_EXCHANGE_RATES_URL_HISTORICAL,
                 access_key=settings.OPEN_EXCHANGE_RATES_APP_ID):
        super().__init__()
        if access_key is None:
            raise ImproperlyConfigured(
                'settings.OPEN_EXCHANGE_RATES_APP_ID should be set'
            )
        self.url = url
        self.url_historical = url_historical
        self.access_key = access_key


rates_backend = OpenExchangeRatesBackend()
