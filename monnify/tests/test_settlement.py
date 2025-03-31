import pytest
import os
from secrets import token_hex

from monnify.tests import prefetch_token, preset_env, set_token as token
from monnify.settlement import Settlement


class TestSettlementAPIs:

    @pytest.fixture(autouse=True)
    def instantiate_class(self):
        self.__instance = Settlement(
            os.environ.get("API_KEY"), os.environ.get("SECRET_KEY")
        )

    @pytest.fixture(autouse=True)
    def initialise_data(self):
        self.__data = [
            {
                "currencyCode": "NGN",
                "bankCode": "035",
                "accountNumber": "9520825504",
                "email": "tamira1@gmail.com",
                "defaultSplitPercentage": "20",
            }
        ]

    def test_create_sub_account(self):

        code, result = self.__instance.create_sub_account(self.__data)
        assert code == 200

    def test_update_sub_account(self):
        _get_sub_account = self.__instance.get_sub_accounts()[1]["responseBody"][1]["subAccountCode"]
        self.__data[0]["email"] = "hello@test.com"
        self.__data[0]["defaultSplitPercentage"] = 73
        self.__data[0]["subAccountCode"] = _get_sub_account

        code, result = self.__instance.update_sub_account(self.__data[0])
        assert code == 200

    def test_get_sub_account(self):

        code, result = self.__instance.get_sub_accounts()
        assert code == 200

    def test_delete_sub_account(self):
        _get_sub_account = self.__instance.get_sub_accounts()[1]["responseBody"][1]["subAccountCode"]
        code, result = self.__instance.delete_sub_account(_get_sub_account)
        assert code == 200
