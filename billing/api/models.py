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


class ModelMixin(object):
    def serialize(self):
        return Serializer.serialize(self)


class Wallet(ModelMixin, db.Model):
    __tablename__ = 'wallet'

    uuid = db.Column(UUID(as_uuid=True), unique=True, nullable=False, primary_key=True)
    balance = db.Column(db.Numeric(12, 2), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True))

    def __repr__(self):
        return '<Wallet %r>' % self.uuid


class Transfer(ModelMixin, db.Model):
    __tablename__ = 'transfer'

    uuid = db.Column(UUID(as_uuid=True), unique=True, nullable=False, primary_key=True)
    balance = db.Column(db.Numeric(12, 2), nullable=False)
    source_id = db.ForeignKey("Wallet", back_populates="source_transfers")
    destination_id = db.ForeignKey("Wallet", back_populates="destination_transfers")
    created_at = db.Column(db.DateTime(timezone=True))

    def __repr__(self):
        return '<Transfer %r>' % self.uuid


class Transaction(ModelMixin, db.Model):
    __tablename__ = 'transaction'

    uuid = db.Column(UUID(as_uuid=True), unique=True, nullable=False, primary_key=True)
    amount = db.Column(db.Numeric(12, 2), nullable=False)
    source_id = db.ForeignKey("Wallet", back_populates="transactions")
    created_at = db.Column(db.DateTime(timezone=True))

    def __repr__(self):
        return '<Transaction %r>' % self.uuid