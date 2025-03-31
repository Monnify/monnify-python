Module monnify.validators.reserved_account_validator
====================================================

Classes
-------

`AddLinkedReservedAccountSchema(*, only: types.StrSequenceOrSet | None = None, exclude: types.StrSequenceOrSet = (), many: bool | None = None, context: dict | None = None, load_only: types.StrSequenceOrSet = (), dump_only: types.StrSequenceOrSet = (), partial: bool | types.StrSequenceOrSet | None = None, unknown: str | None = None)`
:   Schema for adding a linked reserved account.
    
    Attributes:
        getAllAvailableBanks (bool): Flag to get all available banks, required and default is True.
        preferredBanks (list): List of preferred banks, must be numeric.
        accountReference (str): Reference for the account, required.

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

`ReservedAccountCreationSchema(*, only: types.StrSequenceOrSet | None = None, exclude: types.StrSequenceOrSet = (), many: bool | None = None, context: dict | None = None, load_only: types.StrSequenceOrSet = (), dump_only: types.StrSequenceOrSet = (), partial: bool | types.StrSequenceOrSet | None = None, unknown: str | None = None)`
:   Schema for validating the creation of a reserved account.
    
    Attributes:
        accountReference (str): Unique reference for the account, required.
        accountName (str): Name of the account, required.
        customerName (str): Name of the customer, required.
        currencyCode (str): Currency code, default is "NGN".
        contractCode (str): Contract code, required and must be numeric with a minimum length of 10.
        customerEmail (str): Email of the customer, required.
        bvn (str): Bank Verification Number, must be numeric with a length of 11.
        nin (str): National Identification Number, must be numeric with a length of 11.
        getAllAvailableBanks (bool): Flag to get all available banks, required and default is True.
        reservedAccountType (str): Type of reserved account, default is "INVOICE".
        preferredBanks (list): List of preferred banks, must be numeric.
        incomeSplitConfig (list): List of income split configurations, optional.
        restrictPaymentSource (bool): Flag to restrict payment source, optional and default is False.
        allowedPaymentSource (dict): Dictionary of allowed payment sources, required if restrictPaymentSource is True.

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
  :   Post-load processing to convert splitAmount to string.
      
      Args:
          item (dict): The deserialized item.
          many (bool): Indicates if multiple items are being processed.
      
      Returns:
          dict: The processed item with splitAmount as string.

  `validate_schema(self, data, **kwargs)`
  :   Custom schema validation.
      
      Raises:
          ValidationError: If both bvn and nin are missing.
          ValidationError: If restrictPaymentSource is True and allowedPaymentSource is missing.
          ValidationError: If both splitPercentage and splitAmount are missing in incomeSplitConfig.

`UpdateKYCInfoSchema(*, only: types.StrSequenceOrSet | None = None, exclude: types.StrSequenceOrSet = (), many: bool | None = None, context: dict | None = None, load_only: types.StrSequenceOrSet = (), dump_only: types.StrSequenceOrSet = (), partial: bool | types.StrSequenceOrSet | None = None, unknown: str | None = None)`
:   Schema for updating KYC (Know Your Customer) information.
    
    Attributes:
        bvn (str): Bank Verification Number, must be numeric with a length of 11.
        nin (str): National Identification Number, must be numeric with a length of 11.
        accountReference (str): Reference for the account, required.

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

  `check_conditionally_required_fields(self, data, **kwargs)`
  :   Custom schema validation.
      
      Raises:
          ValidationError: If both bvn and nin are not provided.