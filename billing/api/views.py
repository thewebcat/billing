from sqlalchemy.exc import DataError

from werkzeug.exceptions import abort

from billing.api.models import Client, Transaction, Transfer, Wallet
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
        response = [item.serialize() for item in Transfer.query.all()]
        return response, 200

    @classmethod
    def get(cls, *args, **kwargs) -> tuple:
        inst = cls(kwargs['uuid'])
        try:
            transfer = Transfer.query.filter_by(uuid=inst.uuid).first()
        except DataError as err:
            logger.error(err, exc_info=True)
            raise abort(404)
        response = transfer.serialize()
        return response, 200

    @classmethod
    def post(cls, *args, **kwargs) -> tuple:
        inst = cls(kwargs['transfer'])
        transfer = Transfer.create(**inst.transfer)
        response = transfer.serialize()
        return response, 201


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
        response = [item.serialize() for item in Client.query.all()]
        return response, 200

    @classmethod
    def post(cls, *args, **kwargs) -> tuple:
        inst = cls(kwargs['client'])
        client = Client.create(**inst.client)
        Wallet.create(balance=0, currency='USD', client_id=client.uuid)
        response = client.serialize()
        return response, 201
