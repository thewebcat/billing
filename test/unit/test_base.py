# flake8: NOQA
import pytest

from billing.api.models import Client, Transaction, Transfer, Wallet
from billing.conversion.money import converter


@pytest.fixture()
def test_register(app):
    data_list = (
        {
            'city': 'Moscow',
            'country': 'Russia',
            'first_name': 'Marta',
            'last_name': 'Stone',
            'currency': 'USD',
        }, {
            'city': 'USA',
            'country': 'Boston',
            'first_name': 'John',
            'last_name': 'Miller',
            'currency': 'EUR',
        }
    )
    resp = []
    for data in data_list:
        print(data)
        currency = data.pop('currency')
        client = Client.create(**data)
        print(client.uuid)
        wallet = Wallet.create(balance=0, currency=currency, client_id=client.uuid)
        assert isinstance(client.serialize(), dict)
        assert wallet.currency == currency
        resp.append({'client_id': client.uuid, 'wallet_id': wallet.uuid})
    return resp


@pytest.fixture()
def test_deposit(app, test_register):
    data = {
        'amount': 150,
        'wallet_id': test_register[0]['wallet_id']
    }
    wallet = Wallet.query.get(test_register[0]['wallet_id'])
    assert wallet.balance == 0
    data['type'] = 'deposit'
    transaction = Transaction.create(**data)
    assert transaction.amount == 150
    assert wallet.balance == 150


@pytest.fixture()
def test_withdrawal(app, test_register, test_deposit):
    data = {
        'amount': 100,
        'wallet_id': test_register[0]['wallet_id']
    }
    wallet = Wallet.query.get(test_register[0]['wallet_id'])
    print(wallet.uuid)
    wallet.validate_balance(data['amount'])
    assert wallet.balance == 150
    data['amount'] = -data['amount']
    data['type'] = 'withdrawal'
    transaction = Transaction.create(**data)
    assert transaction.amount == -100
    assert wallet.balance == 50


def test_transfer(app, test_register, test_deposit, test_withdrawal):
    data = {
        'amount': 35,
        'source_id': test_register[0]['wallet_id'],
        'destination_id': test_register[1]['wallet_id']
    }
    source_wallet = Wallet.query.get(data['source_id'])
    assert source_wallet.balance == 50
    destination_wallet = Wallet.query.get(data['destination_id'])
    assert destination_wallet.balance == 0
    source_wallet.validate_balance(data['amount'])
    amount_converted = converter.convert_money(data['amount'], from_currency=source_wallet.currency,
                                               to_currency=destination_wallet.currency)
    data['amount_converted'] = amount_converted
    Transfer.create(**data)
    source_wallet = Wallet.query.get(data['source_id'])
    assert source_wallet.balance == 15
    destination_wallet = Wallet.query.get(data['destination_id'])
    assert destination_wallet.balance == amount_converted
