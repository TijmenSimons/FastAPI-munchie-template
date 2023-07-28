from typing import Any
from pydantic import BaseModel

from core.db.enums import WebsocketActionEnum


class WebsocketPacketSchema(BaseModel):
    action: WebsocketActionEnum
    payload: Any | None = None
