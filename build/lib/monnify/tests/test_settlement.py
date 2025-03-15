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
                "bankCode": "057",
                "accountNumber": "2085886393",
                "email": "tamira1@gmail.com",
                "defaultSplitPercentage": "20",
            }
        ]

    @pytest.fixture()
    def get_sub_account(self, token):

        code, result = self.__instance.get_sub_accounts(token)
        assert code == 200
        return result["responseBody"][-1]["subAccountCode"]

    def test_create_sub_account(self, token):

        code, result = self.__instance.create_sub_account(token, self.__data)
        assert code == 200

    def test_update_sub_account(self, token, get_sub_account):

        self.__data[0]["email"] = "hello@test.com"
        self.__data[0]["defaultSplitPercentage"] = 73
        self.__data[0]["subAccountCode"] = get_sub_account

        code, result = self.__instance.update_sub_account(token, self.__data[0])
        assert code == 200

    def test_get_sub_account(self, token):

        code, result = self.__instance.get_sub_accounts(token)
        assert code == 200

    def test_delete_sub_account(self, token, get_sub_account):

        code, result = self.__instance.delete_sub_accounts(token, get_sub_account)
        assert code == 200
