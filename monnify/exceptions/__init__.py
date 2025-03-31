class CustomBaseException(Exception):
    def __init__(self, message, error_code=None):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)

    def __str__(self):
        return f"[Error {self.error_code}] {self.message}"


class UnprocessableRequestException(CustomBaseException):
    pass


class GatewayException(CustomBaseException):
    pass


class DuplicateInstanceException(CustomBaseException):

    def __str__(self):
        return f"{self.message}"


class InvalidDataException(CustomBaseException):

    def __str__(self):
        return f"{self.message}"
    
class GlobalException(CustomBaseException):
    
    def __str__(self):
        return f"{self.message}"
