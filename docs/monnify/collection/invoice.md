Module monnify.collection.invoice
=================================

Classes
-------

`Invoice(API_KEY: str = None, SECRET_KEY: str = None, ENV: str = 'SANDBOX')`
:   The Monnify Invoice API class
    
    Initialises the Base class
    
    Args:
        API_KEY (str): Merchant API Key.
        SECRET_KEY (str): Merchant Secret Key.
        ENV (str): API environment, defaults to "SANDBOX".
    
    Raises:
        InvalidDataException

### Ancestors (in MRO)

* monnify.base.Base

### Methods

`cancel_invoice(self, invoice_reference, auth_token=None) ‑> tuple`
:   This method cancels an invoice using the provided invoice reference.
    
    Args:
        auth_token (str): The authentication token required for the API request.
        invoice_reference (str): The reference of the invoice to be canceled.
    
    Returns:
        tuple: API status code and a json response

`create_invoice(self, data, auth_token=None) ‑> tuple`
:   Create an invoice using the provided authentication token and data.
    
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

`get_all_invoices(self, page=0, size=10, auth_token=None) ‑> tuple`
:   Retrieve all created invoices with pagination.
    
    Args:
        auth_token (str): The authentication token for the API.
        page (int, optional): The page number to retrieve. Defaults to 0.
        size (int, optional): The number of invoices per page. Defaults to 10.
    
    Returns:
        tuple: API status code and a json response

`get_invoice_details(self, invoice_reference, auth_token=None) ‑> tuple`
:   Retrieve the details of a specific invoice.
    
    Args:
        auth_token (str): The authentication token required for the API request.
        invoice_reference (str): The reference used in generating the invoice.
    
    Returns:
        tuple: API status code and a json response