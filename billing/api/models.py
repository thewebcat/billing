import decimal

from sqlalchemy import Enum, text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.exc import DataError
from sqlalchemy.inspection import inspect
from sqlalchemy.orm.collections import InstrumentedList
from sqlalchemy.orm.mapper import Mapper
from sqlalchemy.sql.elements import BinaryExpression

from werkzeug.exceptions import abort

from billing.core.database import db


class Serializer:

    def serialize(self):
        result = {}
        for c in inspect(self.__class__).all_orm_descriptors.keys():
            if not isinstance(getattr(self, c), (Mapper, BinaryExpression)):
                if not isinstance(getattr(self, c), InstrumentedList):
                    if not isinstance(getattr(self, c), db.Model):
                        result[c] = getattr(self, c)
                else:
                    result[c] = [m.serialize() for m in getattr(self, c)]
        return result


class ModelMixin:
    def serialize(self):
        return Serializer.serialize(self)

    @classmethod
    def create(cls, **data):
        obj = cls(**data)
        db.session.add(obj)
        db.session.commit()
        return obj

    @classmethod
    def get_or_abort(cls, object_id, code=404):
        try:
            result = cls.query.get(object_id)
        except DataError as err:
            abort(400, err.__str__())
        if result is None:
            abort(code, f'The requested {cls.__mro__[0].__name__} was not found on the server')
        return result

    def __repr__(self):
        res = f'{self.__class__.__name__}'
        if hasattr(self, 'uuid'):
            res = f'{res} {self.uuid}'
        return res


class BaseMixin:
    uuid = db.Column(UUID(as_uuid=True), unique=True, nullable=False, primary_key=True,
                     server_default=text('uuid_generate_v4()'))
    created_at = db.Column(db.DateTime(timezone=True), server_default=text('Now()'))


class Client(ModelMixin, BaseMixin, db.Model):
    __tablename__ = 'client'

    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=True)
    country = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(255), nullable=False)

    wallet = db.relationship('Wallet', backref='client', lazy=True)


class Wallet(ModelMixin, BaseMixin, db.Model):
    __tablename__ = 'wallet'

    balance = db.Column(db.Numeric(12, 2), default=0, nullable=False)
    currency = db.Column(Enum('USD', 'EUR', 'CAD', 'CNY', name='currency_list', create_type=False))
    client_id = db.Column(UUID(as_uuid=True), db.ForeignKey('client.uuid'))

    transfers = db.relationship('Transfer', backref='wallet', primaryjoin='or_(Wallet.uuid==Transfer.source_id, '
                                                                          'Wallet.uuid==Transfer.destination_id)')
    transactions = db.relationship('Transaction', backref='wallet', lazy=True)

    def validate_balance(self, value):
        if self.balance - decimal.Decimal(value) < 0:
            return abort(400, f'You do not have enough amount on your balance to make this operation')


class Transfer(ModelMixin, BaseMixin, db.Model):
    __tablename__ = 'transfer'

    amount = db.Column(db.Numeric(12, 2), default=0, nullable=False)
    amount_converted = db.Column(db.Numeric(12, 2), default=0, nullable=False)
    source_id = db.Column(UUID(as_uuid=True), db.ForeignKey('wallet.uuid'))
    destination_id = db.Column(UUID(as_uuid=True), db.ForeignKey('wallet.uuid'))


class Transaction(ModelMixin, BaseMixin, db.Model):
    __tablename__ = 'transaction'

    amount = db.Column(db.Numeric(12, 2), default=0, nullable=False)
    type = db.Column(Enum('deposit', 'withdrawal', 'transfer', name='transaction_types_list', create_type=False))
    wallet_id = db.Column(UUID(as_uuid=True), db.ForeignKey('wallet.uuid'))


class Rate(ModelMixin, db.Model):
    __tablename__ = 'rate'

    date = db.Column(db.Date(), unique=True, nullable=False, primary_key=True,
                     server_default=text('Now()'))
    currency = db.Column(JSONB())
