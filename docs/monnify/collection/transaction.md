Module monnify.collection.transaction
=====================================

Classes
-------

`Transaction(API_KEY: str = None, SECRET_KEY: str = None, ENV: str = 'SANDBOX')`
:   The Monnify Transaction API class
    
    Initialises the Base class
    
    Args:
        API_KEY (str): _description_. Merchant API Key.
        SECRET_KEY (str): _description_. Merchant Secret Key.
        ENV (str): _description_. API environment, defaults to "SANDBOX".
    
    Raises:
        InvalidDataException

    ### Ancestors (in MRO)

    * monnify.base.Base

    ### Methods

    `authorize_otp(self, data, auth_token=None) ‑> tuple`
    :   Authorizes an OTP for a transaction.
        
        Args:
            auth_token (str): The authentication token for the request.
            data (dict): The data required for OTP authorization as outlined below:
                transactionReference (str): The Monnify transaction reference, gotten from the transaction init endpoint.
                collectionChannel (str): The collection channel, required.
                tokenId (str): The token ID, gotten from the charge card endpoint.
                token (str): The OTP for authorizing the card charge
        
        Returns:
            tuple: The status code and response from the OTP authorization request.

    `card_tokenization(self, data, auth_token=None) ‑> tuple`
    :   Tokenizes a card for future transactions.
        
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

    `charge_card(self, data, auth_token=None) ‑> tuple`
    :   Charges a card using the provided authentication token and card data.
        
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

    `get_all_transactions(self, start_date, end_date, payment_status=None, page=0, size=10, auth_token=None) ‑> tuple`
    :   Retrieve all transactions with pagination.
        
        Args:
            auth_token (str): The authentication token for the API.
            page (int, optional): The page number to retrieve. Defaults to 0.
            size (int, optional): The number of transactions per page. Defaults to 10.

    `get_transaction_status(self, payment_reference=None, transaction_reference=None, auth_token=None) ‑> tuple`
    :   Get the status of a transaction.
        
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

    `get_transaction_status_v2(self, transaction_reference, auth_token=None) ‑> tuple`
    :   Retrieve the status of a transaction using its reference.
        
        Args:
            auth_token (str): The authentication token for the API.
            transaction_reference (str): The Monnify reference of the transaction to check.
        
        Returns:
            tuple: A tuple containing the response status and data from the API.

    `initialize_transaction(self, data, auth_token=None) ‑> tuple`
    :   Initializes a transaction 
        
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

    `pay_with_bank_transfer(self, data, auth_token=None) ‑> tuple`
    :   Initiates a payment using bank transfer.
        
        Args:
            auth_token (str): The authentication token for the API.
            data (dict): The data required for the bank transfer, as outlined below:
                transactionReference (str): The Monnify transaction reference, gotten from the transaction init endpoint
                bankCode (str): The bank code to generate USSD string for the returned account number
        Returns:
            tuple: The status code and response from the API call.

    `pay_with_ussd(self, data, auth_token=None) ‑> tuple`
    :   Initialize a USSD payment.
        
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

    `three_d_secure_auth_transaction(self, data, auth_token=None) ‑> tuple`
    :   Initiates a 3D Secure authentication transaction.
        
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

`TransactionRefund(API_KEY: str = None, SECRET_KEY: str = None, ENV: str = 'SANDBOX')`
:   The Monnify Transaction Refund API class
    
    Initialises the Base class
    
    Args:
        API_KEY (str): _description_. Merchant API Key.
        SECRET_KEY (str): _description_. Merchant Secret Key.
        ENV (str): _description_. API environment, defaults to "SANDBOX".
    
    Raises:
        InvalidDataException

    ### Ancestors (in MRO)

    * monnify.base.Base

    ### Methods

    `get_all_refunds(self, start_date, end_date, page=0, size=10, auth_token=None)`
    :   Fetches all refunds within a specified date range.
        
        Args:
            auth_token (str): The authentication token for the API, defaults to None.
            page (int, optional): The page number to retrieve. Defaults to 0.
            size (int, optional): The number of refunds per page. Defaults to 10.
            start_date (int): A unix timestamp in milliseconds of the start date for the refund search.
            end_date (int): A unix timestamp in milliseconds of the end date for the refund search.
        
        Returns:
            tuple: A tuple containing the response status and data from the API.

    `get_refund_status(self, refund_reference, auth_token=None) ‑> tuple`
    :   Retrieve the status of a refund using its refund reference.
        
        Args:
            auth_token (str): The authentication token for the API.
            refund_reference (str): The Merchant generated refund reference for the refund.
        
        Returns:
            tuple: A tuple containing the response status and data from the API.

    `initiate_refund(self, data, auth_token=None) ‑> tuple`
    :   Refunds a transaction.
        
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