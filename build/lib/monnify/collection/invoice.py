from ..base import Base
from urllib import parse as url_encoder

from ..validators.invoice_validator import InvoiceCreationSchema


class Invoice(Base):
    """
    The Monnify Invoice API class
    """    

    def __init__(
        self: object, API_KEY: str = None, SECRET_KEY: str = None, ENV: str = "SANDBOX"
    ) -> None:

        super().__init__(API_KEY, SECRET_KEY, ENV)

    def create_invoice(self, auth_token, data) -> tuple:
        """
        Create an invoice using the provided authentication token and data.

        Parameters:
        auth_token (str): The authentication token required for the API request.

        data (dict): The data required to create the invoice outlined below
            invoiceReference (str): Unique reference for the invoice.
            amount (Decimal): Amount to be invoiced.
            accountReference (str, optional): Reference for the account.
            customerName (str): Name of the customer.
            description (str): Description of the invoice.
            currencyCode (str): Currency code for the invoice, default is "NGN".
            contractCode (str): Contract code, must be numeric and at least 10 characters long.
            customerEmail (str): Email of the customer.
            paymentMethods (list of str): List of payment methods.
            expiryDate (str): Expiry date of the invoice.
            redirectUrl (str, optional): URL to redirect after payment.
            metaData (dict): Additional metadata for the invoice.
            incomeSplitConfig (list of SplitConfigSchema, optional): Configuration for income splitting.

        Returns:
        tuple: API status code and a json response
        """
        
        validated_data = InvoiceCreationSchema().load(data)

        url_path = "/api/v1/merchant/transactions/init-transaction"
        return self.do_post(url_path, auth_token, validated_data)

    def get_invoice_details(self, auth_token, invoice_reference) -> tuple:
        """
        Retrieve the details of a specific invoice.

        Args:
            auth_token (str): The authentication token required for the API request.
            invoice_reference (str): The reference used in generating the invoice.

        Returns:
            tuple: API status code and a json response
        """

        encoded_reference = url_encoder.quote_plus(invoice_reference)
        url_path = f"/api/v1/invoice/{encoded_reference}/details"
        return self.do_get(url_path, auth_token)

    def get_all_invoices(self, auth_token, page=0, size=10):
        """
        Retrieve all created invoices with pagination.

        Args:
            auth_token (str): The authentication token for the API.
            page (int, optional): The page number to retrieve. Defaults to 0.
            size (int, optional): The number of invoices per page. Defaults to 10.

        Returns:
            tuple: API status code and a json response
        """

        url_path = f"/api/v1/invoice/all?page={page}&size={size}"
        return self.do_get(url_path, auth_token)

    def cancel_invoice(self, auth_token, invoice_reference):
        """
        Cancel an invoice.

        This method cancels an invoice using the provided invoice reference.

        Args:
            auth_token (str): The authentication token required for the API request.
            invoice_reference (str): The reference of the invoice to be canceled.

        Returns:
            tuple: API status code and a json response
        """

        encoded_reference = url_encoder.quote_plus(invoice_reference)
        url_path = f"/api/v1/invoice/{encoded_reference}/cancel"
        return self.do_get(url_path, auth_token)
