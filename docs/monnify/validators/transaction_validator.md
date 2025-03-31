Module monnify.validators.transaction_validator
===============================================

Classes
-------

`AuthorizeOTPSchema(*, only: types.StrSequenceOrSet | None = None, exclude: types.StrSequenceOrSet = (), many: bool | None = None, context: dict | None = None, load_only: types.StrSequenceOrSet = (), dump_only: types.StrSequenceOrSet = (), partial: bool | types.StrSequenceOrSet | None = None, unknown: str | None = None)`
:   Schema for authorizing OTP.
    
    Attributes:
        transactionReference (str): The Monnify transaction reference, gotten from the transaction init endpoint.
        collectionChannel (str): The collection channel, required.
        tokenId (str): The token ID, gotten from the charge card endpoint.
        token (str): The token, required and must be numeric.

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

`BankTransferSchema(*, only: types.StrSequenceOrSet | None = None, exclude: types.StrSequenceOrSet = (), many: bool | None = None, context: dict | None = None, load_only: types.StrSequenceOrSet = (), dump_only: types.StrSequenceOrSet = (), partial: bool | types.StrSequenceOrSet | None = None, unknown: str | None = None)`
:   Schema for bank transfer transactions.
    
    Attributes:
        transactionReference (str): The Monnify transaction reference, gotten from the transaction init endpoint
        bankCode (str): The bank code to generate USSD string for the returnd account number

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

`CardSchema(*, only: types.StrSequenceOrSet | None = None, exclude: types.StrSequenceOrSet = (), many: bool | None = None, context: dict | None = None, load_only: types.StrSequenceOrSet = (), dump_only: types.StrSequenceOrSet = (), partial: bool | types.StrSequenceOrSet | None = None, unknown: str | None = None)`
:   Schema for card details.
    
    Attributes:
        number (str): The card number, required with a minimum length of 16 and must be numeric.
        expiryMonth (str): The card expiry month, required with a length of 2 and must be numeric.
        expiryYear (str): The card expiry year, required with a length of 4 and must be numeric.
        pin (str): The card PIN, required with a length of 4 and must be numeric.
        cvv (str): The card CVV, required with a length of 3 and must be numeric.

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

`CardTokenSchema(*, only: types.StrSequenceOrSet | None = None, exclude: types.StrSequenceOrSet = (), many: bool | None = None, context: dict | None = None, load_only: types.StrSequenceOrSet = (), dump_only: types.StrSequenceOrSet = (), partial: bool | types.StrSequenceOrSet | None = None, unknown: str | None = None)`
:   Schema for card token transactions.
    
    Attributes:
        paymentReference (str): The payment reference, required.
        amount (Decimal): The transaction amount, required.
        customerName (str): The customer's name, required.
        paymentDescription (str): The payment description, required.
        cardToken (str): The Monnify card token, required.
        currencyCode (str): The currency code, default is "NGN".
        contractCode (str): The contract code, required with a minimum length of 10 and must be numeric.
        customerEmail (Email): The customer's email, required.
        apiKey (str): The API key, required.
        metaData (dict): Metadata dictionary with string keys.
    
    Methods:
        parse_decimal(item, many, **kwargs): Converts amount to string after loading.

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

`ChargeCardSchema(*, only: types.StrSequenceOrSet | None = None, exclude: types.StrSequenceOrSet = (), many: bool | None = None, context: dict | None = None, load_only: types.StrSequenceOrSet = (), dump_only: types.StrSequenceOrSet = (), partial: bool | types.StrSequenceOrSet | None = None, unknown: str | None = None)`
:   Schema for charging a card.
    
    Attributes:
        transactionReference (str): The Monnify transaction reference, gotten from the transaction init endpoint
        collectionChannel (str): The collection channel, required.
        card (CardSchema): The card details, required.
        deviceInformation (dict): Device information dictionary with string keys, required.

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

`InitTransactionSchema(*, only: types.StrSequenceOrSet | None = None, exclude: types.StrSequenceOrSet = (), many: bool | None = None, context: dict | None = None, load_only: types.StrSequenceOrSet = (), dump_only: types.StrSequenceOrSet = (), partial: bool | types.StrSequenceOrSet | None = None, unknown: str | None = None)`
:   Schema for initializing a transaction.
    
    Attributes:
        paymentReference (str): The payment reference, required.
        amount (Decimal): The transaction amount, required.
        customerName (str): The customer's name.
        paymentDescription (str): The payment description, required with a minimum length of 3.
        currencyCode (str): The currency code, default is "NGN".
        contractCode (str): The merchant's contract code, required with a minimum length of 10 and must be numeric.
        customerEmail (Email): The customer's email, required.
        paymentMethods (list): List of supported payment methods.
        redirectUrl (Url): The redirect URL after payment completion.
        metaData (dict): Metadata dictionary with string keys.
        incomeSplitConfig (list): List of income split configurations.
    
    Methods:
        validate_schema(data, **kwargs): Validates the schema to ensure either splitPercentage or splitAmount is provided in incomeSplitConfig.
        parse_decimal(item, many, **kwargs): Converts amount and splitAmount to string after loading.

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

    `validate_schema(self, data, **kwargs)`
    :

`RefundSchema(*, only: types.StrSequenceOrSet | None = None, exclude: types.StrSequenceOrSet = (), many: bool | None = None, context: dict | None = None, load_only: types.StrSequenceOrSet = (), dump_only: types.StrSequenceOrSet = (), partial: bool | types.StrSequenceOrSet | None = None, unknown: str | None = None)`
:   Schema for refunding transactions.
    
    Attributes:
        transactionReference (str): The Monnify transaction reference for a completed transaction.
        refundReference (str): The merchant uniquely generated refund reference, required.
        customerNote (str): The customer's note, required with a maximum length of 16.
        amount (Decimal): The refund amount, required.
        currencyCode (str): The currency code, default is "NGN".
        refundReason (str): The refund reason, required.
        contractCode (str): The contract code, required with a minimum length of 10 and must be numeric.
        destinationAcountNumber (str): The destination account number, optional with a minimum length of 10 and must be numeric.
        destinationAccountBankCode (str): The destination account bank code, optional and must be numeric.
    
    Methods:
        parse_decimal(item, many, **kwargs): Converts amount to string after loading.

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

`ThreeDsSchema(*, only: types.StrSequenceOrSet | None = None, exclude: types.StrSequenceOrSet = (), many: bool | None = None, context: dict | None = None, load_only: types.StrSequenceOrSet = (), dump_only: types.StrSequenceOrSet = (), partial: bool | types.StrSequenceOrSet | None = None, unknown: str | None = None)`
:   Schema for 3D secure transactions.
    
    Attributes:
        transactionReference (str): The Monnify transaction reference, gotten from the transaction init endpoint.
        collectionChannel (str): The collection channel, required.
        apikey (str): The API key, required.
        card (CardSchema): The card details, required.

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

`USSDPaymentSchema(*, only: types.StrSequenceOrSet | None = None, exclude: types.StrSequenceOrSet = (), many: bool | None = None, context: dict | None = None, load_only: types.StrSequenceOrSet = (), dump_only: types.StrSequenceOrSet = (), partial: bool | types.StrSequenceOrSet | None = None, unknown: str | None = None)`
:   Schema for USSD payment transactions.
    
    Attributes:
        transactionReference (str): The Monnify transaction reference, gotten from the transaction init endpoint
        bankUssdCode (str): The bank USSD code for the bank customer is paying from

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