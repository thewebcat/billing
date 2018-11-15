from billing.api.models import Transaction
from billing.core.log import logger


def transaction() -> tuple:
    transactions = Transaction.query.all()
    return [item.serialize() for item in transactions], 200