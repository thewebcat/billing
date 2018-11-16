from billing.api.models import Transaction, Wallet, Transfer, Client
from billing.core.database import db


def transaction() -> tuple:
    transactions = Transaction.query.all()
    return [item.serialize() for item in transactions], 200


def wallet() -> tuple:
    wallets = Wallet.query.all()
    return [item.serialize() for item in wallets], 200


class BaseHandler:
    def __init__(self, attr=None):
        self.__attr = attr

    def __getattr__(self, item):
        return self.__attr


class TransferHandler(BaseHandler):
    @classmethod
    def list(cls, *args, **kwargs):
        response = [item.serialize() for item in Transfer.query.all()]
        return response, 200


class ClientsHandler(BaseHandler):

    @classmethod
    def get(cls, *args, **kwargs):
        inst = cls(kwargs['uuid'])
        response = Client.query.filter_by(uuid=inst.uuid).first()
        return response.serialize(), 200

    @classmethod
    def list(cls, *args, **kwargs):
        response = [item.serialize() for item in Client.query.all()]
        return response, 200

    @classmethod
    def post(cls, *args, **kwargs):
        inst = cls(kwargs['client'])
        client = Client.create(**inst.client)
        Wallet.create(balance=0, currency='USD', client_id=client.uuid)
        response = client.serialize()
        return response, 201