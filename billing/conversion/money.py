import decimal
from datetime import datetime


from billing.config import settings
from billing.core.cache import cache

from .exceptions import MissingRate

__all__ = [
    'convert_money'
]


def get_rate(source, target, date):
    key = f'get_rate:{source}:{target}'
    result = cache.get(key)
    if result is not None:
        return result
    result = _get_rate(source, target, date)
    cache.set(key, result)
    return result

def _get_rate(source, target, date):
    from billing.api.models import Rate
    if source == target:
        return 1
    rate = Rate.query.get(date).currency[target]
    if not rate:
        raise MissingRate('Rate %s -> %s does not exist' % (source, target))
    # if len(rates) == 1:
    #     return _try_to_get_rate_directly(source, target, rates[0])
    return rate

def convert_money(value, currency, date=datetime.now().date(), from_currency=settings.BASE_CURRENCY):
    amount = value * decimal.Decimal(get_rate(from_currency, currency, date))
    return round(amount, 2)