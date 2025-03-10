import os

import pytest

from monnify.base import Base




@pytest.fixture(autouse=True, scope='package')
def preset_env():
    os.environ['API_KEY'] = 'MK_TEST_JRQAZRFD2W'
    os.environ['SECRET_KEY'] = 'T2CTRSB758NT2RATE17CV0Y9BSH4KCCB'
    os.environ.ENV = 'SANDBOX'


@pytest.fixture(autouse=True, scope='package')
def prefetch_token(preset_env):
    base_instance = Base(os.environ.get('API_KEY'),os.environ.get('SECRET_KEY'))
    return base_instance.get_auth_token()


@pytest.fixture(scope='package',autouse=True)
def set_token(prefetch_token):
     status, response = prefetch_token
     return response['responseBody']['accessToken']