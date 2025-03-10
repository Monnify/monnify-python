from ..base import Base
from urllib import parse as url_encoder
from ..validators.reserved_account_validator import (
    ReservedAccountCreationSchema,
    AddLinkedReservedAccountSchema,
    UpdateKYCInfoSchema,
    ValidationError,
)


class ReservedAccount(Base):

    def __init__(
        self: object, API_KEY: str = None, SECRET_KEY: str = None, ENV: str = "SANDBOX"
    ) -> None:

        super().__init__(API_KEY, SECRET_KEY, ENV)

    def create_reserved_acount(self: object, auth_token: str, data: dict) -> tuple:

        validated_data = ReservedAccountCreationSchema().load(data)
        url_path = "/api/v2/bank-transfer/reserved-accounts"
        return self.do_post(url_path, auth_token, validated_data)

    def add_linked_accounts(self, auth_token, data) -> tuple:

        validated_data = AddLinkedReservedAccountSchema().load(data)
        encoded_reference = url_encoder.quote_plus(validated_data["accountReference"])
        url_path = (
            "/api/v1/bank-transfer/reserved-accounts/add-linked-accounts/"
            + encoded_reference
        )
        return self.do_put(url_path, auth_token, validated_data)

    def get_reserved_account_details(self, auth_token: str, account_reference: str):

        encoded_reference = url_encoder.quote_plus(account_reference)
        url_path = (
            "/api/v2/bank-transfer/reserved-accounts/"
            + encoded_reference
        )
        return self.do_get(url_path, auth_token)

    def deallocate_reserved_account(self, auth_token, account_reference) -> tuple:

        encoded_reference = url_encoder.quote_plus(account_reference)
        url_path = (
            "/api/v1/bank-transfer/reserved-accounts/reference/" + encoded_reference
        )
        return self.do_delete(url_path, auth_token)

    def update_reserved_account_kyc_info(self, auth_token, data) -> tuple:

        validated_data = UpdateKYCInfoSchema().load(data)

        encoded_reference = url_encoder.quote_plus(validated_data["accountReference"])
        url_path = (
            "/api/v1/bank-transfer/reserved-accounts/" + encoded_reference + "/kyc-info"
        )
        return self.do_put(url_path, auth_token, validated_data)

    def get_reserved_account_transactions(
        self, auth_token, account_reference, page=0, size=10
    ):

        encoded_reference = url_encoder.quote_plus(account_reference)
        url_path = f"/api/v1/bank-transfer/reserved-accounts/transactions?accountReference={encoded_reference}&page={page}&size={size}"
        return self.do_get(url_path, auth_token)
