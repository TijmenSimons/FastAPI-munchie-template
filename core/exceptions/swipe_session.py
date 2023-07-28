from core.exceptions import CustomException


class SwipeSessionNotFoundException(CustomException):
    code = 404
    error_code = "SWIPE_SESSION__NOT_FOUND"
    message = "swipe session was not found"