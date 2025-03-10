from marshmallow import Schema, fields, validates_schema, ValidationError, validate, post_load

from . import is_numeric, SplitConfigSchema




class InvoiceCreationSchema(Schema):

    invoiceReference = fields.Str(required=True)
    amount = fields.Decimal(required=True)
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

    @validates_schema(skip_on_field_errors=False)
    def validate_schema(self, data, **kwargs):

        for param in data['incomeSplitConfig']:
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
