from marshmallow import Schema, fields, validates_schema, ValidationError, validate

from . import is_numeric


class BVNVerificationSchema(Schema):
    """
    Schema for BVN (Bank Verification Number) verification.

    Attributes:
        bvn (str): The BVN number, must be exactly 11 digits.
        name (str): The name of the customer.
        mobileNo (str): The mobile number of the customer, must be exactly 11 digits.
        dateOfBirth (str): The date of birth of the customer.
    """

    bvn = fields.Str(
        required=True, validate=[validate.Length(min=11, max=11), is_numeric]
    )
    name = fields.Str(required=True)
    mobileNo = fields.Str(
        required=True, validate=[validate.Length(min=11, max=11), is_numeric]
    )
    dateOfBirth = fields.Str(required=True)


class BVNMatchSchema(Schema):
    """
    Schema for matching BVN with bank details.

    Attributes:
        bvn (str): The BVN number, must be exactly 11 digits.
        bankCode (str): The bank code of the bank linked to the account number, must be numeric.
        accountNumber (str): The account number, must be exactly 10 digits.
    """

    bvn = fields.Str(
        required=True, validate=[validate.Length(min=11, max=11), is_numeric]
    )
    bankCode = fields.Str(required=True, validate=[is_numeric])
    accountNumber = fields.Str(
        required=True, validate=[validate.Length(min=10, max=10), is_numeric]
    )


class NINVerificationSchema(Schema):
    """
    Schema for NIN (National Identification Number) verification.

    Attributes:
        nin (str): The NIN number, must be exactly 11 digits.
    """

    nin = fields.Str(
        required=True, validate=[validate.Length(min=11, max=11), is_numeric]
    )
