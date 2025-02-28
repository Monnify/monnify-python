from marshmallow import Schema, fields, validates_schema, ValidationError, validate
from validators import is_numeric


class SingleTransferSchema(Schema):

    reference = fields.Str(required=True)
    amount = fields.Decima(required=True)
    narration = fields.Str(required=True)
    destinationBankCode = fields.Str(required=True, validate=[is_numeric])
    destinationAccountNumber = fields.Str(required=True, validate=[validate.Length(min=10,max=10), is_numeric])
    sourceAccountNumber = fields.Str(required=True, validate=[validate.Length(min=10,max=10), is_numeric])
    currency = fields.Str(required=True, default="NGN")
    #Async = fields.Bool(required=False, default=False)

    def __init__(self, *args, **kwargs):
        exclude_fields = kwargs.pop("exclude_fields", [])
        super().__init__(*args, **kwargs)
        
        for field_name in exclude_fields:
            self.fields.pop(field_name, None)
    


class AuthorizeTransferSchema(Schema):
    reference = fields.Str(required=True)
    authorizationCode = fields.Str(required=True)


class ResendOTPSchema(Schema):
    reference = fields.Str(required=True)


class BulkTransferSchema(Schema):

    batchReference = fields.Str(required=True)
    amount = fields.Decima(required=True)
    narration = fields.Str(required=True)
    title = fields.Str(required=True)
    sourceAccountNumber = fields.Str(required=True, validate=[validate.Length(min=10,max=10), is_numeric])
    onValidationFailure = fields.Str(required=True, default='CONTINUE')
    notificationInterval = fields.Integer(required=True, default=25)
    transactionList = fields.List(fields.Nested(SingleTransferSchema, excluded_fields=["sourceAccountNumber"]), required=True)