class BaseException(Exception):
    """Base template for custom exceptions."""

    message = "An error occurred"

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class InvalidEruptionDateTimeException(BaseException):
    message = "Invalid date passed"
