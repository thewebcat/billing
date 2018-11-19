# flake8: NOQA
import json
from datetime import datetime

import pytest


pytest.client_ids = []
pytest.wallet_ids = []


@pytest.mark.parametrize('param', [
    dict(
        city="Germany",
        country="Berlin",
        currency="USD",
        first_name="Ul",
        last_name="Lin"
    ),
    dict(
        city="Moscow",
        country="Russia",
        currency="CNY",
        first_name="Ul",
        last_name="Lin"
    )])
def test_api_register(client, app, param):
    response = client.request(app.op['billing.api.views.ClientsHandler.post'](
        client=param
    ))
    content = str(response.raw).replace('\\n', '')
    pytest.client_ids.append(response.data['uuid'])
    assert response.status == 201, content


def test_api_clients(client, app):
    response = client.request(app.op['billing.api.views.ClientsHandler.list']())
    content = str(response.raw).replace('\\n', '')
    assert response.status == 200, content


@pytest.mark.parametrize('count', (0, 1))
def test_api_get_client(client, app, count):
    response = client.request(app.op['billing.api.views.ClientsHandler.get'](
        uuid=pytest.client_ids[count]
    ))
    content = str(response.raw).replace('\\n', '')
    pytest.wallet_ids.append(json.loads(response.raw)['wallet'][0]['uuid'])
    assert response.status == 200, content


def test_api_deposit(client, app):
    response = client.request(app.op['billing.api.views.DepositWithdrawal.post_deposit'](
        deposit=dict(
            amount=180,
            wallet_id=pytest.wallet_ids[0]
        )
    ))
    content = str(response.raw).replace('\\n', '')
    assert response.status == 201, content


def test_api_withdrawal(client, app):
    response = client.request(app.op['billing.api.views.DepositWithdrawal.post_withdrawal'](
        withdrawal=dict(
            amount=80,
            wallet_id=pytest.wallet_ids[0]
        )
    ))
    content = str(response.raw).replace('\\n', '')
    assert response.status == 201, content


def test_api_transfer(client, app):
    response = client.request(app.op['billing.api.views.TransferHandler.post'](
        transfer=dict(
            amount=1,
            source_id=pytest.wallet_ids[0],
            destination_id=pytest.wallet_ids[1]
        )
    ))
    content = str(response.raw).replace('\\n', '')
    assert response.status == 201, content


def test_api_bad_transfer(client, app):
    response = client.request(app.op['billing.api.views.TransferHandler.post'](
        transfer=dict(
            amount=100,
            source_id=pytest.wallet_ids[0],
            destination_id=pytest.wallet_ids[1]
        )
    ))
    content = str(response.raw).replace('\\n', '')
    assert response.status == 400, content


def test_api_report(client, app):
    response = client.request(app.op['billing.api.views.report'](
        uuid=pytest.client_ids[0]
    ))
    content = str(response.raw).replace('\\n', '')
    assert response.status == 200, content


def test_api_cources(client, app):
    response = client.request(app.op['billing.api.views.courses'](
        date=datetime.now().date(),
        currency='EUR',
    ))
    content = str(response.raw).replace('\\n', '')
    assert response.status == 200, content
