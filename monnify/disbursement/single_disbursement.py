from monnify.base import Base
from urllib import parse as url_encoder

from monnify.validators.disbursement_validator import (
    SingleTransferSchema,
    AuthorizeTransferSchema,
    ResendOTPSchema,
)


class DisbursementSingle(Base):
    """
    The Monnify Single Disbursement API class
    """

    def __init__(
        self: object, API_KEY: str = None, SECRET_KEY: str = None, ENV: str = "SANDBOX"
    ) -> None:

        super().__init__(API_KEY, SECRET_KEY, ENV)

    def initiate_transfer(self, data, auth_token=None):
        """
        Initiates a single transfer disbursement.

        Args:
            auth_token (str): The authentication token for the API.
            data (dict): The data required for the transfer as outlined below:
                reference (str): Unique reference for the transfer.
                amount (decimal): Amount to be transferred.
                narration (str): Description or narration for the transfer.
                destinationBankCode (str): Bank code of the destination bank.
                destinationAccountNumber (str): Account number of the destination account.
                sourceAccountNumber (str): The wallet account number of the source account.
                currency (str): Currency of the transfer, default is "NGN".
                async (bool): Whether to process the transfer asynchronously, default is False.

        Returns:
            tuple: The status code and response from the API after initiating the transfer.
        """

        validated_data = SingleTransferSchema().load(data)

        url_path = "/api/v2/disbursements/single"
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

        url_path = "/api/v2/disbursements/single/validate-otp"
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
            reference (str): The generated reference for the single transfer.

        Returns:
            tuple: The response from the API along with the status of the single transfer.
        """

        encoded_reference = url_encoder.quote_plus(reference)
        url_path = f"/api/v2/disbursements/single/summary?reference={encoded_reference}"
        return self.do_get(url_path, auth_token)

    def list_all_transfers(self, page=0, size=10, auth_token=None):
        """
        List all single disbursement transactions.

        Args:
            auth_token (str): The authentication token for the API.
            page (int, optional): The page number to retrieve. Defaults to 0.
            size (int, optional): The number of transactions per page. Defaults to 10.

        Returns:
            tuple: The response from the API along with the status code of the request.
        """

        url_path = (
            f"/api/v2/disbursements/single/transactions?pageNo={page}&pageSize={size}"
        )
        return self.do_get(url_path, auth_token)

    def get_wallet_balance(self, wallet_account_number, auth_token=None):
        """
        Retrieve the balance of the merchant's Monnify wallet.

        Args:
            auth_token (str): The authentication token for the API request.
            wallet_account_number (str): The merchant wallet account number

        Returns:
            tuple: The response from the API along with the status code of the request.
        """

        url_path = f"/api/v2/disbursements/wallet-balance?accountNumber={wallet_account_number}"
        return self.do_get(url_path, auth_token)
