from marshmallow import (
    Schema,
    fields,
    validate,
    validates_schema,
    ValidationError,
    post_load,
)
from . import is_numeric, SplitConfigSchema


class InitTransactionSchema(Schema):
    """
    Schema for initializing a transaction.

    Attributes:
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

    Methods:
        validate_schema(data, **kwargs): Validates the schema to ensure either splitPercentage or splitAmount is provided in incomeSplitConfig.
        parse_decimal(item, many, **kwargs): Converts amount and splitAmount to string after loading.
    """

    paymentReference = fields.Str(required=True)
    amount = fields.Decimal(required=True)
    customerName = fields.Str()
    paymentDescription = fields.Str(required=True, validate=[validate.Length(min=3)])
    currencyCode = fields.Str(required=True, default="NGN")
    contractCode = fields.Str(
        required=True, validate=[validate.Length(min=10), is_numeric]
    )
    customerEmail = fields.Email(required=True)
    paymentMethods = fields.List(fields.Str())
    redirectUrl = fields.Url(required=False)
    metaData = fields.Dict(keys=fields.Str())
    incomeSplitConfig = fields.List(fields.Nested(SplitConfigSchema), required=False)

    @validates_schema(skip_on_field_errors=False)
    def validate_schema(self, data, **kwargs):
        if data.get("incomeSplitConfig"):
            for param in data.get("incomeSplitConfig"):
                if (
                    param.get("splitPercentage") is None
                    and param.get("splitAmount") is None
                ):
                    raise ValidationError(
                        "Either splitPercentage or splitAmount is required"
                    )

    @post_load
    def parse_decimal(self, item, many, **kwargs):
        item["amount"] = str(item["amount"])
        split_data = item.pop("incomeSplitConfig", None)
        if split_data is not None:
            for data in split_data:
                if data.get("splitAmount"):
                    data["splitAmount"] = str(data["splitAmount"])
            item["incomeSplitConfig"] = split_data

        return item


class BankTransferSchema(Schema):
    """
    Schema for bank transfer transactions.

    Attributes:
        transactionReference (str): The Monnify transaction reference, gotten from the transaction init endpoint
        bankCode (str): The bank code to generate USSD string for the returnd account number
    """

    transactionReference = fields.Str(required=True)
    bankCode = fields.Str(required=False, validate=[is_numeric])


class USSDPaymentSchema(Schema):
    """
    Schema for USSD payment transactions.

    Attributes:
        transactionReference (str): The Monnify transaction reference, gotten from the transaction init endpoint
        bankUssdCode (str): The bank USSD code for the bank customer is paying from
    """

    transactionReference = fields.Str(required=True)
    bankUssdCode = fields.Str(required=True, validate=[is_numeric])


class CardSchema(Schema):
    """
    Schema for card details.

    Attributes:
        number (str): The card number, required with a minimum length of 16 and must be numeric.
        expiryMonth (str): The card expiry month, required with a length of 2 and must be numeric.
        expiryYear (str): The card expiry year, required with a length of 4 and must be numeric.
        pin (str): The card PIN, required with a length of 4 and must be numeric.
        cvv (str): The card CVV, required with a length of 3 and must be numeric.
    """

    number = fields.Str(required=True, validate=[validate.Length(min=16), is_numeric])
    expiryMonth = fields.Str(
        required=True, validate=[validate.Length(min=2, max=2), is_numeric]
    )
    expiryYear = fields.Str(
        required=True, validate=[validate.Length(min=4), is_numeric]
    )
    pin = fields.Str(required=True, validate=[validate.Length(min=4), is_numeric])
    cvv = fields.Str(required=True, validate=[validate.Length(min=3), is_numeric])


class ChargeCardSchema(Schema):
    """
    Schema for charging a card.

    Attributes:
        transactionReference (str): The Monnify transaction reference, gotten from the transaction init endpoint
        collectionChannel (str): The collection channel, required.
        card (CardSchema): The card details, required.
        deviceInformation (dict): Device information dictionary with string keys, required.
    """

    transactionReference = fields.Str(required=True)
    collectionChannel = fields.Str(required=True)
    card = fields.Nested(CardSchema, required=True)
    deviceInformation = fields.Dict(keys=fields.Str(), required=True)


class AuthorizeOTPSchema(Schema):
    """
    Schema for authorizing OTP.

    Attributes:
        transactionReference (str): The Monnify transaction reference, gotten from the transaction init endpoint.
        collectionChannel (str): The collection channel, required.
        tokenId (str): The token ID, gotten from the charge card endpoint.
        token (str): The token, required and must be numeric.
    """

    transactionReference = fields.Str(required=True)
    collectionChannel = fields.Str(required=True)
    tokenId = fields.Str(required=True)
    token = fields.Str(required=True, validate=[is_numeric])


class ThreeDsSchema(Schema):
    """
    Schema for 3D secure transactions.

    Attributes:
        transactionReference (str): The Monnify transaction reference, gotten from the transaction init endpoint.
        collectionChannel (str): The collection channel, required.
        apikey (str): The API key, required.
        card (CardSchema): The card details, required.
    """

    transactionReference = fields.Str(required=True)
    collectionChannel = fields.Str(required=True)
    apikey = fields.Str(required=True)
    card = fields.Nested(CardSchema, required=True)


class CardTokenSchema(Schema):
    """
    Schema for card token transactions.

    Attributes:
        paymentReference (str): The payment reference, required.
        amount (Decimal): The transaction amount, required.
        customerName (str): The customer's name, required.
        paymentDescription (str): The payment description, required.
        cardToken (str): The Monnify card token, required.
        currencyCode (str): The currency code, default is "NGN".
        contractCode (str): The contract code, required with a minimum length of 10 and must be numeric.
        customerEmail (Email): The customer's email, required.
        apikey (str): The API key, required.
        metaData (dict): Metadata dictionary with string keys.

    Methods:
        parse_decimal(item, many, **kwargs): Converts amount to string after loading.
    """

    paymentReference = fields.Str(required=True)
    amount = fields.Decimal(required=True)
    customerName = fields.Str(required=True)
    paymentDescription = fields.Str(required=True)
    cardToken = fields.Str(required=True)
    currencyCode = fields.Str(required=True, default="NGN")
    contractCode = fields.Str(
        required=True, validate=[validate.Length(min=10), is_numeric]
    )
    customerEmail = fields.Email(required=True)
    apikey = fields.Str(required=True)
    metaData = fields.Dict(keys=fields.Str())

    @post_load
    def parse_decimal(self, item, many, **kwargs):
        item["amount"] = str(item["amount"])
        return item
