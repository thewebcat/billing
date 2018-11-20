from sqlalchemy import and_

from billing.api.models import Client, Transaction, Transfer, Wallet
from billing.config import settings
from billing.conversion.money import converter


class TransferHandler:

    @classmethod
    def list(cls) -> tuple:
        return [item.serialize() for item in Transfer.query.all()], 200

    @classmethod
    def get(cls, uuid) -> tuple:
        transfer = Transfer.get_or_abort(uuid)
        return transfer.serialize(), 200

    @classmethod
    def post(cls, transfer) -> tuple:
        source_wallet = Wallet.get_or_abort(transfer['source_id'])
        source_wallet.validate_balance(transfer['amount'])
        destination_wallet = Wallet.get_or_abort(transfer['destination_id'])
        transfer['amount_converted'] = converter.convert_money(transfer['amount'],
                                                               from_currency=source_wallet.currency,
                                                               to_currency=destination_wallet.currency)
        transfer = Transfer.create(**transfer)
        return transfer.serialize(), 201


class ClientsHandler:

    @classmethod
    def get(cls, uuid) -> tuple:
        response = Client.get_or_abort(uuid)
        return response.serialize(), 200

    @classmethod
    def list(cls) -> tuple:
        return [item.serialize() for item in Client.query.all()], 200

    @classmethod
    def post(cls, client) -> tuple:
        currency = client.pop('currency')
        client = Client.create(**client)
        Wallet.create(balance=0, currency=currency, client_id=client.uuid)
        return client.serialize(), 201


class DepositWithdrawal:

    @classmethod
    def post_deposit(cls, deposit) -> tuple:
        deposit['type'] = 'deposit'
        transaction_ = Transaction.create(**deposit)
        return transaction_.serialize(), 201

    @classmethod
    def post_withdrawal(cls, withdrawal) -> tuple:
        wallet_ = Wallet.get_or_abort(withdrawal['wallet_id'])
        wallet_.validate_balance(withdrawal['amount'])
        withdrawal['type'] = 'withdrawal'
        withdrawal['amount'] = -withdrawal['amount']
        transaction_ = Transaction.create(**withdrawal)
        return transaction_.serialize(), 201


def report(uuid, start_date=None, end_date=None):
    transaction_ = Transaction.query.join(Wallet).filter(Wallet.client_id == uuid)
    if start_date and end_date:
        response = transaction_.filter(
            and_(Transaction.created_at >= start_date, Transaction.created_at <= end_date)).all()
    elif start_date:
        response = transaction_.filter(
            and_(Transaction.created_at >= start_date)).all()
    elif end_date:
        response = transaction_.filter(
            and_(Transaction.created_at <= end_date)).all()
    else:
        response = transaction_.all()
    return [item.serialize() for item in response], 200


def courses(date, currency):
    result = converter.get_rate_by_date(currency, date)
    return {f'{currency}/{settings.BASE_CURRENCY}': result}, 200
