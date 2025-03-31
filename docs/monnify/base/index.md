Module monnify.base
===================

Classes
-------

`Base(API_KEY: str = None, SECRET_KEY: str = None, ENV: str = 'SANDBOX')`
:   The base monnify classes from which other classes inherits
    
    Raises:
        DuplicateInstanceException: This is thrown when two instances of different enviroments or API key are created
    
        InvalidDataException: This is thrown when the class is instantiated with invalid data
    
        UnprocessableRequestException: This is thrown when the API request cannot be processed
    
        GatewayException: This is thrown when there's a server error with the API
    
        RequestException: This is thrown when there's an issue with the API request
    Returns:
        _type_: An instance of Base
    
    Initialises the Base class
    
    Args:
        API_KEY (str): _description_. Merchant API Key.
        SECRET_KEY (str): _description_. Merchant Secret Key.
        ENV (str): _description_. API environment, defaults to "SANDBOX".
    
    Raises:
        InvalidDataException

### Descendants

* monnify.collection.invoice.Invoice
* monnify.collection.reserved_account.ReservedAccount
* monnify.collection.transaction.Transaction
* monnify.collection.transaction.TransactionRefund
* monnify.disbursement.bulk_disbursement.DisibursementBulk
* monnify.disbursement.paycode.Paycode
* monnify.disbursement.single_disbursement.DisbursementSingle
* monnify.settlement.sub_account.Settlement
* monnify.verification.kyc_verification.Verification

### Static methods

`reset_token_config()`
:   Resets the token configuration

`update_token_threshold(threshold: int)`
:   Updates the token threshold

### Methods

`compare_hash(self: object, payload: bytes, monnify_signature: str) ‑> bool`
:   Webhook signature comparison utility
    
    Args:
        self (object): The class instance
        payload (bytes): Webhook payload in byte sent from Monnify
        monnify_signature (str): A string of the webhook hash from Monnify
    
    Returns:
        bool: A boolean value denoting if there's a match between the computed hash and Monnify's

`do_delete(self: object, url_path: str, authorization: str = None) ‑> tuple`
:   A low level Delete request to the Monnify API
    
    Args:
        self (object): The class instance
        url_path (str): The API url being requested
        authorization (str): A bearer token for authorizing the request
    
    Raises:
        UnprocessableRequestException: This is thrown when the API request cannot be processed
        GatewayException: This is thrown when there's a server error with the API
        RequestException: This is thrown when there's an issue with the API request
        Exception: A general exception
    
    Returns:
        tuple: API status code, and a json response

`do_get(self: object, url_path: str, authorization: str = None) ‑> tuple`
:   A low level GET request to the Monnify API
    
    Args:
        self (object): The class instance
        url_path (str): The API url being requested
        authorization (str): A bearer token for authorizing the request
    
    Raises:
        UnprocessableRequestException: This is thrown when the API request cannot be processed
        GatewayException: This is thrown when there's a server error with the API
        RequestException: This is thrown when there's an issue with the API request
        Exception: A general exception
    
    Returns:
        tuple: API status code, and a json response

`do_post(self: object, url_path: str, data: dict, authorization: str = None) ‑> tuple`
:   A low level POST request to the Monnify API
    
    Args:
        self (object): The class instance
        url_path (str): The API url being requested
        authorization (str): A bearer token for authorizing the request
        data (dict): A dictionary of request payload to be sent to the API
    
    Raises:
        UnprocessableRequestException: _description_
        GatewayException: _description_
        RequestException: _description_
        Exception: _description_
    
    Returns:
        tuple: API status code, and a json response

`do_put(self: object, url_path: str, data: dict, authorization: str = None) ‑> tuple`
:   A low level PUT request to the Monnify API
    
    Args:
        self (object): The class instance
        url_path (str): The API url being requested
        authorization (str): A bearer token for authorizing the request
        data (dict): A dictionary of request payload to be sent to the API
    
    Raises:
        UnprocessableRequestException: _description_
        GatewayException: _description_
        RequestException: _description_
        Exception: _description_
    
    Returns:
        tuple: API status code, and a json response

`get_auth_token(self, cache: bool = True) ‑> tuple`
:   Retrieves access token from Monnify
    
    Raises:
        UnprocessableRequestException: This is thrown when the API request cannot be processed
        GatewayException: This is thrown when there's a server error with the API
        RequestException: This is thrown when there's an issue with the API request
        Exception: A general exception
    
    Returns:
        _type_: A tuple of API status code, and a json response