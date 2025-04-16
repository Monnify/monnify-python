Module monnify.validators.settlement_validator
==============================================

Classes
-------

`SubAccountSchema(*, only: types.StrSequenceOrSet | None = None, exclude: types.StrSequenceOrSet = (), many: bool | None = None, context: dict | None = None, load_only: types.StrSequenceOrSet = (), dump_only: types.StrSequenceOrSet = (), partial: bool | types.StrSequenceOrSet | None = None, unknown: str | None = None)`
:   Schema for subAccount data.
    
    Attributes:
        data (list): A list of sub-account details, each conforming to UpdateSubSchema.

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

`post_format(self, item, many, **kwargs)`
:   Post-process deserialized data.
    
    Args:
        item (dict): The deserialized data.
        many (bool): Indicates if the input data contains multiple items.
        **kwargs: Additional keyword arguments.
    
    Returns:
        list: The post-processed data.

`pre_format(self, data, many, **kwargs)`
:   Pre-process input data before validation and deserialization.
    
    Args:
        data (dict): The input data.
        many (bool): Indicates if the input data contains multiple items.
        **kwargs: Additional keyword arguments.
    
    Returns:
        dict: The pre-processed data.

`UpdateSubSchema(*, only: types.StrSequenceOrSet | None = None, exclude: types.StrSequenceOrSet = (), many: bool | None = None, context: dict | None = None, load_only: types.StrSequenceOrSet = (), dump_only: types.StrSequenceOrSet = (), partial: bool | types.StrSequenceOrSet | None = None, unknown: str | None = None)`
:   Schema for updating sub-account details.
    
    Attributes:
        bankCode (str): The bank code for the bank, must be numeric.
        accountNumber (str): The account number needed to create the subAccount, must be 10 digits and numeric.
        email (str): The email address to receive subAccount settlement report.
        currencyCode (str): The currency code, default is "NGN".
        defaultSplitPercentage (float): The default split percentage.
        subAccountCode (str): The sub-account code, optional.

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