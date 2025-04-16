from marshmallow import (
    Schema,
    fields,
    validates_schema,
    ValidationError,
    validate,
    post_load,
)

from . import is_numeric, SplitConfigSchema


class InvoiceCreationSchema(Schema):
    """A schema for validating the creation of an invoice

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
    """

    invoiceReference = fields.Str(required=True)
    amount = fields.Decimal(required=True)
    accountReference = fields.Str(required=False)
    customerName = fields.Str(required=True)
    description = fields.Str(required=True)
    currencyCode = fields.Str(required=True, default="NGN")
    contractCode = fields.Str(
        required=True, validate=[validate.Length(min=10), is_numeric]
    )
    customerEmail = fields.Email(required=True)
    paymentMethods = fields.List(fields.Str())
    expiryDate = fields.Str(required=True)
    redirectUrl = fields.Url(required=False)
    metaData = fields.Dict(keys=fields.Str())
    incomeSplitConfig = fields.List(fields.Nested(SplitConfigSchema), required=False)


    @validates_schema(skip_on_field_errors=False)
    def validate_schema(self, data, **kwargs):
        """
        Custom schema validation to ensure either splitPercentage or splitAmount is provided
        in each incomeSplitConfig entry.

        Args:
            data (dict): The data to validate.
            **kwargs: Additional keyword arguments.

        Raises:
            ValidationError: If neither splitPercentage nor splitAmount is provided.
        """
        if not data.get("incomeSplitConfig"):
            return
        
        for param in data["incomeSplitConfig"]:
            if (
                param.get("splitPercentage") is None
                and param.get("splitAmount") is None
            ):
                raise ValidationError(
                    "Either splitPercentage or splitAmount is required"
                )

    @post_load
    def parse_decimal(self, item, many, **kwargs):
        """
        Post-load processing to convert Decimal fields to strings.

        Args:
            item (dict): The deserialized item.
            many (bool): Whether the item is a list of items.
            **kwargs: Additional keyword arguments.

        Returns:
            dict: The processed item with Decimal fields converted to strings.
        """

        item["amount"] = str(item["amount"])
        split_data = item.pop("incomeSplitConfig", None)
        if split_data is not None:
            for data in split_data:
                if data.get("splitAmount"):
                    data["splitAmount"] = str(data["splitAmount"])
            item["incomeSplitConfig"] = split_data

        return item
