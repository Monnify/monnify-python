import pytest
import os
from secrets import token_hex

from monnify.tests import prefetch_token, preset_env, set_token as token
from monnify.disbursement import DisbursementSingle, DisibursementBulk, Paycode
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
    def get_reference(self):
        self.__data["reference"] = token_hex(5)
        _, result = self.__instance.initiate_transfer( self.__data)
        return result["responseBody"]["reference"]

    def test_transfer(self):

        self.__data["reference"] = token_hex(5)

        code, result = self.__instance.initiate_transfer( self.__data)
        assert code == 200

    def test_resend_otp(self,  get_reference):

        code, result = self.__instance.resend_otp( {"reference": get_reference})
        assert code == 200

    def test_authorize_transfer(self,  get_reference):

        data = {"reference": get_reference, "authorizationCode": "123456"}

        code, result = self.__instance.authorize_transfer( data)
        assert code == 200

    def test_transfer_status(self,  get_reference):
        code, result = self.__instance.get_transfer_status( get_reference)
        assert code == 200

    def test_list_transfers(self):
        code, result = self.__instance.list_all_transfers(token)
        assert code == 200

    def test_wallet_balance(self):
        code, result = self.__instance.get_wallet_balance( self.__wallet_account)
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
    def get_reference(self):
        self.__data["batchReference"] = token_hex(5)
        _, result = self.__instance.initiate_transfer( self.__data)
        return self.__data["batchReference"]

    def test_transfer(self):

        self.__data["batchReference"] = token_hex(5)

        code, result = self.__instance.initiate_transfer( self.__data)
        assert code == 200

    def test_transfer_status(self,  get_reference):
        code, result = self.__instance.get_transfer_status( get_reference)
        assert code == 200

    def test_search_transaction(self):
        code, result = self.__instance.search_transactions( self.__wallet_account)
        assert code == 200


class TestPaycodeAPIs:
    @pytest.fixture(autouse=True)
    def instantiate_class(self):
        self.__instance = Paycode(
            os.environ.get("API_KEY"), os.environ.get("SECRET_KEY")
        )

    @pytest.fixture(autouse=True)
    def initialise_data(self):
        self.__data = {
            "beneficiaryName": "Tester",
            "amount": 20,
            "paycodeReference": token_hex(5),
            "expiryDate": "2025-03-28 17:00:26",
            "clientId":"MK_TEST_JRQAZRFD2W"
        }


    @pytest.fixture()
    def get_reference(self):
        self.__data["paycodeReference"] = token_hex(5)
        _, result = self.__instance.create_paycode( self.__data)
        return result["responseBody"]["paycodeReference"]

    def test_create_paycode(self):

        code, result = self.__instance.create_paycode(self.__data)
        assert code == 200
        self.__gen_reference = result["responseBody"]["paycodeReference"]
        

    def test_get_paycode(self, get_reference):
    
        code, result = self.__instance.get_paycode(get_reference)
        assert code == 200

    def test_get_clear_paycode(self, get_reference):
            
        code, result = self.__instance.get_clear_paycode(get_reference)
        assert code == 200

    def test_delete_paycode(self, get_reference):
        
        code, result = self.__instance.delete_paycode(get_reference)
        assert code == 200