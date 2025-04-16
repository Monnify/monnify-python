import pytest
import os
from secrets import token_hex

from . import prefetch_token, preset_env, set_token as token
from monnify.collection import Transaction
from monnify.collection.reserved_account import ReservedAccount
from monnify.collection.invoice import Invoice
from monnify.exceptions import UnprocessableRequestException
from marshmallow.exceptions import ValidationError


def test_authentication(prefetch_token):
    status, response = prefetch_token
    assert status == 200


class TestTransactionAPIs:

    @pytest.fixture(autouse=True)
    def instantiate_class(self):
        self.__instance = Transaction(
            os.environ.get("API_KEY"), os.environ.get("SECRET_KEY")
        )
        assert isinstance(self.__instance, Transaction)

    @pytest.fixture(autouse=True)
    def initialise_data(self):
        self.__data = {
            "amount": 100000,
            "customerEmail": "test@gmail.com",
            "paymentDescription": "FIN",
            "currencyCode": "NGN",
            "contractCode": "7059707855",
            "redirectUrl": "https://plateauexpress.net/payment/callback",
            "paymentMethods": [],
            "metaData": {"phoneNumber": "08088632541", "name": "Khalid"},
            "incomeSplitConfig": [
                {
                    "subAccountCode": "MFY_SUB_456786606061",
                    "feePercentage": 10.5,
                    "splitAmount": 25000,
                    "feeBearer": True,
                }
            ],
        }
        self.__trx_ref = "MNFY|50|20250205174323|000010"
        self.__payment_ref = "f70d6c203e6d966c9407a19de895aeb5b9fabb96"
        self.__card_data = {
            "card": {
                "number": "4111111111111111",
                "expiryMonth": "10",
                "expiryYear": "2022",
                "pin": "1234",
                "cvv": "122",
            },
            "deviceInformation": {
                "httpBrowserLanguage": "en-US",
                "httpBrowserJavaEnabled": False,
                "httpBrowserJavaScriptEnabled": True,
                "httpBrowserColorDepth": 24,
                "httpBrowserScreenHeight": 1203,
                "httpBrowserScreenWidth": 2138,
                "httpBrowserTimeDifference": "",
                "userAgentBrowserValue": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)     Chrome/105.0.0.0 Safari/537.36",
            },
        }
        self._trx_reference = ""

    @pytest.fixture()
    def get_reference(self):
        self.__data["paymentReference"] = token_hex(5)
        _, result = self.__instance.initialize_transaction(self.__data)
        return result["responseBody"]["transactionReference"]

    def test_transaction_initialization(self):
        with pytest.raises(ValidationError):
            self.__instance.initialize_transaction(self.__data)

        self.__data["paymentReference"] = token_hex(5)
        code, result = self.__instance.initialize_transaction(self.__data)
        assert code == 200

    def test_transaction_status_v2(self):
        code, result = self.__instance.get_transaction_status_v2(
            transaction_reference=self.__trx_ref
        )
        assert code == 200 and result["responseBody"]["paymentStatus"] == "PAID"

    def test_transaction_status(self):
        code, result = self.__instance.get_transaction_status(
            transaction_reference=self.__trx_ref
        )
        assert code == 200 and result["responseBody"]["paymentStatus"] == "PAID"

        code, result = self.__instance.get_transaction_status(
             payment_reference=self.__payment_ref
        )
        assert code == 200 and result["responseBody"]["paymentStatus"] == "PAID"

        with pytest.raises((UnprocessableRequestException, Exception)):
            self.__instance.get_transaction_status_v1(
                 payment_reference=self.__trx_ref
            )

    def test_ussd_transaction(self,  get_reference):

        data = {"transactionReference": get_reference, "bankUssdCode": "737"}
        with pytest.raises(ValidationError):
            data.pop("transactionReference")
            _, result = self.__instance.pay_with_ussd( data)

        if os.environ.get("ENV") is not None and os.environ.get("ENV") == "SANDBOX":
            pytest.skip("Skipping test as API not available in SANDBOX environment")

    def test_bank_transfer(self,  get_reference):

        data = {"transactionReference": get_reference}
        code, result = self.__instance.pay_with_bank_transfer( data)
        assert code == 200 and result["responseBody"].get("accountNumber") is not None

        with pytest.raises(ValidationError):
            data.pop("transactionReference")
            _, result = self.__instance.pay_with_bank_transfer( data)

    def test_card(self,  get_reference):

        self.__card_data["transactionReference"] = get_reference
        self.__card_data["collectionChannel"] = "API_NOTIFICATION"
        code, result = self.__instance.charge_card( self.__card_data)
        assert code == 200


class TestReservedAccountAPIs:

    @pytest.fixture(autouse=True)
    def init_class(self):
        self.__instance = ReservedAccount(
            os.environ.get("API_KEY"), os.environ.get("SECRET_KEY")
        )

    @pytest.fixture(autouse=True)
    def init_data(self):
        self.__data = {
            "accountName": "Test Reserved Account",
            "currencyCode": "NGN",
            "contractCode": "7059707855",
            "customerName": "John Doe",
            "bvn": "21212121212",
            "getAllAvailableBanks": True,
            "incomeSplitConfig": [
                {
                    "subAccountCode": "MFY_SUB_456786606061",
                    "feePercentage": 10.5,
                    "splitAmount": 25000,
                    "feeBearer": True,
                }
            ],
        }

    @pytest.fixture()
    def get_account_reference(self, token):
        self.__data["accountReference"] = token_hex(5)
        self.__data["customerEmail"] = f"{token_hex(3)}@test.com"

        code, result = self.__instance.create_reserved_account( self.__data)
        assert code == 200
        return result["responseBody"]["accountReference"]

    def test_account_creation(self, token):

        self.__data["accountReference"] = token_hex(5)
        self.__data["customerEmail"] = f"{token_hex(3)}@test.com"

        code, result = self.__instance.create_reserved_account( self.__data)
        assert code == 200
        self.__data.pop("bvn")

        with pytest.raises(ValidationError):
            self.__data["accountReference"] = token_hex(5)
            self.__data["customerEmail"] = f"{token_hex(3)}@test.com"
            self.__instance.create_reserved_account( self.__data)

    def test_add_linked_account(self,  get_account_reference):

        data = {
            "getAllAvailableBanks": False,
            "preferredBanks": ["232"],
            "accountReference": get_account_reference,
        }
        code, result = self.__instance.add_linked_accounts( data)
        assert code == 200

    # def test_update_kyc_info(self,  get_account_reference):

    #     data = {"bvn":"21212121212","accountReference": get_account_reference}
    #     code, result = self.__instance.update_reserved_account_kyc_info( data)
    #     assert code == 200

    def test_account_details(self,  get_account_reference):
        code, result = self.__instance.get_reserved_account_details(
             get_account_reference
        )
        assert code == 200

    def test_account_transactions(self,  get_account_reference):
        code, result = self.__instance.get_reserved_account_transactions(
             get_account_reference
        )
        assert code == 200

    def test_account_deallocation(self,  get_account_reference):
        code, result = self.__instance.deallocate_reserved_account(
             get_account_reference
        )
        assert code == 200


class TestInvoiceAPIs:

    @pytest.fixture(autouse=True)
    def instantiate_class(self):
        self.__instance = Invoice(
            os.environ.get("API_KEY"), os.environ.get("SECRET_KEY")
        )

    @pytest.fixture(autouse=True)
    def initialize_data(self):
        self.__data = {
            "amount": "999",
            "description": "test invoice",
            "currencyCode": "NGN",
            "contractCode": "7059707855",
            "customerEmail": "johnsnow@gmail.com",
            "customerName": "John Snow",
            "expiryDate": "2025-05-30 12:00:00",
            "paymentMethods": [],
            "incomeSplitConfig": [
                {
                    "subAccountCode": "MFY_SUB_456786606061",
                    "feePercentage": 10.5,
                    "splitAmount": 20,
                    "feeBearer": True,
                }
            ],
            "metaData": {"phoneNumber": "07044987067", "location": "Shangai"},
            "redirectUrl": "http://app.monnify.com",
        }

    @pytest.fixture()
    def get_reference(self):
        self.__data["invoiceReference"] = token_hex(5)
        _, result = self.__instance.create_invoice( self.__data)
        return result["responseBody"]["invoiceReference"]


    def test_invoice_creation(self, token):

        self.__data["invoiceReference"] = token_hex(5)

        code, result = self.__instance.create_invoice( self.__data)
        assert code == 200
        self.__data["incomeSplitConfig"][0].pop("splitAmount")

        with pytest.raises(ValidationError):
            self.__data["invoiceReference"] = token_hex(5)
            self.__instance.create_invoice( self.__data)

    def test_invoice_details(self,  get_reference):
        code, result = self.__instance.get_invoice_details( get_reference)
        assert code == 200

    def test_all_invoice(self):
        code, result = self.__instance.get_all_invoices()
        assert code == 200

    def test_delete_invoice(self,  get_reference):
        code, result = self.__instance.cancel_invoice( get_reference)
        assert code == 200
