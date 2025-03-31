Module monnify.disbursement.paycode
===================================

Classes
-------

`Paycode(API_KEY: str = None, SECRET_KEY: str = None, ENV: str = 'SANDBOX')`
:   The Monnify Paycode API class
    
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

    `create_paycode(self, data, auth_token=None)`
    :   Create a paycode using the provided data.
        
        This method validates the input data using the `PaycodeSchema` 
        and sends a POST request to the Monnify API to create a paycode.
        
        Args:
            data (dict): The data required to create the paycode. 
                amount (decimal): The amount to be paid.
                beneficiaryName (str): The name of the beneficiary.
                paycodeReference (str): The paycode reference.
                clientId (str): The merchant API key.
                expiryDate (str): The expiry date of the paycode.
        
            auth_token (str, optional): The authentication token to authorize the request. 
        
        Returns:
            tuple: The status code and response from the Monnify API after creating the paycode.

    `delete_paycode(self, paycode_reference, auth_token=None)`
    :   Deletes a paycode using the paycode reference.
        Args:
            paycode_reference (str): The paycode reference.
            auth_token (str, optional): The authentication token. Defaults to None.
        Returns:
            tuple: The status code and response from the Monnify API after deleting the paycode.

    `fetch_paycodes(self, start_date, end_date, transaction_status='PAID', auth_token=None)`
    :   Fetches all paycodes within a specified date range.
        Args:
            start_date (str): The start date for the date range.
            end_date (str): The end date for the date range.
            transaction_status (str, optional): The transaction status. Defaults to 'PAID'.
            auth_token (str, optional): The authentication token. Defaults to None.
        Returns:
            tuple: The status code and response from the Monnify API after fetching the paycodes.

    `get_clear_paycode(self, paycode_reference, auth_token=None)`
    :   This method fetches details of a paycode in clear text using the paycode reference.
        Args:
            paycode_reference (str): The paycode reference.
            auth_token (str, optional): The authentication token. Defaults to None.
        
        Returns:
            tuple: The status code and response from the Monnify API after fetching the paycode.

    `get_paycode(self, paycode_reference, auth_token=None)`
    :   This method fetches details of a paycode using the paycode reference.
        Args:
            paycode_reference (str): The paycode reference.
            auth_token (str, optional): The authentication token. Defaults to None.
        
        Returns:
            tuple: The status code and response from the Monnify API after fetching the paycode.