from monnify.base import Base

from monnify.validators.verification_validator import (
    BVNMatchSchema,
    BVNVerificationSchema,
    NINVerificationSchema,
)


class Verification(Base):
    """
    This class is used to verify BVN, NIN and bank account details.
    """

    def __init__(
        self: object, API_KEY: str = None, SECRET_KEY: str = None, ENV: str = "SANDBOX"
    ) -> None:

        super().__init__(API_KEY, SECRET_KEY, ENV)

    def verify_bvn(self, auth_token, data):
        """
        Verify BVN (Bank Verification Number) details.

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
        """

        validated_data = BVNVerificationSchema().load(data)

        url_path = "/api/v1/vas/bvn-details-match"
        return self.do_post(url_path, auth_token, data)

    def match_bvn_with_account_name(self, auth_token, data):
        """
        Matches a BVN (Bank Verification Number) with the supplied account name.

        Args:
            auth_token (str): The authentication token required for the API request.
            data (dict): The data to be validated as outlined below:
                bvn (str): The supplied BVN number, must be exactly 11 digits.
                bankCode (str): The bank code of the bank linked to the account number, must be numeric.
                accountNumber (str): The customer's account number

        Returns:
            tuple: The status and response from the API call.
        """

        validated_data = BVNMatchSchema().load(data)

        url_path = "/api/v1/vas/bvn-account-match"
        return self.do_post(url_path, auth_token, data)

    def verify_nin(self, auth_token, data):
        """
        This method verifies the NIN supplied by the customer.

        Args:
            auth_token (str): The authentication token required for the API request.
            data (dict): The data containing NIN details to be verified as outlined below:
                nin (str): The NIN number, must be exactly 11 digits.

        Returns:
            tuple: The status and response from the Monnify API containing the verification result.
        """

        validated_data = NINVerificationSchema().load(data)

        url_path = "/api/v1/vas/nin-details"
        return self.do_post(url_path, auth_token, data)

    def validate_bank_account(self, auth_token, account_number, bank_code):
        """
        Validate a bank account using the provided account number and bank code.

        Args:
            auth_token (str): The authentication token for the API request.
            account_number (str): The bank account number to be validated.
            bank_code (str): The code of the bank where the account is held.

        Returns:
            tuple: The status code and response from the API containing the validation result.
    """

        url_path = f"/api/v1/disbursements/account/validate?accountNumber={account_number}&bankCode={bank_code}"
        return self.do_get(url_path, auth_token)
