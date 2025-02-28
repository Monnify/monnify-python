from marshmallow import Schema, fields, validates_schema, ValidationError, validate

from validators import is_numeric, SplitConfigSchema






class ReservedAccountCreationSchema(Schema):

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
    allowedPaymentSource = fields.Dict(keys=fields.Str(), values=fields.List())

    @validates_schema
    def check_conditionally_required_fields(self, data, **kwargs):

        if data.get("bvn") and data.get("nin"):
            raise ValidationError("Either bvn or nin is required")

        if (
            data.get("restrictPaymentSource") is True
            and data.get("allowedPaymentSource") is None
        ):
            raise ValidationError(
                "allowedPaymentSource is required when restrictPaymentSource is True"
            )


class AddLinkedReservedAccountSchema(Schema):

    getAllAvailableBanks = fields.Bool(required=True, default=True)
    preferredBanks = fields.List(fields.Str(validate=[is_numeric]))


class UpdateKYCInfoSchema(Schema):

    bvn = fields.Str(validate=[validate.Length(min=11, max=11), is_numeric])
    nin = fields.Str(validate=[validate.Length(min=11, max=11), is_numeric])

    @validates_schema
    def check_conditionally_required_fields(self, data, **kwargs):

        if data.get("bvn") and data.get("nin"):
            raise ValidationError("Either bvn or nin is required")
