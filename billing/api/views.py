from sqlalchemy import and_

from billing.api.models import Client, Transaction, Transfer, Wallet
from billing.config import settings
from billing.conversion.money import Converter


class BaseHandler:
    def __init__(self, attr=None):
        self.__attr = attr

    def __getattr__(self, item):
        return self.__attr


class TransferHandler(BaseHandler):

    @classmethod
    def list(cls, *args, **kwargs) -> tuple:
        return [item.serialize() for item in Transfer.query.all()], 200

    @classmethod
    def get(cls, *args, **kwargs) -> tuple:
        inst = cls(kwargs['uuid'])
        transfer = Transfer.get_or_abort(inst.uuid)
        return transfer.serialize(), 200

    @classmethod
    def post(cls, *args, **kwargs) -> tuple:
        inst = cls(kwargs['transfer'])
        source_wallet = Wallet.get_or_abort(inst.transfer['source_id'])
        source_wallet.validate_balance(inst.transfer['amount'])
        destination_wallet = Wallet.get_or_abort(inst.transfer['destination_id'])
        inst.transfer['amount_converted'] = Converter.convert_money(inst.transfer['amount'],
                                                                    from_currency=source_wallet.currency,
                                                                    to_currency=destination_wallet.currency)
        transfer = Transfer.create(**inst.transfer)
        return transfer.serialize(), 201


class ClientsHandler(BaseHandler):

    @classmethod
    def get(cls, *args, **kwargs) -> tuple:
        inst = cls(kwargs['uuid'])
        response = Client.get_or_abort(inst.uuid)
        return response.serialize(), 200

    @classmethod
    def list(cls, *args, **kwargs) -> tuple:
        return [item.serialize() for item in Client.query.all()], 200

    @classmethod
    def post(cls, *args, **kwargs) -> tuple:
        inst = cls(kwargs['client'])
        client = Client.create(**inst.client)
        Wallet.create(balance=0, currency='USD', client_id=client.uuid)
        return client.serialize(), 201


class DepositWithdrawal(BaseHandler):

    @classmethod
    def post_deposit(cls, *args, **kwargs) -> tuple:
        inst = cls(kwargs['deposit'])
        inst.deposit['type'] = 'deposit'
        transaction_ = Transaction.create(**inst.deposit)
        return transaction_.serialize(), 201

    @classmethod
    def post_withdrawal(cls, *args, **kwargs) -> tuple:
        inst = cls(kwargs['withdrawal'])
        wallet_ = Wallet.get_or_abort(inst.withdrawal['wallet_id'])
        wallet_.validate_balance(inst.withdrawal['amount'])
        inst.withdrawal['type'] = 'withdrawal'
        inst.withdrawal['amount'] = -inst.withdrawal['amount']
        transaction_ = Transaction.create(**inst.withdrawal)
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
    result = Converter.get_rate_by_date(currency, date)
    return {f'{currency}/{settings.BASE_CURRENCY}': result}, 200
