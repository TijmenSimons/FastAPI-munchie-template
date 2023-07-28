from core.exceptions import CustomException


class IncorrectHashIDException(CustomException):
    code = 400
    error_code = "HASH__INCORRECT_HASH_ID"
    message = "the inputted hash was incorrect"
