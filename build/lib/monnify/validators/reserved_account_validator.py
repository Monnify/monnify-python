from marshmallow import (
    Schema,
    fields,
    validates_schema,
    ValidationError,
    validate,
    post_load,
)

from . import is_numeric, SplitConfigSchema


class ReservedAccountCreationSchema(Schema):
    """
    Schema for validating the creation of a reserved account.

    Attributes:
        accountReference (str): Unique reference for the account, required.
        accountName (str): Name of the account, required.
        customerName (str): Name of the customer, required.
        currencyCode (str): Currency code, default is "NGN".
        contractCode (str): Contract code, required and must be numeric with a minimum length of 10.
        customerEmail (str): Email of the customer, required.
        bvn (str): Bank Verification Number, must be numeric with a length of 11.
        nin (str): National Identification Number, must be numeric with a length of 11.
        getAllAvailableBanks (bool): Flag to get all available banks, required and default is True.
        preferredBanks (list): List of preferred banks, must be numeric.
        incomeSplitConfig (list): List of income split configurations, optional.
        restrictPaymentSource (bool): Flag to restrict payment source, optional and default is False.
        allowedPaymentSource (dict): Dictionary of allowed payment sources, required if restrictPaymentSource is True.
    """

    accountReference = fields.Str(required=True)
    accountName = fields.Str(required=True)
    customerName = fields.Str(required=True)
    currencyCode = fields.Str(required=True, default="NGN")
    contractCode = fields.Str(
        required=True, validate=[validate.Length(min=10), is_numeric]
    )
    customerEmail = fields.Email(required=True)
    bvn = fields.Str(validate=[validate.Length(min=11, max=11), is_numeric])
    nin = fields.Str(validate=[validate.Length(min=11, max=11), is_numeric])
    getAllAvailableBanks = fields.Bool(required=True, default=True)
    preferredBanks = fields.List(fields.Str(validate=[is_numeric]))
    incomeSplitConfig = fields.List(fields.Nested(SplitConfigSchema), required=False)
    restrictPaymentSource = fields.Bool(required=False, default=False)
    allowedPaymentSource = fields.Dict(
        keys=fields.Str(), values=fields.List(fields.Str())
    )

    @validates_schema(skip_on_field_errors=False)
    def validate_schema(self, data, **kwargs):
        """
        Custom schema validation.

        Raises:
            ValidationError: If both bvn and nin are missing.
            ValidationError: If restrictPaymentSource is True and allowedPaymentSource is missing.
            ValidationError: If both splitPercentage and splitAmount are missing in incomeSplitConfig.
        """

        if data.get("bvn") is None and data.get("nin") is None:
            raise ValidationError("Either bvn or nin is required")

        if (
            data.get("restrictPaymentSource") is True
            and data.get("allowedPaymentSource") is None
        ):
            raise ValidationError(
                "allowedPaymentSource is required when restrictPaymentSource is True"
            )

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
        """
        Post-load processing to convert splitAmount to string.

        Args:
            item (dict): The deserialized item.
            many (bool): Indicates if multiple items are being processed.

        Returns:
            dict: The processed item with splitAmount as string.
        """

        split_data = item.pop("incomeSplitConfig", None)
        if split_data is not None:
            for data in split_data:
                if data.get("splitAmount"):
                    data["splitAmount"] = str(data["splitAmount"])
            item["incomeSplitConfig"] = split_data

        return item


class AddLinkedReservedAccountSchema(Schema):
    """
    Schema for adding a linked reserved account.

    Attributes:
        getAllAvailableBanks (bool): Flag to get all available banks, required and default is True.
        preferredBanks (list): List of preferred banks, must be numeric.
        accountReference (str): Reference for the account, required.
    """

    getAllAvailableBanks = fields.Bool(required=True, default=True)
    preferredBanks = fields.List(fields.Str(validate=[is_numeric]))
    accountReference = fields.Str(required=True)


class UpdateKYCInfoSchema(Schema):
    """
    Schema for updating KYC (Know Your Customer) information.

    Attributes:
        bvn (str): Bank Verification Number, must be numeric with a length of 11.
        nin (str): National Identification Number, must be numeric with a length of 11.
        accountReference (str): Reference for the account, required.
    """

    bvn = fields.Str(validate=[validate.Length(min=11, max=11), is_numeric])
    nin = fields.Str(validate=[validate.Length(min=11, max=11), is_numeric])
    accountReference = fields.Str(required=True)

    @validates_schema
    def check_conditionally_required_fields(self, data, **kwargs):
        """
        Custom schema validation.

        Raises:
            ValidationError: If both bvn and nin are not provided.
        """

        if data.get("bvn") is None and data.get("nin") is None:
            raise ValidationError("Either bvn or nin is required")
