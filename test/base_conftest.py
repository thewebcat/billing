# flake8: NOQA
import pytest

from billing.core.cache import cache


@pytest.fixture(scope='session', autouse=True)
def redis_clean(request):
    cache.clear()

    def resource_teardown():
        cache.clear()

    request.addfinalizer(resource_teardown)
