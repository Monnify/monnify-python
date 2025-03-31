Module monnify.exceptions
=========================

Classes
-------

`CustomBaseException(message, error_code=None)`
:   Common base class for all non-exit exceptions.

### Ancestors (in MRO)

* builtins.Exception
* builtins.BaseException

### Descendants

* monnify.exceptions.DuplicateInstanceException
* monnify.exceptions.GatewayException
* monnify.exceptions.GlobalException
* monnify.exceptions.InvalidDataException
* monnify.exceptions.UnprocessableRequestException

`DuplicateInstanceException(message, error_code=None)`
:   Common base class for all non-exit exceptions.

### Ancestors (in MRO)

* monnify.exceptions.CustomBaseException
* builtins.Exception
* builtins.BaseException

`GatewayException(message, error_code=None)`
:   Common base class for all non-exit exceptions.

### Ancestors (in MRO)

* monnify.exceptions.CustomBaseException
* builtins.Exception
* builtins.BaseException

`GlobalException(message, error_code=None)`
:   Common base class for all non-exit exceptions.

### Ancestors (in MRO)

* monnify.exceptions.CustomBaseException
* builtins.Exception
* builtins.BaseException

`InvalidDataException(message, error_code=None)`
:   Common base class for all non-exit exceptions.

### Ancestors (in MRO)

* monnify.exceptions.CustomBaseException
* builtins.Exception
* builtins.BaseException

`UnprocessableRequestException(message, error_code=None)`
:   Common base class for all non-exit exceptions.

### Ancestors (in MRO)

* monnify.exceptions.CustomBaseException
* builtins.Exception
* builtins.BaseException