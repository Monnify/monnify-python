Module monnify.verification.kyc_verification
============================================

Classes
-------

`Verification(API_KEY: str = None, SECRET_KEY: str = None, ENV: str = 'SANDBOX')`
:   This class is used to verify BVN, NIN and bank account details.
    
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

`match_bvn_with_account_name(self, data, auth_token=None)`
:   Matches a BVN (Bank Verification Number) with the supplied account name.
    
    Args:
        auth_token (str): The authentication token required for the API request.
        data (dict): The data to be validated as outlined below:
            bvn (str): The supplied BVN number, must be exactly 11 digits.
            bankCode (str): The bank code of the bank linked to the account number, must be numeric.
            accountNumber (str): The customer's account number
    
    Returns:
        tuple: The status and response from the API call.

`validate_bank_account(self, account_number, bank_code, auth_token=None)`
:   Validate a bank account using the provided account number and bank code.
    
    Args:
        auth_token (str): The authentication token for the API request.
        account_number (str): The bank account number to be validated.
        bank_code (str): The code of the bank where the account is held.
    
    Returns:
        tuple: The status code and response from the API containing the validation result.

`verify_bvn(self, data, auth_token=None)`
:   Verify BVN (Bank Verification Number) details.
    
    This method validates the provided data using the BVNVerificationSchema
    and sends a POST request to the Monnify API to verify the BVN details.
    
    Args:
        auth_token (str): The authentication token for the API request.
        data (dict): The data to be validated as outlined below:
            bvn (str): The BVN number, must be exactly 11 digits.
            name (str): The name of the customer.
            mobileNo (str): The mobile number of the customer, must be exactly 11 digits.
            dateOfBirth (str): The date of birth of the customer.
    
    Returns:
        tuple: The status code and response from the Monnify API containing the verification result.

`verify_nin(self, data, auth_token=None)`
:   This method verifies the NIN supplied by the customer.
    
    Args:
        auth_token (str): The authentication token required for the API request.
        data (dict): The data containing NIN details to be verified as outlined below:
            nin (str): The NIN number, must be exactly 11 digits.
    
    Returns:
        tuple: The status and response from the Monnify API containing the verification result.