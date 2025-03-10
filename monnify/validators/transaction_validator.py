from marshmallow import Schema, fields, validate, validates_schema, ValidationError, post_load
from . import is_numeric, SplitConfigSchema





class InitTransactionSchema(Schema):

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
        if data.get('incomeSplitConfig'):
            for param in data.get('incomeSplitConfig'):
                if param.get("splitPercentage") is None and param.get("splitAmount") is None:
                    raise ValidationError("Either splitPercentage or splitAmount is required")
            
    @post_load
    def parse_decimal(self, item, many, **kwargs):
        item["amount"] = str(item["amount"])
        split_data = item.pop('incomeSplitConfig',None)
        if split_data is not None:
            for data in split_data:
                if data.get('splitAmount'):
                    data['splitAmount'] = str(data['splitAmount'])
            item['incomeSplitConfig'] = split_data

        return item




class BankTransferSchema(Schema):

    transactionReference = fields.Str(required=True)
    bankCode = fields.Str(required=False, validate=[is_numeric])


class USSDPaymentSchema(Schema):

    transactionReference = fields.Str(required=True)
    bankUssdCode = fields.Str(required=True, validate=[is_numeric])




class CardSchema(Schema):

    number = fields.Str(required=True, validate=[validate.Length(min=16), is_numeric])
    expiryMonth = fields.Str(required=True, validate=[validate.Length(min=2, max=2), is_numeric])
    expiryYear = fields.Str(required=True, validate=[validate.Length(min=4), is_numeric])
    pin = fields.Str(required=True, validate=[validate.Length(min=4), is_numeric])
    cvv = fields.Str(required=True, validate=[validate.Length(min=3), is_numeric])



class ChargeCardSchema(Schema):

    transactionReference = fields.Str(required=True)
    collectionChannel = fields.Str(required=True)
    card = fields.Nested(CardSchema, required=True)
    deviceInformation = fields.Dict(keys=fields.Str(),required=True)


class AuthorizeOTPSchema(Schema):

    transactionReference = fields.Str(required=True)
    collectionChannel = fields.Str(required=True)
    tokenId = fields.Str(required=True)
    token = fields.Str(required=True, validate=[is_numeric])


class ThreeDsSchema(Schema):

    transactionReference = fields.Str(required=True)
    collectionChannel = fields.Str(required=True)
    apikey = fields.Str(required=True)
    card = fields.Nested(CardSchema, required=True)


class CardTokenSchema(Schema):

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