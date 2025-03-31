Module monnify.validators.invoice_validator
===========================================

Classes
-------

`InvoiceCreationSchema(*, only: types.StrSequenceOrSet | None = None, exclude: types.StrSequenceOrSet = (), many: bool | None = None, context: dict | None = None, load_only: types.StrSequenceOrSet = (), dump_only: types.StrSequenceOrSet = (), partial: bool | types.StrSequenceOrSet | None = None, unknown: str | None = None)`
:   A schema for validating the creation of an invoice
    
    Attributes:
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

    ### Ancestors (in MRO)

    * marshmallow.schema.Schema
    * marshmallow.base.SchemaABC
    * abc.ABC

    ### Class variables

    `OPTIONS_CLASS: type`
    :   Defines defaults for `marshmallow.Schema.Meta`.

    `TYPE_MAPPING: dict[type, type[Field]]`
    :

    `error_messages: dict[str, str]`
    :

    `opts: typing.Any`
    :

    ### Methods

    `parse_decimal(self, item, many, **kwargs)`
    :   Post-load processing to convert Decimal fields to strings.
        
        Args:
            item (dict): The deserialized item.
            many (bool): Whether the item is a list of items.
            **kwargs: Additional keyword arguments.
        
        Returns:
            dict: The processed item with Decimal fields converted to strings.

    `validate_schema(self, data, **kwargs)`
    :   Custom schema validation to ensure either splitPercentage or splitAmount is provided
        in each incomeSplitConfig entry.
        
        Args:
            data (dict): The data to validate.
            **kwargs: Additional keyword arguments.
        
        Raises:
            ValidationError: If neither splitPercentage nor splitAmount is provided.