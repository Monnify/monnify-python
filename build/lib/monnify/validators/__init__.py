from marshmallow import Schema, fields, validates_schema, ValidationError, validate

"""from .invoice_validator import *
from .reserved_account_validator import *
from .transaction_validator import *
from .settlement_validator import *"""


def is_numeric(value):
    if value.isdigit() is False:
        raise ValidationError("String must be numeric")


class SplitConfigSchema(Schema):

    subAccountCode = fields.Str(required=True)
    feeBearer = fields.Bool(required=True, default=False)
    feePercentage = fields.Float()
    splitPercentage = fields.Float()
    splitAmount = fields.Decimal(rounding=2)
