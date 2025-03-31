from marshmallow import (
    Schema,
    fields,
    validates_schema,
    ValidationError,
    validate,
    post_load,
    INCLUDE,
    pre_load,
    EXCLUDE,
)
from . import is_numeric


class SingleTransferSchema(Schema):
    """
    Schema for validating single transfer disbursement payload.

    Attributes:
        reference (str): Unique reference for the transfer.
        amount (decimal): Amount to be transferred.
        narration (str): Description or narration for the transfer.
        destinationBankCode (str): Bank code of the destination bank.
        destinationAccountNumber (str): Account number of the destination account.
        sourceAccountNumber (str): The wallet account number of the source account.
        currency (str): Currency of the transfer, default is "NGN".
    """

    reference = fields.Str(required=True)
    amount = fields.Decimal(required=True)
    narration = fields.Str(required=True)
    destinationBankCode = fields.Str(required=True, validate=[is_numeric])
    destinationAccountNumber = fields.Str(
        required=True, validate=[validate.Length(min=10, max=10), is_numeric]
    )
    sourceAccountNumber = fields.Str(
        required=True, validate=[validate.Length(min=10, max=10), is_numeric]
    )
    currency = fields.Str(required=True, default="NGN")

    class Meta:
        unknown = INCLUDE

    @post_load
    def parse_decimal(self, item, many, **kwargs):
        item["amount"] = str(item["amount"])
        return item


class AuthorizeTransferSchema(Schema):
    """
    Schema for authorizing a transfer.

    Attributes:
        reference (str): The reference for the transfer.
        authorizationCode (str): The authorization code for the transfer.
    """

    reference = fields.Str(required=True)
    authorizationCode = fields.Str(required=True)


class ResendOTPSchema(Schema):
    """
    Schema for resending OTP.

    Attributes:
        reference (str): The reference for the OTP resend request.
    """

    reference = fields.Str(required=True)


class BulkTransferSchema(Schema):
    """
    Schema for bulk transfer.

    Attributes:
        batchReference (str): The batch reference for the bulk transfer.
        narration (str): The narration for the bulk transfer.
        title (str): The title for the bulk transfer.
        currency (str): The currency for the bulk transfer, default is "NGN".
        sourceAccountNumber (str): The merchant wallet account number.
        onValidationFailure (str): Action on validation failure, default is "CONTINUE".
        notificationInterval (int): Notification interval, default is 25.
        transactionList (list): List of transactions in the bulk transfer.
    """

    batchReference = fields.Str(required=True)
    narration = fields.Str(required=True)
    title = fields.Str(required=True)
    currency = fields.Str(required=True, default="NGN")
    sourceAccountNumber = fields.Str(
        required=True, validate=[validate.Length(min=10, max=10), is_numeric]
    )
    onValidationFailure = fields.Str(required=False, default="CONTINUE")
    notificationInterval = fields.Integer(required=True, default=25)
    transactionList = fields.List(
        fields.Nested(SingleTransferSchema, exclude=("sourceAccountNumber",)),
        required=True,
    )

    class Meta:
        unknown = EXCLUDE


    @post_load
    def parse_decimal(self, item, many, **kwargs):
        """
        Post-load processing to convert decimal amount fields to string.

        Args:
            item (dict): The loaded data.
            many (bool): Whether the data is a list of items.
            **kwargs: Additional keyword arguments.

        Returns:
            dict: The processed data with amounts as strings.
        """

        trx_data = item.pop("transactionList")
        if trx_data is not None:
            for data in trx_data:
                if data.get("amount"):
                    data["amount"] = str(data["amount"])
            item["transactionList"] = trx_data

        return item
