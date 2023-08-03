from enum import Enum


class BaseEnum(Enum):
    pass


class UserEnum(BaseEnum):
    pass


class WebsocketActionEnum(str, BaseEnum):
    CONNECTION_CODE = "CONNECTION_CODE"
    POOL_MESSAGE = "POOL_MESSAGE"
    GLOBAL_MESSAGE = "GLOBAL_MESSAGE"


class ChatWebsocketActionEnum(str, BaseEnum):
    CONNECTION_CODE = "CONNECTION_CODE"
    POOL_MESSAGE = "POOL_MESSAGE"
    GLOBAL_MESSAGE = "GLOBAL_MESSAGE"
    POOL_USER_MESSAGE = "POOL_USER_MESSAGE"
