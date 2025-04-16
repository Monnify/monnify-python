from monnify.base import Base
from urllib import parse as url_encoder

from monnify.validators.paycode_validator import (
    PaycodeSchema
)


class Paycode(Base):
    """
    The Monnify Paycode API class
    """

    def __init__(
        self: object, API_KEY: str = None, SECRET_KEY: str = None, ENV: str = "SANDBOX"
    ) -> None:

        super().__init__(API_KEY, SECRET_KEY, ENV)

    def create_paycode(self, data, auth_token=None):
        """
        Create a paycode using the provided data.

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
        """

        validated_data = PaycodeSchema().load(data)

        url_path = "/api/v1/paycode"
        return self.do_post(url_path, validated_data, auth_token)
    
    
    def get_paycode(self, paycode_reference, auth_token=None):
        """
        This method fetches details of a paycode using the paycode reference.
        Args:
            paycode_reference (str): The paycode reference.
            auth_token (str, optional): The authentication token. Defaults to None.

        Returns:
            tuple: The status code and response from the Monnify API after fetching the paycode.
        """
    
        encoded_reference = url_encoder.quote_plus(paycode_reference)
        url_path = f"/api/v1/paycode/{encoded_reference}"
        return self.do_get(url_path, auth_token)
    
    def get_clear_paycode(self, paycode_reference, auth_token=None):
        """
        This method fetches details of a paycode in clear text using the paycode reference.
        Args:
            paycode_reference (str): The paycode reference.
            auth_token (str, optional): The authentication token. Defaults to None.

        Returns:
            tuple: The status code and response from the Monnify API after fetching the paycode.
        """
        
        encoded_reference = url_encoder.quote_plus(paycode_reference)
        url_path = f"/api/v1/paycode/{encoded_reference}/authorize"
        return self.do_get(url_path, auth_token)
    
    def fetch_paycodes(self, start_date, end_date, transactionStatus=None, transactionReference=None,
                       beneficiaryName=None, auth_token=None):
        """
        Fetches all paycodes within a specified date range.
        Args:
            start_date (str): The start date for the date range.
            end_date (str): The end date for the date range.
            transaction_status (str, optional): The transaction status. Defaults to 'PAID'.
            transactionReference (str, optional): The transaction reference. Defaults to None.
            auth_token (str, optional): The authentication token. Defaults to None.
        Returns:
            tuple: The status code and response from the Monnify API after fetching the paycodes.
            """
        
        url_path = f"/api/v1/paycode?from={start_date}&to={end_date}"
        if transactionStatus:
            url_path += f"&transactionStatus={transactionStatus}"
        if transactionReference:
            url_path += f"&transactionReference={url_encoder.quote_plus(transactionReference)}"
        if beneficiaryName:
            url_path += f"&beneficiaryName={url_encoder.quote_plus(beneficiaryName)}"
        return self.do_get(url_path, auth_token)
    
    def delete_paycode(self, paycode_reference, auth_token=None):
        """
        Deletes a paycode using the paycode reference.
        Args:
            paycode_reference (str): The paycode reference.
            auth_token (str, optional): The authentication token. Defaults to None.
        Returns:
            tuple: The status code and response from the Monnify API after deleting the paycode.
        """
        
        encoded_reference = url_encoder.quote_plus(paycode_reference)
        url_path = f"/api/v1/paycode/{encoded_reference}"
        return self.do_delete(url_path, auth_token)