from marshmallow import Schema, fields, validate

from validators import is_numeric




class SubAccountSchema(Schema):

    bankCode = fields.Str(required=True, validate=[is_numeric])
    accountNumber = fields.Str(required=True, validate=[validate.Length(min=10,max=10), is_numeric])
    email = fields.Email(required=True)
    currencyCode = fields.Str(required=True, default="NGN")
    defaultSplitConfig = fields.Float(required=True)
    subAccountCode = fields.Str(required=False)