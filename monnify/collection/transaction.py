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
    RefundSchema
)


class Transaction(Base):
    """
    The Monnify Transaction API class
    """

    def __init__(
        self: object, API_KEY: str = None, SECRET_KEY: str = None, ENV: str = "SANDBOX"
    ) -> None:

        super().__init__(API_KEY, SECRET_KEY, ENV)

    def initialize_transaction(self, data, auth_token=None) -> tuple:
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
        return self.do_post(url_path, validated_data, auth_token)

    def get_transaction_status_v2(self, transaction_reference, auth_token=None) -> tuple:
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

    def get_transaction_status(
        self, payment_reference=None, transaction_reference=None, auth_token=None
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
    
    def get_all_transactions(self, start_date, end_date, payment_status=None, page=0, size=10, auth_token=None) -> tuple:
        """
        Retrieve all transactions with pagination.

        Args:
            auth_token (str): The authentication token for the API.
            page (int, optional): The page number to retrieve. Defaults to 0.
            size (int, optional): The number of transactions per page. Defaults to 10.
        """

        url_path =( f"/api/v1/transactions/search?page={page}&size={size}&from={start_date}&to={end_date}"
                   if payment_status is not None  
                   else f"/api/v1/transactions/search?page={page}&size={size}&from={start_date}&to={end_date}&paymentStatus={payment_status}")        
        return self.do_get(url_path, auth_token)
    

    def pay_with_ussd(self, data, auth_token=None) -> tuple:
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
        return self.do_post(url_path, validated_data, auth_token)


    def pay_with_bank_transfer(self, data, auth_token=None) -> tuple:
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
        return self.do_post(url_path, validated_data, auth_token)


    def charge_card(self, data, auth_token=None) -> tuple:
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
        return self.do_post(url_path, validated_data, auth_token)


    def authorize_otp(self, data, auth_token=None) -> tuple:
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
        return self.do_post(url_path, validated_data, auth_token)


    def three_d_secure_auth_transaction(self, data, auth_token=None) -> tuple:
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
        return self.do_post(url_path, validated_data, auth_token)


    def card_tokenization(self, data, auth_token=None) -> tuple:
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
        return self.do_post(url_path, validated_data, auth_token)


class TransactionRefund(Base):
    """
    The Monnify Transaction Refund API class
    """

    def __init__(
        self: object, API_KEY: str = None, SECRET_KEY: str = None, ENV: str = "SANDBOX"
    ) -> None:

        super().__init__(API_KEY, SECRET_KEY, ENV)


    def initiate_refund(self, data, auth_token=None) -> tuple:
        """
        Refunds a transaction.

        Args:
            auth_token (str): The authentication token for the API request.
            data (dict): The data required for the refund as outlined below:
                transactionReference (str): The Monnify transaction reference for a completed transaction.
                refundReference (str): The merchant uniquely generated refund reference, required.
                customerNote (str): The customer's note, required with a maximum length of 16.
                amount (Decimal): The refund amount, required.
                currencyCode (str): The currency code, default is "NGN".
                refundReason (str): The refund reason, required.
                contractCode (str): The contract code, required with a minimum length of 10 and must be numeric.
                destinationAcountNumber (str): The destination account number, optional with a minimum length of 10 and must be numeric.
                destinationAccountBankCode (str): The destination account bank code, optional and must be numeric.
            
        Returns:
            tuple: The response from the API call, typically containing the status and the response data.
        """
        validated_data = RefundSchema().load(data)

        url_path = "/api/v1/refunds/initiate-refund"
        return self.do_post(url_path, validated_data, auth_token)
    

    def get_refund_status(self, refund_reference, auth_token=None) -> tuple:
        """
        Retrieve the status of a refund using its refund reference.

        Args:
            auth_token (str): The authentication token for the API.
            refund_reference (str): The Merchant generated refund reference for the refund.

        Returns:
            tuple: A tuple containing the response status and data from the API.
        """

        encoded_reference = url_encoder.quote_plus(refund_reference)
        url_path = "/api/v1/refunds/" + encoded_reference
        return self.do_get(url_path, auth_token)
    
    def get_all_refunds(self, start_date, end_date, page=0, size=10, auth_token=None):
        """
        Fetches all refunds within a specified date range.

        Args:
            auth_token (str): The authentication token for the API, defaults to None.
            page (int, optional): The page number to retrieve. Defaults to 0.
            size (int, optional): The number of refunds per page. Defaults to 10.
            start_date (int): A unix timestamp in milliseconds of the start date for the refund search.
            end_date (int): A unix timestamp in milliseconds of the end date for the refund search.

        Returns:
            tuple: A tuple containing the response status and data from the API.
        """

        url_path = f"/api/v1/refunds?page={page}&size={size}&from={start_date}&to={end_date}"
        return self.do_get(url_path, auth_token)
