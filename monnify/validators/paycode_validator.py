from marshmallow import (
    Schema,
    fields,
    validates_schema,
    ValidationError,
    validate,
    post_load,
    INCLUDE,
    pre_load,
    EXCLUDE,
)
from . import is_numeric



class PaycodeSchema(Schema):
    """
    Schema for paycode transactions.

    Attributes:
        amount (decimal): The amount to be paid.
        beneficiaryName (str): The name of the beneficiary.
        paycodeReference (str): The paycode reference.
        clientId (str): The merchant API key.
        expiryDate (str): The expiry date of the paycode.
    """

    amount = fields.Decimal(required=True)
    beneficiaryName = fields.Str(required=True)
    paycodeReference = fields.Str(required=True)
    clientId = fields.Str(required=True)
    expiryDate = fields.Str(required=True)

    
    @post_load
    def parse_decimal(self, item, many, **kwargs):
        item["amount"] = str(item["amount"])
        return item