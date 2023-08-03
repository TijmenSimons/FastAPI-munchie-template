"""
Chat implementation using websockets.
"""

from typing import Any, Coroutine
from fastapi import WebSocket
from core.db.enums import ChatWebsocketActionEnum as ChatEnum
from core.exceptions.websocket import NoMessageException
from core.helpers.schemas.websocket import ChatWebsocketPacketSchema
from core.helpers.websocket.base import BaseWebsocketService
from core.helpers.websocket.manager import WebsocketConnectionManager


manager = WebsocketConnectionManager()


class ChatWebsocketService(BaseWebsocketService):
    """WebsocketService for SwipeSessions

    Attributes:
        - manager (WebsocketConnectionManager): Manage connections.
        - actions (dict): Contains a map of actions.

    Methods:
        - __init__(): Initialize the service.

        - handler(websocket: WebSocket, swipe_session_id: int, access_token: str): Start
        the handler.

        - handle_pool_user_message(pool_id: str, packet: SwipeSessionPacketSchema, 
        websocket: WebSocket, username: str): Broadcast a message to all participants 
        of a pool as a user.
    """

    def __init__(self) -> None:
        """Initialize the service."""
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
        """Initialize the handler with authentication.

        Args:
            websocket (WebSocket): The Websocket connection.
            pool_id (str): Pool identifier.
            username (str): User's username to represent themselves.

        Returns:
            Coroutine[Any, Any, None]: The handler loop.
        """
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
        """Broadcast a message to all participants of a pool as a user.

        Args:
            pool_id (int): Identifier for the pool to send the message to.
            packet (SwipeSessionPacketSchema): WebsocketPacket sent by client.
            websocket (WebSocket): The websocket connection.
            username (str): The username representing the sender of the message.

        Returns:
            None.
        """
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
