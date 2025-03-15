import pytest
import os
from secrets import token_hex

from monnify.tests import prefetch_token, preset_env, set_token as token
from monnify.disbursement.bulk_disbursement import DisibursementBulk
from monnify.disbursement import DisbursementSingle
from monnify.exceptions import UnprocessableRequestException
from marshmallow.exceptions import ValidationError


class TestSingleDisbursementAPIs:

    @pytest.fixture(autouse=True)
    def instantiate_class(self):
        self.__instance = DisbursementSingle(
            os.environ.get("API_KEY"), os.environ.get("SECRET_KEY")
        )

    @pytest.fixture(autouse=True)
    def initialise_data(self):
        self.__data = {
            "amount": 200,
            "narration": "Test01",
            "destinationBankCode": "057",
            "destinationAccountNumber": "2085886393",
            "currency": "NGN",
            "sourceAccountNumber": "3934178936",
            "destinationAccountName": "Marvelous Benji",
        }
        self.__wallet_account = "3934178936"

    @pytest.fixture()
    def get_reference(self, token):
        self.__data["reference"] = token_hex(5)
        _, result = self.__instance.initiate_transfer(token, self.__data)
        return result["responseBody"]["reference"]

    def test_transfer(self, token):

        self.__data["reference"] = token_hex(5)

        code, result = self.__instance.initiate_transfer(token, self.__data)
        assert code == 200

    def test_resend_otp(self, token, get_reference):

        code, result = self.__instance.resend_otp(token, {"reference": get_reference})
        assert code == 200

    def test_authorize_transfer(self, token, get_reference):

        data = {"reference": get_reference, "authorizationCode": "123456"}

        code, result = self.__instance.authorize_transfer(token, data)
        assert code == 200

    def test_transfer_status(self, token, get_reference):
        code, result = self.__instance.get_transfer_status(token, get_reference)
        assert code == 200

    def test_list_transfers(self, token):
        code, result = self.__instance.list_all_transfers(token)
        assert code == 200

    def test_wallet_balance(self, token):
        code, result = self.__instance.get_wallet_balance(token, self.__wallet_account)
        assert code == 200


class TestBulkDisbursementAPIs:

    @pytest.fixture(autouse=True)
    def instantiate_class(self):
        self.__instance = DisibursementBulk(
            os.environ.get("API_KEY"), os.environ.get("SECRET_KEY")
        )

    @pytest.fixture(autouse=True)
    def initialise_data(self):
        self.__data = {
            "title": "Test01",
            "narration": "911 Transaction",
            "currency": "NGN",
            "sourceAccountNumber": "3934178936",
            "destinationAccountName": "Marvelous Benji",
            "notificationInterval": 25,
            "onValidationFailure": "CONTINUE",
            "transactionList": [
                {
                    "amount": 1300,
                    "reference": f"{token_hex(4)}",
                    "narration": "911 Transaction",
                    "destinationBankCode": "057",
                    "destinationAccountNumber": "2085886393",
                    "destinationAccountName": "Marvelous Benji",
                    "currency": "NGN",
                }
            ],
        }
        self.__wallet_account = "3934178936"

    @pytest.fixture()
    def get_reference(self, token):
        self.__data["batchReference"] = token_hex(5)
        _, result = self.__instance.initiate_transfer(token, self.__data)
        return self.__data["batchReference"]

    def test_transfer(self, token):

        self.__data["batchReference"] = token_hex(5)

        code, result = self.__instance.initiate_transfer(token, self.__data)
        assert code == 200

    def test_transfer_status(self, token, get_reference):
        code, result = self.__instance.get_transfer_status(token, get_reference)
        assert code == 200

    def test_search_transaction(self, token):
        code, result = self.__instance.search_transactions(token, self.__wallet_account)
        assert code == 200
