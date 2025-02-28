from marshmallow import Schema, fields, validates_schema, ValidationError, validate

from validators import is_numeric, SplitConfigSchema




class InvoiceCreationSchema(Schema):

    invoiceReference = fields.Str(required=True)
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
