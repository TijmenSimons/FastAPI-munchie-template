from core.exceptions import CustomException


class PasswordDoesNotMatchException(CustomException):
    code = 401
    error_code = "USER__PASSWORD_DOES_NOT_MATCH"
    message = "password does not match"


class MissingUserIDException(CustomException):
    code = 401
    error_code = "USER__NO_ID"
    message = "no id was provided, or was not logged in"


class MissingGroupIDException(CustomException):
    code = 401
    error_code = "GROUP__NO_ID"
    message = "no group id was provided"


class IncorrectPasswordException(CustomException):
    code = 403
    error_code = "USER__INCORRECT_PASSWORD"
    message = "password is incorrect"


class UserNotFoundException(CustomException):
    code = 404
    error_code = "USER__NOT_FOUND"
    message = "user not found"


class DuplicateUsernameException(CustomException):
    code = 409
    error_code = "USER__DUPLICATE_USERNAME"
    message = "duplicate username"


class DuplicateClientTokenException(CustomException):
    code = 409
    error_code = "USER__DUPLICATE_CLIENT_TOKEN"
    message = "duplicate client token"
