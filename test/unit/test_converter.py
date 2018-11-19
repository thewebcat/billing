# flake8: NOQA
from datetime import datetime, timedelta

import pytest

from billing.conversion.exceptions import MissingRate
from billing.conversion.money import Converter

date = datetime.now().date() - timedelta(days=1)

@pytest.mark.parametrize('currency', ('EUR', 'USD', 'CNY'))
def test_money(app, currency):
    result = Converter.get_rate_by_date(currency, date)
    assert result


def test_money_wrong_rate(app):
    with pytest.raises(MissingRate):
        Converter.get_rate_by_date('EURf', date)


@pytest.mark.parametrize('currencies', (['EUR', 'USD',], ['CNY', 'CAD']))
def test_money_conversion(app, currencies):
    amount = 30
    amount_converted = Converter.convert_money(amount, from_currency=currencies[0],
                                               to_currency=currencies[1])
    assert amount_converted