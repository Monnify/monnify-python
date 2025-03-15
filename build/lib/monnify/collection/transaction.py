from ..base import Base
from urllib import parse as url_encoder

from ..validators.transaction_validator import (
    InitTransactionSchema,
    BankTransferSchema,
    ChargeCardSchema,
    AuthorizeOTPSchema,
    ThreeDsSchema,
    CardTokenSchema,
    USSDPaymentSchema,
)


class Transaction(Base):
    """
    The Monnify Transaction API class
    """

    def __init__(
        self: object, API_KEY: str = None, SECRET_KEY: str = None, ENV: str = "SANDBOX"
    ) -> None:

        super().__init__(API_KEY, SECRET_KEY, ENV)

    def initialize_transaction(self, auth_token, data) -> tuple:
        """
        Initializes a transaction 

        Args:
            auth_token (str): The authentication token for the API.
            data (dict): The data required to initialize the transaction as outlined:
                paymentReference (str): The payment reference, required.
                amount (Decimal): The transaction amount, required.
                customerName (str): The customer's name.
                paymentDescription (str): The payment description, required with a minimum length of 3.
                currencyCode (str): The currency code, default is "NGN".
                contractCode (str): The merchant's contract code, required with a minimum length of 10 and must be numeric.
                customerEmail (Email): The customer's email, required.
                paymentMethods (list): List of supported payment methods.
                redirectUrl (Url): The redirect URL after payment completion.
                metaData (dict): Metadata dictionary with string keys.
                incomeSplitConfig (list): List of income split configurations.


        Returns:
            tuple: The status code and response from the API call.
        """

        validated_data = InitTransactionSchema().load(data)
        url_path = "/api/v1/merchant/transactions/init-transaction"
        return self.do_post(url_path, auth_token, validated_data)

    def get_transaction_status_v2(self, auth_token, transaction_reference) -> tuple:
        """
        Retrieve the status of a transaction using its reference.

        Args:
            auth_token (str): The authentication token for the API.
            transaction_reference (str): The Monnify reference of the transaction to check.

        Returns:
            tuple: A tuple containing the response status and data from the API.
        """

        encoded_reference = url_encoder.quote_plus(transaction_reference)
        url_path = "/api/v2/transactions/" + encoded_reference
        return self.do_get(url_path, auth_token)

    def get_transaction_status_v1(
        self, auth_token, payment_reference=None, transaction_reference=None
    ) -> tuple:
        """
        Get the status of a transaction.

        This method retrieves the status of a transaction using either the payment reference or the transaction reference.
        At least one of the references must be provided.

        Args:
            auth_token (str): The authentication token required for the API call.
            payment_reference (str, optional): The payment reference of the transaction. Defaults to None.
            transaction_reference (str, optional): The transaction reference of the transaction. Defaults to None.

        Raises:
            Exception: If both payment_reference and transaction_reference are None.

        Returns:
            tuple: The status code and response from the API call.
        """

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
        """
        Initialize a USSD payment.

        This method validates the provided data using the USSDPaymentSchema,
        constructs the URL path for the USSD payment initialization, and
        performs a POST request to the Monnify API.

        Args:
            auth_token (str): The authentication token for the API request.
            data (dict): The data required for the USSD payment initialization as outlined below:
                transactionReference (str): The Monnify transaction reference, gotten from the transaction init endpoint
                bankUssdCode (str): The bank USSD code for the bank customenr is paying from

        Returns:
            tuple: The status code and response from the API call.
        """

        validated_data = USSDPaymentSchema().load(data)

        url_path = "/api/v1/merchant/ussd/initialize"
        return self.do_post(url_path, auth_token, validated_data)

    def pay_with_bank_transfer(self, auth_token, data) -> tuple:
        """
        Initiates a payment using bank transfer.

        Args:
            auth_token (str): The authentication token for the API.
            data (dict): The data required for the bank transfer, as outlined below:
                transactionReference (str): The Monnify transaction reference, gotten from the transaction init endpoint
                bankCode (str): The bank code to generate USSD string for the returned account number
        Returns:
            tuple: The status code and response from the API call.
        """

        validated_data = BankTransferSchema().load(data)

        url_path = "/api/v1/merchant/bank-transfer/init-payment"
        return self.do_post(url_path, auth_token, validated_data)

    def charge_card(self, auth_token, data) -> tuple:
        """
        Charges a card using the provided authentication token and card data.

        Args:
            auth_token (str): The authentication token for the request.
            data (dict): The data required to charge the card as outlined below:
                transactionReference (str): The Monnify transaction reference, gotten from the transaction init endpoint
                collectionChannel (str): The collection channel, required.
                card (CardSchema): The card details, required.
                deviceInformation (dict): Device information dictionary with string keys, required.


        Returns:
            tuple: The status code and response from the API call.

        Raises:
            ValidationError: If the provided data is invalid.
        """

        validated_data = ChargeCardSchema().load(data)

        url_path = "/api/v1/merchant/cards/charge"
        return self.do_post(url_path, auth_token, validated_data)

    def authorize_otp(self, auth_token, data) -> tuple:
        """
        Authorizes an OTP for a transaction.

        Args:
            auth_token (str): The authentication token for the request.
            data (dict): The data required for OTP authorization as outlined below:
                transactionReference (str): The Monnify transaction reference, gotten from the transaction init endpoint.
                collectionChannel (str): The collection channel, required.
                tokenId (str): The token ID, gotten from the charge card endpoint.
                token (str): The OTP for authorizing the card charge

        Returns:
            tuple: The status code and response from the OTP authorization request.
        """

        validated_data = AuthorizeOTPSchema().load(data)

        url_path = "/api/v1/merchant/cards/otp/authorize"
        return self.do_post(url_path, auth_token, validated_data)

    def three_d_secure_auth_transaction(self, auth_token, data) -> tuple:
        """
        Initiates a 3D Secure authentication transaction.

        This method sends a POST request to the Monnify API to authorize a card transaction using 3D Secure authentication.

        Args:
            auth_token (str): The authentication token for the API request.
            data (dict): The data required for the 3D Secure authentication as outlined below:
                transactionReference (str): The Monnify transaction reference, gotten from the transaction init endpoint.
                collectionChannel (str): The collection channel, required.
                apikey (str): The merchant API key, required.
                card (CardSchema): The card details, required.

        Returns:
            tuple: The response from the API, typically containing the status and any relevant data from the transaction.
        """

        validated_data = ThreeDsSchema().load(data)

        url_path = "/api/v1/sdk/cards/secure-3d/authorize"
        return self.do_post(url_path, auth_token, validated_data)

    def card_tokenization(self, auth_token, data) -> tuple:
        """
        Tokenizes a card for future transactions.

        Args:
            auth_token (str): The authentication token for the API request.
            data (dict): The data required for card tokenization as outlined below:
                paymentReference (str): The payment reference, required.
                amount (Decimal): The transaction amount, required.
                customerName (str): The customer's name, required.
                paymentDescription (str): The payment description, required.
                cardToken (str): The Monnify card token, required.
                currencyCode (str): The currency code, default is "NGN".
                contractCode (str): The merchant's contract code
                customerEmail (Email): The customer's email, required.
                apikey (str): The API key, required.
                metaData (dict): Metadata dictionary with string keys.

        Returns:
            tuple: The response from the API call, typically containing the status and the response data.
        """

        validated_data = CardTokenSchema().load(data)

        url_path = "/api/v1/merchant/cards/charge-card-token"
        return self.do_post(url_path, auth_token, validated_data)
