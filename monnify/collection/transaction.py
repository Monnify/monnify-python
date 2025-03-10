from ..base import Base
from urllib import parse as url_encoder

from ..validators.transaction_validator import (
    InitTransactionSchema, 
    BankTransferSchema, 
    ChargeCardSchema,
    AuthorizeOTPSchema,
    ThreeDsSchema,
    CardTokenSchema,
    USSDPaymentSchema)


class Transaction(Base):

    def __init__(
        self: object, API_KEY: str = None, SECRET_KEY: str = None, ENV: str = "SANDBOX"
    ) -> None:

        super().__init__(API_KEY, SECRET_KEY, ENV)


    def initialize_transaction(self, auth_token, data) -> tuple:

        validated_data = InitTransactionSchema().load(data)
        url_path = "/api/v1/merchant/transactions/init-transaction"
        return self.do_post(url_path, auth_token, validated_data)


    def get_transaction_status_v2(self, auth_token, transaction_reference) -> tuple:

        encoded_reference = url_encoder.quote_plus(transaction_reference)
        url_path = "/api/v2/transactions/" + encoded_reference
        return self.do_get(url_path, auth_token)


    def get_transaction_status_v1(
        self, auth_token, payment_reference=None, transaction_reference=None
    ) -> tuple:

        if payment_reference is None and transaction_reference is None:
            raise Exception(
                "At least one of payment or transaction reference is required!!"
            )

        url_path = (
            "/api/v2/merchant/transactions/query?transactionReference="
            + url_encoder.quote_plus(transaction_reference)
            if (payment_reference is None)
            else "/api/v2/merchant/transactions/query?paymentReference="
            + url_encoder.quote_plus(payment_reference)
        )
        return self.do_get(url_path, auth_token)


    def pay_with_ussd(self, auth_token, data) -> tuple:

        validated_data = USSDPaymentSchema().load(data)

        url_path = "/api/v1/merchant/ussd/initialize"
        return self.do_post(url_path, auth_token, validated_data)


    def pay_with_bank_transfer(self, auth_token, data) -> tuple:

        validated_data = BankTransferSchema().load(data)

        url_path = "/api/v1/merchant/bank-transfer/init-payment"
        return self.do_post(url_path, auth_token, validated_data)


    def charge_card(self, auth_token, data) -> tuple:

        validated_data = ChargeCardSchema().load(data)

        url_path = "/api/v1/merchant/cards/charge"
        return self.do_post(url_path, auth_token, validated_data)


    def authorize_otp(self, auth_token, data) -> tuple:

        validated_data = AuthorizeOTPSchema().load(data)

        url_path = "/api/v1/merchant/cards/otp/authorize"
        return self.do_post(url_path, auth_token, validated_data)


    def three_d_secure_auth_transaction(self, auth_token, data) -> tuple:

        validated_data = ThreeDsSchema().load(data)

        url_path = "/api/v1/sdk/cards/secure-3d/authorize"
        return self.do_post(url_path, auth_token, validated_data)


    def card_tokenization(self, auth_token, data) -> tuple:

        validated_data = CardTokenSchema().load(data)

        url_path = "/api/v1/merchant/cards/charge-card-token"
        return self.do_post(url_path, auth_token, validated_data)
