from marshmallow import Schema, fields, validates_schema, ValidationError, validate, post_load, INCLUDE, pre_load, EXCLUDE
from . import is_numeric


class SingleTransferSchema(Schema):

    reference = fields.Str(required=True)
    amount = fields.Decimal(required=True)
    narration = fields.Str(required=True)
    destinationBankCode = fields.Str(required=True, validate=[is_numeric])
    destinationAccountNumber = fields.Str(required=True, validate=[validate.Length(min=10,max=10), is_numeric])
    sourceAccountNumber = fields.Str(required=True, validate=[validate.Length(min=10,max=10), is_numeric])
    currency = fields.Str(required=True, default="NGN")

    class Meta:
        unknown = EXCLUDE
        

    @post_load
    def parse_decimal(self, item, many, **kwargs):
        item["amount"] = str(item["amount"])
        return item

    


class AuthorizeTransferSchema(Schema):
    reference = fields.Str(required=True)
    authorizationCode = fields.Str(required=True)


class ResendOTPSchema(Schema):
    reference = fields.Str(required=True)


class BulkTransferSchema(Schema):

    batchReference = fields.Str(required=True)
    narration = fields.Str(required=True)
    title = fields.Str(required=True)
    currency = fields.Str(required=True, default="NGN")
    sourceAccountNumber = fields.Str(required=True, validate=[validate.Length(min=10,max=10), is_numeric])
    onValidationFailure = fields.Str(required=False, default='CONTINUE')
    notificationInterval = fields.Integer(required=True, default=25)
    transactionList = fields.List(fields.Nested(SingleTransferSchema, exclude=('sourceAccountNumber',)), required=True)

    class Meta:
        unknown = EXCLUDE

    
    # @pre_load
    # def evict_field(self, data, many, **kwargs):
    #     print(data,'--------------------')
    #     schema = SingleTransferSchema()
    #     trx_data = data.pop('transactionList')
    #     if trx_data is not None:
    #         for dt in trx_data:
    #             if dt.get('sourceAccountNumber'):
    #                 dt.pop('sourceAccountNumber')
    #         data['transactionList'] = trx_data
    
    

    @post_load
    def parse_decimal(self, item, many, **kwargs):
        trx_data = item.pop('transactionList')
        if trx_data is not None:
            for data in trx_data:
                if data.get('amount'):
                    data['amount'] = str(data['amount'])
            item['transactionList'] = trx_data

        return item
