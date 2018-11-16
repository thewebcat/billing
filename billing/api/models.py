from sqlalchemy import text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.inspection import inspect
from sqlalchemy.orm.collections import InstrumentedList

from billing.core.database import db


class Serializer:

    def serialize(self):
        result = {}

        for c in inspect(self).attrs.keys():
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


class Client(ModelMixin, db.Model):
    __tablename__ = 'client'

    uuid = db.Column(UUID(as_uuid=True), unique=True, nullable=False, primary_key=True,
                     server_default=text("uuid_generate_v4()"))
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=True)
    country = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=text("Now()"))

    wallet = db.relationship("Wallet", backref='client', lazy=True)


class Wallet(ModelMixin, db.Model):
    __tablename__ = 'wallet'

    uuid = db.Column(UUID(as_uuid=True), unique=True, nullable=False, primary_key=True,
                     server_default=text("uuid_generate_v4()"))
    balance = db.Column(db.Numeric(12, 2), nullable=False)
    currency = db.Column(db.String(3), nullable=False)
    client_id = db.Column(UUID(as_uuid=True), db.ForeignKey("client.uuid"))
    created_at = db.Column(db.DateTime(timezone=True), server_default=text("Now()"))


class Transfer(ModelMixin, db.Model):
    __tablename__ = 'transfer'

    uuid = db.Column(UUID(as_uuid=True), unique=True, nullable=False, primary_key=True)
    amount = db.Column(db.Numeric(12, 2), nullable=False)
    source_id = db.Column(UUID(as_uuid=True), db.ForeignKey("wallet.uuid"))
    destination_id = db.Column(UUID(as_uuid=True), db.ForeignKey("wallet.uuid"))
    created_at = db.Column(db.DateTime(timezone=True))


class Transaction(ModelMixin, db.Model):
    __tablename__ = 'transaction'

    uuid = db.Column(UUID(as_uuid=True), unique=True, nullable=False, primary_key=True)
    amount = db.Column(db.Numeric(12, 2), nullable=False)
    source_id = db.Column(UUID(as_uuid=True), db.ForeignKey("wallet.uuid"))
    created_at = db.Column(db.DateTime(timezone=True))