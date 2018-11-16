from datetime import datetime

from sqlalchemy import text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.ext.hybrid import hybrid_method, hybrid_property
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import column_property
from sqlalchemy.orm.mapper import Mapper
from sqlalchemy.orm.collections import InstrumentedList
from sqlalchemy.sql.elements import BinaryExpression

from billing.config import settings
from billing.conversion.money import convert_money
from billing.core.database import db


class Serializer:

    def serialize(self):
        result = {}
        for c in inspect(self.__class__).all_orm_descriptors.keys():#inspect(self).attrs.keys():
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

    balance = db.Column(db.Numeric(12, 2), nullable=False)
    currency = db.Column(db.String(3), nullable=False)
    client_id = db.Column(UUID(as_uuid=True), db.ForeignKey('client.uuid'))

    def __init__(self, balance, currency):
        self.balance = balance
        self.currency = currency

    @hybrid_property
    def balance_converted(self):
        if self.currency == settings.BASE_CURRENCY:
            return self.balance
        else:
            return convert_money(self.balance, self.currency)


class Transfer(ModelMixin, BaseMixin, db.Model):
    __tablename__ = 'transfer'

    amount = db.Column(db.Numeric(12, 2), nullable=False)
    source_id = db.Column(UUID(as_uuid=True), db.ForeignKey('wallet.uuid'))
    destination_id = db.Column(UUID(as_uuid=True), db.ForeignKey('wallet.uuid'))


class Transaction(ModelMixin, BaseMixin, db.Model):
    __tablename__ = 'transaction'

    amount = db.Column(db.Numeric(12, 2), nullable=False)
    wallet_id = db.Column(UUID(as_uuid=True), db.ForeignKey('wallet.uuid'))


class Rate(ModelMixin, db.Model):
    date = db.Column(db.Date(), unique=True, nullable=False, primary_key=True,
                     server_default=text('Now()'))
    currency = db.Column(JSONB())

    @classmethod
    def get_for_date(cls, date=None): pass
