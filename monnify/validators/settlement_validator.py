from marshmallow import Schema, fields, validate, pre_load, post_load

from . import is_numeric


class UpdateSubSchema(Schema):
    bankCode = fields.Str(required=True, validate=[is_numeric])
    accountNumber = fields.Str(required=True, validate=[validate.Length(min=10,max=10), is_numeric])
    email = fields.Email(required=True)
    currencyCode = fields.Str(required=True, default="NGN")
    defaultSplitPercentage = fields.Float(required=True)
    subAccountCode = fields.Str(required=False)


class SubAccountSchema(Schema):

    data = fields.Nested(UpdateSubSchema, required=True,many=True)
    

    @pre_load
    def pre_format(self, data, many, **kwargs):
        return {"data": data}
    
    @post_load
    def post_format(self, item, many, **kwargs):
        return item.pop('data')