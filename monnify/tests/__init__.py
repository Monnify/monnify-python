import os

import pytest

from monnify.base import Base


@pytest.fixture(autouse=True, scope="package")
def preset_env():
    os.environ["API_KEY"] = "MK_TEST_MRP986PBE2"
    os.environ["SECRET_KEY"] = "JDY8NGX46ZB21W83ZF202914V14Y8TCK"
    os.environ.ENV = "SANDBOX"


@pytest.fixture(autouse=True, scope="package")
def prefetch_token(preset_env):
    base_instance = Base(os.environ.get("API_KEY"), os.environ.get("SECRET_KEY"))
    return base_instance.get_auth_token()


@pytest.fixture(scope="package", autouse=True)
def set_token(prefetch_token):
    status, response = prefetch_token
    return response["accessToken"]
