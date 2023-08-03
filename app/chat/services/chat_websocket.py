from typing import Any, Coroutine
from fastapi import WebSocket
from core.db.enums import ChatWebsocketActionEnum as ChatEnum
from core.exceptions.websocket import NoMessageException
from core.helpers.schemas.websocket import ChatWebsocketPacketSchema
from core.helpers.websocket.base import BaseWebsocketService
from core.helpers.websocket.manager import WebsocketConnectionManager


manager = WebsocketConnectionManager()


class ChatWebsocketService(BaseWebsocketService):
    def __init__(self) -> None:
        actions = {
            ChatEnum.POOL_MESSAGE.value: self.handle_pool_message,
            ChatEnum.GLOBAL_MESSAGE.value: self.handle_global_message,
            ChatEnum.POOL_USER_MESSAGE.value: self.handle_pool_user_message,
        }

        super().__init__(
            manager=manager, schema=ChatWebsocketPacketSchema, actions=actions
        )

    async def handler(
        self,
        websocket: WebSocket,
        pool_id: int,
        username: str,
    ) -> Coroutine[Any, Any, None]:
        exc = await self.manager.check_auth()
        if exc:
            await self.manager.deny(websocket, exc)
            return

        return await super().handler(
            websocket=websocket,
            pool_id=pool_id,
            username=username,
        )

    async def handle_pool_user_message(
        self,
        pool_id: int,
        packet: ChatWebsocketPacketSchema,
        websocket: WebSocket,
        username: str,
        **kwargs
    ):
        del kwargs

        message = packet.payload.get("message")

        if not message:
            await self.manager.handle_connection_code(websocket, NoMessageException)
            return

        message_packet = ChatWebsocketPacketSchema(
            action=ChatEnum.POOL_USER_MESSAGE,
            payload={"username": username, "message": message},
        )

        await self.manager.pool_packet(pool_id, message_packet)
