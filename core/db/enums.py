from enum import Enum


class BaseEnum(Enum):
    """Base enum"""
    pass


class WebsocketActionEnum(str, BaseEnum):
    """Define the websocket actions."""

    CONNECTION_CODE = "CONNECTION_CODE"
    POOL_MESSAGE = "POOL_MESSAGE"
    GLOBAL_MESSAGE = "GLOBAL_MESSAGE"


class ChatWebsocketActionEnum(str, BaseEnum):
    """Define the chat websocket actions."""

    CONNECTION_CODE = "CONNECTION_CODE"
    POOL_MESSAGE = "POOL_MESSAGE"
    GLOBAL_MESSAGE = "GLOBAL_MESSAGE"
    POOL_USER_MESSAGE = "POOL_USER_MESSAGE"
