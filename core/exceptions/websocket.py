from core.exceptions import CustomException


class ConnectionCode:
    code = 200
    message = "connection code"

    def __init__(self, code, message) -> None:
        self.code = code
        self.message = message


class SuccessfullConnection(ConnectionCode):
    code = 202
    message = "you have connected"


class ClosingConnection(ConnectionCode):
    code = 200
    message = "you have been forcefully disconnected"


class InactiveException(CustomException):
    code = 400
    error_code = "WEBSOCKET__INACTIVE_SESSION"
    message = "you cannot connect to an inactive session"


class NoMessageException(CustomException):
    code = 400
    error_code = "WEBSOCKET__NO_MESSAGE"
    message = "no message provided"


class JSONSerializableException(CustomException):
    code = 400
    error_code = "WEBSOCKET__JSON_UNSERIALIZABLE"
    message = "data is not JSON serializable"


class ValidationException(CustomException):
    code = 400
    error_code = "WEBSOCKET__VALIDATION_ERROR"
    message = "pydantic schema validation failed"


class InvalidIdException(CustomException):
    code = 400
    error_code = "WEBSOCKET__INVALID_ID"
    message = "either session or user id is invalid"


class AccessDeniedException(CustomException):
    code = 403
    error_code = "WEBSOCKET__ACCESS_DENIED"
    message = "access denied"


class StatusNotFoundException(CustomException):
    code = 404
    error_code = "WEBSOCKET__STATUS_NOT_FOUND"
    message = "status does not exist"


class ActionNotFoundException(CustomException):
    code = 404
    error_code = "WEBSOCKET__ACTION_NOT_FOUND"
    message = "action does not exist"


class AlreadySwipedException(CustomException):
    code = 409
    error_code = "WEBSOCKET__SWIPE_CONFLICT"
    message = "this user has already swiped this recipe in this session"


class ActionNotImplementedException(CustomException):
    code = 501
    error_code = "WEBSOCKET__ACTION_NOT_IMPLEMENTED"
    message = "action is not implemented or not available"
