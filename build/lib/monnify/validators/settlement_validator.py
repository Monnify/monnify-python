from marshmallow import Schema, fields, validate, pre_load, post_load

from . import is_numeric


class UpdateSubSchema(Schema):
    """
    Schema for updating sub-account details.

    Attributes:
        bankCode (str): The bank code for the bank, must be numeric.
        accountNumber (str): The account number needed to create the subAccount, must be 10 digits and numeric.
        email (str): The email address to receive subAccount settlement report.
        currencyCode (str): The currency code, default is "NGN".
        defaultSplitPercentage (float): The default split percentage.
        subAccountCode (str): The sub-account code, optional.
    """

    bankCode = fields.Str(required=True, validate=[is_numeric])
    accountNumber = fields.Str(
        required=True, validate=[validate.Length(min=10, max=10), is_numeric]
    )
    email = fields.Email(required=True)
    currencyCode = fields.Str(required=True, default="NGN")
    defaultSplitPercentage = fields.Float(required=True)
    subAccountCode = fields.Str(required=False)


class SubAccountSchema(Schema):
    """
    Schema for subAccount data.

    Attributes:
        data (list): A list of sub-account details, each conforming to UpdateSubSchema.
    """

    data = fields.Nested(UpdateSubSchema, required=True, many=True)

    @pre_load
    def pre_format(self, data, many, **kwargs):
        """
        Pre-process input data before validation and deserialization.

        Args:
            data (dict): The input data.
            many (bool): Indicates if the input data contains multiple items.
            **kwargs: Additional keyword arguments.

        Returns:
            dict: The pre-processed data.
        """

        return {"data": data}

    @post_load
    def post_format(self, item, many, **kwargs):
        """
        Post-process deserialized data.

        Args:
            item (dict): The deserialized data.
            many (bool): Indicates if the input data contains multiple items.
            **kwargs: Additional keyword arguments.

        Returns:
            list: The post-processed data.
        """
        return item.pop("data")
