Module monnify.validators.paycode_validator
===========================================

Classes
-------

`PaycodeSchema(*, only: types.StrSequenceOrSet | None = None, exclude: types.StrSequenceOrSet = (), many: bool | None = None, context: dict | None = None, load_only: types.StrSequenceOrSet = (), dump_only: types.StrSequenceOrSet = (), partial: bool | types.StrSequenceOrSet | None = None, unknown: str | None = None)`
:   Schema for paycode transactions.
    
    Attributes:
        amount (decimal): The amount to be paid.
        beneficiaryName (str): The name of the beneficiary.
        paycodeReference (str): The paycode reference.
        clientId (str): The merchant API key.
        expiryDate (str): The expiry date of the paycode.

    ### Ancestors (in MRO)

    * marshmallow.schema.Schema
    * marshmallow.base.SchemaABC
    * abc.ABC

    ### Class variables

    `OPTIONS_CLASS: type`
    :   Defines defaults for `marshmallow.Schema.Meta`.

    `TYPE_MAPPING: dict[type, type[Field]]`
    :

    `error_messages: dict[str, str]`
    :

    `opts: typing.Any`
    :

    ### Methods

    `parse_decimal(self, item, many, **kwargs)`
    :