from sqlalchemy.exc import DataError

from werkzeug.exceptions import abort

from billing.api.models import Client, Transaction, Transfer, Wallet
from billing.conversion.money import Converter
from billing.core.log import logger


class BaseHandler:
    def __init__(self, attr=None):
        self.__attr = attr

    def __getattr__(self, item):
        return self.__attr


def transaction() -> tuple:
    transactions = Transaction.query.all()
    return [item.serialize() for item in transactions], 200


def wallet() -> tuple:
    wallets = Wallet.query.all()
    return [item.serialize() for item in wallets], 200


class TransferHandler(BaseHandler):

    @classmethod
    def list(cls, *args, **kwargs) -> tuple:
        return [item.serialize() for item in Transfer.query.all()], 200

    @classmethod
    def get(cls, *args, **kwargs) -> tuple:
        inst = cls(kwargs['uuid'])
        try:
            transfer = Transfer.query.filter_by(uuid=inst.uuid).first()
        except DataError as err:
            logger.error(err, exc_info=True)
            raise abort(404)
        return transfer.serialize(), 200

    @classmethod
    def post(cls, *args, **kwargs) -> tuple:
        inst = cls(kwargs['transfer'])
        source_wallet = Wallet.query.get(inst.transfer['source_id'])
        destination_wallet = Wallet.query.get(inst.transfer['destination_id'])
        inst.transfer['amount_converted'] = Converter.convert_money(inst.transfer['amount'],
                                                                    from_currency=source_wallet.currency,
                                                                    to_currency=destination_wallet.currency)
        transfer = Transfer.create(**inst.transfer)
        return transfer.serialize(), 201


class ClientsHandler(BaseHandler):

    @classmethod
    def get(cls, *args, **kwargs) -> tuple:
        inst = cls(kwargs['uuid'])
        try:
            response = Client.query.filter_by(uuid=inst.uuid).first()
        except DataError as err:
            logger.error(err, exc_info=True)
            raise abort(404)
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
        transaction_ = Transaction.create(**inst.deposit)
        return transaction_.serialize(), 201

    @classmethod
    def post_withdrawal(cls, *args, **kwargs) -> tuple:
        inst = cls(kwargs['withdrawal'])
        inst.withdrawal['amount'] = -inst.withdrawal['amount']
        transaction_ = Transaction.create(**inst.withdrawal)
        return transaction_.serialize(), 201
