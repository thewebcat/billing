import pytest

from billing.core.cache import cache


@pytest.fixture(scope='module', autouse=True)
def redis_clean():
    cache.clear()