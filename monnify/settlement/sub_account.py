from monnify.base import Base
from urllib import parse as url_encoder

from monnify.validators.settlement_validator import SubAccountSchema, UpdateSubSchema


class Settlement(Base):
    """
    The Monnify Settlement API class
    """

    def __init__(
        self: object, API_KEY: str = None, SECRET_KEY: str = None, ENV: str = "SANDBOX"
    ) -> None:

        super().__init__(API_KEY, SECRET_KEY, ENV)

    def create_sub_account(self, data, auth_token=None):
        """
        Create a new sub-account.

        This method sends a POST request to the Monnify API to create a new sub-account
        using the provided authentication token and data.

        Args:
            auth_token (str): The authentication token for the API.
            data (dict): The data required to create the sub-account as outlined below:
                bankCode (str): The bank code for the bank, must be numeric.
                accountNumber (str): The account number needed to create the subAccount, must be 10 digits and numeric.
                email (str): The email address to receive subAccount settlement report.
                currencyCode (str): The currency code, default is "NGN".
                defaultSplitPercentage (float): The default split percentage.


        Returns:
            tuple: The status code and response from the Monnify API after creating the sub-account.
        """

        validated_data = SubAccountSchema().load(data)

        url_path = "/api/v1/sub-accounts"
        return self.do_post(url_path, validated_data, auth_token)

    def update_sub_account(self, data, auth_token=None):
        """
        Update a sub-account with the provided data.

        Args:
            auth_token (str): The authentication token for the API request.
            data (dict): The data to update the sub-account with,as outlined below:
                subAccountCode (str): The subAccount code to update.
                email (str): The email address to receive subAccount settlement report.
                currencyCode (str): The currency code, default is "NGN".
                defaultSplitPercentage (float): The default split percentage.

        Returns:
            tuple: The status code and response from the Monnify API after upating the subAccount.
        """

        validated_data = UpdateSubSchema().load(data)

        url_path = "/api/v1/sub-accounts"
        return self.do_put(url_path, validated_data, auth_token)

    def get_sub_accounts(self, auth_token=None):
        """
        Retrieve a list of subAccounts.

        Args:
            auth_token (str): The authentication token required to access the API.

        Returns:
            tuple: The status code and response from the API containing the list of subAccounts.
        """

        url_path = f"/api/v1/sub-accounts"
        return self.do_get(url_path, auth_token)

    def delete_sub_account(self, sub_account_code, auth_token=None):
        """
        Deletes a sub-account.

        Args:
            auth_token (str): The authentication token required for the API call.
            sub_account_code (str): The code of the sub-account to be deleted.

        Returns:
            Response: The response from the API call.
        """

        url_path = f"/api/v1/sub-accounts/{sub_account_code}"
        return self.do_delete(url_path, auth_token)

    def get_transaction_by_settlement_reference(
        self, settlement_reference, page=0, size=10, auth_token=None
    ):
        """
        Retrieve transactions by settlement reference.

        Args:
            auth_token (str): The authentication token for the API.
            settlement_reference (str): The settlement reference to search for.
            page (int, optional): The page number to retrieve. Defaults to 0.
            size (int, optional): The number of records per page. Defaults to 10.

        Returns:
            tuple: The status code and response from the API
        """

        encoded_reference = url_encoder.quote_plus(settlement_reference)
        url_path = f"/api/v1/transactions/find-by-settlement-reference?settlement-reference={encoded_reference}&page={page}&size={size}"
        return self.do_get(url_path, auth_token)

    def get_settlement_status_by_transaction_reference(
        self, transaction_reference, auth_token=None
    ):
        """
        Retrieve the settlement status for a given transaction reference.

        Args:
            auth_token (str): The authentication token for the API request.
            transaction_reference (str): The reference of the transaction to check the settlement status for.

        Returns:
            tuple: The status code and response from the API containing the settlement status details.
        """

        encoded_reference = url_encoder.quote_plus(transaction_reference)
        url_path = f"/api/v1/settlement-detail?transactionReference={encoded_reference}"
        return self.do_get(url_path, auth_token)
