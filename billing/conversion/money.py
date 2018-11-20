import decimal
from collections import namedtuple
from datetime import datetime

from billing.config import settings
from billing.conversion.backend import rates_backend
from billing.core.cache import cache
from billing.core.utils import round_decimal

from .exceptions import MissingRate

__all__ = [
    'converter'
]


class Converter:
    __slots__ = ('source', 'target', 'date')

    def __init__(self):
        self.source = None
        self.target = None
        self.date = None

    def get_rate(self):
        key = f'get_rate:{self.source}:{self.target}:{self.date}'
        result = cache.get(key)
        if result is not None:
            return result
        result = self._get_rate()
        cache.set(key, result)
        return result

    def _get_rate(self):
        from billing.api.models import Rate
        if self.source == self.target:
            return 1
        rate_obj = Rate.query.get(self.date)
        if not rate_obj:
            rates_backend.update_rates(date=self.date)
            rate_obj = Rate.query.get(self.date)
        currencies = rate_obj.currency
        RateList = namedtuple('RateList', 'currency value')
        try:
            rates = [RateList(self.source, currencies[self.source]), RateList(self.target, currencies[self.target])]
        except KeyError:
            raise MissingRate('Rate %s -> %s does not exist' % (self.source, self.target))
        return self._get_rate_base(rates)

    def _get_rate_base(self, rates):
        first, second = rates
        # items if they are ordered not as expected
        if first.currency == self.target:
            first, second = second, first
        return second.value / first.value

    def convert_money(self, value, from_currency, to_currency, date=datetime.now().date()):
        self.source, self.target, self.date = from_currency, to_currency, date
        if not isinstance(value, decimal.Decimal):
            value = decimal.Decimal(value)
        amount = round_decimal(value * decimal.Decimal(self.get_rate()))
        return amount

    def get_rate_by_date(self, currency, date=datetime.now().date()):
        self.source, self.target, self.date = settings.BASE_CURRENCY, currency, date
        return self.get_rate()


converter = Converter()
