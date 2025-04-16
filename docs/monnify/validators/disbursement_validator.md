Module monnify.validators.disbursement_validator
================================================

Classes
-------

`AuthorizeTransferSchema(*, only: types.StrSequenceOrSet | None = None, exclude: types.StrSequenceOrSet = (), many: bool | None = None, context: dict | None = None, load_only: types.StrSequenceOrSet = (), dump_only: types.StrSequenceOrSet = (), partial: bool | types.StrSequenceOrSet | None = None, unknown: str | None = None)`
:   Schema for authorizing a transfer.
    
    Attributes:
        reference (str): The reference for the transfer.
        authorizationCode (str): The authorization code for the transfer.

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

`BulkTransferSchema(*, only: types.StrSequenceOrSet | None = None, exclude: types.StrSequenceOrSet = (), many: bool | None = None, context: dict | None = None, load_only: types.StrSequenceOrSet = (), dump_only: types.StrSequenceOrSet = (), partial: bool | types.StrSequenceOrSet | None = None, unknown: str | None = None)`
:   Schema for bulk transfer.
    
    Attributes:
        batchReference (str): The batch reference for the bulk transfer.
        narration (str): The narration for the bulk transfer.
        title (str): The title for the bulk transfer.
        currency (str): The currency for the bulk transfer, default is "NGN".
        sourceAccountNumber (str): The merchant wallet account number.
        onValidationFailure (str): Action on validation failure, default is "CONTINUE".
        notificationInterval (int): Notification interval, default is 25.
        transactionList (list): List of transactions in the bulk transfer.

  ### Ancestors (in MRO)

  * marshmallow.schema.Schema
  * marshmallow.base.SchemaABC
  * abc.ABC

  ### Class variables

  `Meta`
  :

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
  :   Post-load processing to convert decimal amount fields to string.
      
      Args:
          item (dict): The loaded data.
          many (bool): Whether the data is a list of items.
          **kwargs: Additional keyword arguments.
      
      Returns:
          dict: The processed data with amounts as strings.

`ResendOTPSchema(*, only: types.StrSequenceOrSet | None = None, exclude: types.StrSequenceOrSet = (), many: bool | None = None, context: dict | None = None, load_only: types.StrSequenceOrSet = (), dump_only: types.StrSequenceOrSet = (), partial: bool | types.StrSequenceOrSet | None = None, unknown: str | None = None)`
:   Schema for resending OTP.
    
    Attributes:
        reference (str): The reference for the OTP resend request.

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

`SingleTransferSchema(*, only: types.StrSequenceOrSet | None = None, exclude: types.StrSequenceOrSet = (), many: bool | None = None, context: dict | None = None, load_only: types.StrSequenceOrSet = (), dump_only: types.StrSequenceOrSet = (), partial: bool | types.StrSequenceOrSet | None = None, unknown: str | None = None)`
:   Schema for validating single transfer disbursement payload.
    
    Attributes:
        reference (str): Unique reference for the transfer.
        amount (decimal): Amount to be transferred.
        narration (str): Description or narration for the transfer.
        destinationBankCode (str): Bank code of the destination bank.
        destinationAccountNumber (str): Account number of the destination account.
        sourceAccountNumber (str): The wallet account number of the source account.
        currency (str): Currency of the transfer, default is "NGN".

  ### Ancestors (in MRO)

  * marshmallow.schema.Schema
  * marshmallow.base.SchemaABC
  * abc.ABC

  ### Class variables

  `Meta`
  :

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