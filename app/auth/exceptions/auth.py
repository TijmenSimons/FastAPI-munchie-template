"""
Auth exceptions
"""

from core.exceptions.base import CustomException


class BadUUIDException(CustomException):
    """
    Exception raised when a submitted value is not a valid UUID.

    Attributes:
        code (int): The HTTP status code associated with the exception (400).
        error_code (str): A unique error code associated with the exception ("AUTH__BAD_UUID").
        message (str): A human-readable message describing the exception 
        ("submitted value is not a uuid").
    """
    code = 400
    error_code = "AUTH__BAD_UUID"
    message = "submitted value is not a uuid"
