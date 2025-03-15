from ..base import Base
from urllib import parse as url_encoder
from ..validators.reserved_account_validator import (
    ReservedAccountCreationSchema,
    AddLinkedReservedAccountSchema,
    UpdateKYCInfoSchema,
    ValidationError,
)


class ReservedAccount(Base):
    """
    The Monnify Reserved Account API class
    """    

    def __init__(
        self: object, API_KEY: str = None, SECRET_KEY: str = None, ENV: str = "SANDBOX"
    ) -> None:

        super().__init__(API_KEY, SECRET_KEY, ENV)

    def create_reserved_acount(self: object, auth_token: str, data: dict) -> tuple:
        """
        Creates reserved account.

        This method sends a POST request to the Monnify API to create a reserved account.

        Args:
            self (object): The instance of the class.
            auth_token (str): The authentication token required for the API request.
            data (dict): The data required for creating the reserved account as outlined below:
                accountReference (str): Unique reference for the account, required.
                accountName (str): Name of the account, required.
                customerName (str): Name of the customer, required.
                currencyCode (str): Currency code, default is "NGN".
                contractCode (str): Contract code, required and must be numeric with a minimum length of 10.
                customerEmail (str): Email of the customer, required.
                bvn (str): Bank Verification Number, must be numeric with a length of 11.
                nin (str): National Identification Number, must be numeric with a length of 11.
                getAllAvailableBanks (bool): Flag to get all available banks, required and default is True.
                preferredBanks (list): List of preferred banks, must be numeric.
                incomeSplitConfig (list): List of income split configurations, optional.
                restrictPaymentSource (bool): Flag to restrict payment source, optional and default is False.
                allowedPaymentSource (dict): Dictionary of allowed payment sources, required if restrictPaymentSource is True.


        Returns:
            tuple: The response from the API, typically containing the status code and the response data.
        """

        validated_data = ReservedAccountCreationSchema().load(data)
        url_path = "/api/v2/bank-transfer/reserved-accounts"
        return self.do_post(url_path, auth_token, validated_data)

    def add_linked_accounts(self, auth_token, data) -> tuple:
        """
        Add linked accounts to a reserved account.

        This method helps add a new bank to an existing reserved account.

        Args:
            auth_token (str): The authentication token for the API request.
            data (dict): The data containing the account information as outlined below:
                getAllAvailableBanks (bool): Flag to get all available banks, required and default is True.
                preferredBanks (list): List of preferred banks, must be numeric.
                accountReference (str): Reference for the existing reserved account, required.

        Returns:
            tuple: The response from the API, typically containing the status code and the response data.
        """

        validated_data = AddLinkedReservedAccountSchema().load(data)
        encoded_reference = url_encoder.quote_plus(validated_data["accountReference"])
        url_path = (
            "/api/v1/bank-transfer/reserved-accounts/add-linked-accounts/"
            + encoded_reference
        )
        return self.do_put(url_path, auth_token, validated_data)

    def get_reserved_account_details(self, auth_token: str, account_reference: str):
        """
        Retrieve the details of a reserved account.

        Args:
            auth_token (str): The authentication token required for the API request.
            account_reference (str): The reference identifier for the reserved account.

        Returns:
            tuple: The status code and details of the reserved account as returned by the API.
        """

        encoded_reference = url_encoder.quote_plus(account_reference)
        url_path = "/api/v2/bank-transfer/reserved-accounts/" + encoded_reference
        return self.do_get(url_path, auth_token)

    def deallocate_reserved_account(self, auth_token, account_reference) -> tuple:
        """
        Deallocates a reserved account.

        This method sends a DELETE request to the Monnify API to deallocate a reserved account
        based on the provided account reference.

        Args:
            auth_token (str): The authentication token required to authorize the request.
            account_reference (str): The reference of the reserved account to be deallocated.

        Returns:
            tuple: A tuple containing the response status and data from the API.
        """

        encoded_reference = url_encoder.quote_plus(account_reference)
        url_path = (
            "/api/v1/bank-transfer/reserved-accounts/reference/" + encoded_reference
        )
        return self.do_delete(url_path, auth_token)

    def update_reserved_account_kyc_info(self, auth_token, data) -> tuple:
        """
        Update the BVN/NIN information for a reserved account.

        Args:
            auth_token (str): The authentication token required for the API request.
            data (dict): A dictionary containing the BVN/NIN information to be updated as outlined below:
                accountReference (str): Reference for the reserved account, required.
                bvn (str): The customer's BVN (Bank Verification Number)
                nin (str): The customer's NIN (National Identification Number)

        Returns:
            tuple: A tuple containing the response status and the response data from the API.

        Raises:
            ValidationError: If the provided data does not match the schema.
        """

        validated_data = UpdateKYCInfoSchema().load(data)

        encoded_reference = url_encoder.quote_plus(validated_data["accountReference"])
        url_path = (
            "/api/v1/bank-transfer/reserved-accounts/" + encoded_reference + "/kyc-info"
        )
        return self.do_put(url_path, auth_token, validated_data)

    def get_reserved_account_transactions(
        self, auth_token, account_reference, page=0, size=10
    ):
        """
        Retrieve transactions for a reserved account.

        Args:
            auth_token (str): The authentication token for the API.
            account_reference (str): The reference of the reserved account.
            page (int, optional): The page number of the transactions to retrieve. Defaults to 0.
            size (int, optional): The number of transactions per page. Defaults to 10.

        Returns:
            dict: The response from the API containing the transactions.
        """

        encoded_reference = url_encoder.quote_plus(account_reference)
        url_path = f"/api/v1/bank-transfer/reserved-accounts/transactions?accountReference={encoded_reference}&page={page}&size={size}"
        return self.do_get(url_path, auth_token)
