Module monnify.validators
=========================

Sub-modules
-----------
* monnify.validators.disbursement_validator
* monnify.validators.invoice_validator
* monnify.validators.paycode_validator
* monnify.validators.reserved_account_validator
* monnify.validators.settlement_validator
* monnify.validators.transaction_validator
* monnify.validators.verification_validator

Functions
---------

`is_numeric(value)`
:   

Classes
-------

`SplitConfigSchema(*, only: types.StrSequenceOrSet | None = None, exclude: types.StrSequenceOrSet = (), many: bool | None = None, context: dict | None = None, load_only: types.StrSequenceOrSet = (), dump_only: types.StrSequenceOrSet = (), partial: bool | types.StrSequenceOrSet | None = None, unknown: str | None = None)`
:   Base schema class with which to define schemas.
    
  Example usage:
  
  .. code-block:: python
  
      import datetime as dt
      from dataclasses import dataclass
  
      from marshmallow import Schema, fields
  
  
      @dataclass
      class Album:
          title: str
          release_date: dt.date
  
  
      class AlbumSchema(Schema):
          title = fields.Str()
          release_date = fields.Date()
  
  
      album = Album("Beggars Banquet", dt.date(1968, 12, 6))
      schema = AlbumSchema()
      data = schema.dump(album)
      data  # {'release_date': '1968-12-06', 'title': 'Beggars Banquet'}
  
  :param only: Whitelist of the declared fields to select when
      instantiating the Schema. If None, all fields are used. Nested fields
      can be represented with dot delimiters.
  :param exclude: Blacklist of the declared fields to exclude
      when instantiating the Schema. If a field appears in both `only` and
      `exclude`, it is not used. Nested fields can be represented with dot
      delimiters.
  :param many: Should be set to `True` if ``obj`` is a collection
      so that the object will be serialized to a list.
  :param context: Optional context passed to :class:`fields.Method` and
      :class:`fields.Function` fields.
  :param load_only: Fields to skip during serialization (write-only fields)
  :param dump_only: Fields to skip during deserialization (read-only fields)
  :param partial: Whether to ignore missing fields and not require
      any fields declared. Propagates down to ``Nested`` fields as well. If
      its value is an iterable, only missing fields listed in that iterable
      will be ignored. Use dot delimiters to specify nested fields.
  :param unknown: Whether to exclude, include, or raise an error for unknown
      fields in the data. Use `EXCLUDE`, `INCLUDE` or `RAISE`.
  
  .. versionchanged:: 3.0.0
      `prefix` parameter removed.

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