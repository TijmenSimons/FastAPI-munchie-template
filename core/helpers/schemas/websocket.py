from typing import Any
from pydantic import BaseModel

from core.db.enums import ChatWebsocketActionEnum, WebsocketActionEnum


class WebsocketPacketSchema(BaseModel):
    action: WebsocketActionEnum
    payload: Any | None = None


class ChatWebsocketPacketSchema(BaseModel):
    action: ChatWebsocketActionEnum
    payload: Any | None = None

