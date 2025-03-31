from monnify.base import Base
from urllib import parse as url_encoder

from monnify.validators.disbursement_validator import (
    BulkTransferSchema,
    AuthorizeTransferSchema,
    ResendOTPSchema,
)


class DisibursementBulk(Base):
    """
    The Monnify Bulk Disbursement API class
    """

    def __init__(
        self: object, API_KEY: str = None, SECRET_KEY: str = None, ENV: str = "SANDBOX"
    ) -> None:

        super().__init__(API_KEY, SECRET_KEY, ENV)

    def initiate_transfer(self, data, auth_token=None):
        """
        Initiates a bulk transfer.

        Args:
            auth_token (str): The authentication token for the API.
            data (dict): The data for the bulk transfer as outlined below:
                batchReference (str): The batch reference for the bulk transfer.
                narration (str): The narration for the bulk transfer.
                title (str): The title for the bulk transfer.
                currency (str): The currency for the bulk transfer, default is "NGN".
                sourceAccountNumber (str): The merchant wallet account number.
                onValidationFailure (str): Action on validation failure, default is "CONTINUE".
                notificationInterval (int): Notification interval, default is 25.
                transactionList (list): List of transactions in the bulk transfer.

        Returns:
            tuple: The status code and response from the API after initiating the bulk transfer.
        """

        validated_data = BulkTransferSchema().load(data)
        url_path = "/api/v2/disbursements/batch"
        return self.do_post(url_path, validated_data, auth_token)

    def authorize_transfer(self, data, auth_token=None):
        """
        Authorizes a transfer using the provided authentication token and data.

        Args:
            auth_token (str): The authentication token required for authorization.
            data (dict): The data required for the transfer authorization as outlined below:
                reference (str): The reference for the transfer.
                authorizationCode (str): The OTP code for the transfer.

        Returns:
            tuple: The status code and response from the server after attempting to authorize the transfer.
        """

        validated_data = AuthorizeTransferSchema().load(data)
        url_path = "/api/v2/disbursements/batch/validate-otp"
        return self.do_post(url_path, validated_data, auth_token)

    def resend_otp(self, data, auth_token=None):
        """
        Resend OTP for a disbursement transaction.

        Args:
            auth_token (str): The authentication token for the API request.
            data (dict): The data required to resend the OTP as outlined below:
                reference (str): The generated disbursement reference for the OTP resend request.

        Returns:
            tuple: The status code and response from the API after attempting to resend the OTP.
        """

        validated_data = ResendOTPSchema().load(data)
        url_path = "/api/v2/disbursements/single/resend-otp"
        return self.do_post(url_path, validated_data, auth_token)

    def get_transfer_status(self, reference, auth_token=None):
        """
        Retrieve the status of a bulk transfer.

        Args:
            auth_token (str): The authentication token required for the API request.
            reference (str): The batch reference for the bulk transfer.

        Returns:
            tuple: The response from the API along with the status of the bulk transfer.
        """

        encoded_reference = url_encoder.quote_plus(reference)
        url_path = f"/api/v2/disbursements/bulk/{encoded_reference}/transactions"
        return self.do_get(url_path, auth_token)

    def search_transactions(self, wallet_account_number, auth_token=None):
        """
        Search for transactions associated with a specific wallet account number.

        Args:
            auth_token (str): The authentication token required for the API request.
            wallet_account_number (str): The wallet account number of the merchant.

        Returns:
            tuple: The status code and response from the API containing the transaction details.
        """

        url_path = f"/api/v2/disbursements/search-transactions?sourceAccountNumber={wallet_account_number}"
        return self.do_get(url_path, auth_token)
