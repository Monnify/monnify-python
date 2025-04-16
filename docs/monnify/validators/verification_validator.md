Module monnify.validators.verification_validator
================================================

Classes
-------

`BVNMatchSchema(*, only: types.StrSequenceOrSet | None = None, exclude: types.StrSequenceOrSet = (), many: bool | None = None, context: dict | None = None, load_only: types.StrSequenceOrSet = (), dump_only: types.StrSequenceOrSet = (), partial: bool | types.StrSequenceOrSet | None = None, unknown: str | None = None)`
:   Schema for matching BVN with bank details.
    
    Attributes:
        bvn (str): The BVN number, must be exactly 11 digits.
        bankCode (str): The bank code of the bank linked to the account number, must be numeric.
        accountNumber (str): The account number, must be exactly 10 digits.

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

`BVNVerificationSchema(*, only: types.StrSequenceOrSet | None = None, exclude: types.StrSequenceOrSet = (), many: bool | None = None, context: dict | None = None, load_only: types.StrSequenceOrSet = (), dump_only: types.StrSequenceOrSet = (), partial: bool | types.StrSequenceOrSet | None = None, unknown: str | None = None)`
:   Schema for BVN (Bank Verification Number) verification.
    
    Attributes:
        bvn (str): The BVN number, must be exactly 11 digits.
        name (str): The name of the customer.
        mobileNo (str): The mobile number of the customer, must be exactly 11 digits.
        dateOfBirth (str): The date of birth of the customer.

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

`NINVerificationSchema(*, only: types.StrSequenceOrSet | None = None, exclude: types.StrSequenceOrSet = (), many: bool | None = None, context: dict | None = None, load_only: types.StrSequenceOrSet = (), dump_only: types.StrSequenceOrSet = (), partial: bool | types.StrSequenceOrSet | None = None, unknown: str | None = None)`
:   Schema for NIN (National Identification Number) verification.
    
    Attributes:
        nin (str): The NIN number, must be exactly 11 digits.

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