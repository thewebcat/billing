from billing.conversion.backend import rates_backend
from billing.core.celery import celery


@celery.task
def update_rates():
    rates_backend.update_rates()
