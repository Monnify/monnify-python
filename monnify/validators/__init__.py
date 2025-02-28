from marshmallow import Schema, fields, validates_schema, ValidationError, validate





def is_numeric(value):
    if value.isdigit() is False:
        raise ValidationError("String must be numeric")
    



class SplitConfigSchema(Schema):
    
    subAccountCode = fields.Str(required=True)
    feeBearer = fields.Bool(required=True, default=False)
    feePercentage = fields.Float()
    splitPercentage = fields.Float()
    splitAmount = fields.Decimal(rounding=2)

    @validates_schema
    def validate_schema(self, data, **kwargs):

        if data.get("splitPercentage") and data.get("splitAmount"):
            raise ValidationError("Either splitPercentage or splitAmount is required")