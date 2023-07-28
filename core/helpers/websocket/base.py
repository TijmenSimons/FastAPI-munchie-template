"""Module containing the base websocket service for other variations to extend upon.
"""

import logging
from fastapi import WebSocket, WebSocketDisconnect, WebSocketException
from starlette.websockets import WebSocketState
from core.db.enums import WebsocketActionEnum
from core.exceptions.base import CustomException
from core.exceptions.websocket import (
    ActionNotImplementedException,
    SuccessfullConnection,
)
from core.helpers.logger import get_logger
from core.helpers.schemas.websocket import WebsocketPacketSchema
from core.helpers.websocket.manager import WebsocketConnectionManager
from pydantic.main import ModelMetaclass


class BaseWebsocketService:
    def __init__(
        self,
        manager: WebsocketConnectionManager,
        schema: ModelMetaclass = WebsocketPacketSchema,
        actions: dict = None,
    ) -> None:
        self.manager = manager
        self.schema = schema

        if not actions:
            self.actions = {
                WebsocketActionEnum.POOL_MESSAGE.value: self.handle_pool_message,
                WebsocketActionEnum.GLOBAL_MESSAGE.value: self.handle_global_message,
            }
        else:
            self.actions = actions

    async def handler(self, websocket: WebSocket, pool_id: int, **kwargs) -> None:
        """The handler for the Websocket protocol.

        Args:
            websocket (WebSocket): The websocket connection.
            pool_id (int): The identifiër for which pool the websocket will be
            connected to.
            kwargs: Any extra arguments which will be passed to the functions ran by
            the handler.
        """
        await self.manager.connect(websocket, pool_id)
        await self.manager.handle_connection_code(websocket, SuccessfullConnection)

        try:
            while (
                websocket.application_state == WebSocketState.CONNECTED
                and websocket.client_state == WebSocketState.CONNECTED
            ):
                try:
                    packet: self.schema = await self.manager.receive_data(
                        websocket, self.schema
                    )

                except CustomException as exc:
                    await self.manager.handle_connection_code(websocket, exc)

                else:
                    func = self.actions.get(
                        packet.action.value, self.handle_action_not_implemented
                    )

                    await self.manager.queued_run(
                        pool_id=pool_id,
                        func=func,
                        packet=packet,
                        websocket=websocket,
                        **kwargs
                    )

        except WebSocketDisconnect:
            # Check because sometimes the exception is raised
            # but it's already disconnected
            if websocket.client_state == WebSocketState.CONNECTED:
                await self.manager.disconnect(websocket, pool_id)

            elif websocket.application_state == WebSocketState.CONNECTED:
                self.manager.remove_websocket(websocket, pool_id)

        except WebSocketException as exc:
            get_logger(exc)
            logging.info(self.active_pools)
            logging.info(f"pool_id {pool_id}, func: {func.__name__}")
            logging.info(self.active_pools.get(pool_id))
            logging.exception(exc)
            print(exc)

    async def handle_action_not_implemented(self, websocket: WebSocket, **kwargs):
        """Handle an action packet that has not been implemented.

        Args:
            websocket (WebSocket): The websocket connection.

        Returns:
            None.
        """
        del kwargs

        await self.manager.handle_connection_code(
            websocket, ActionNotImplementedException
        )

    async def handle_global_message(
        self, packet: WebsocketPacketSchema, websocket: WebSocket, **kwargs
    ):
        """Handle a global message sent by an admin user to all participants of a
        swipe session.

        Args:
            packet (SwipeSessionPacketSchema): WebsocketPacket sent by client.
            websocket (WebSocket): The websocket connection.

        Returns:
            None.
        """
        del kwargs

        await self.manager.handle_global_message(
            websocket, packet.payload.get("message")
        )

    async def handle_pool_message(
        self,
        pool_id: int,
        packet: WebsocketPacketSchema,
        websocket: WebSocket,
        **kwargs
    ):
        """Handle a message sent by a participant of a pool to the entire pool.

        Args:
            pool_id (int): Identifier for the pool to send the message to.
            packet (SwipeSessionPacketSchema): WebsocketPacket sent by client.
            websocket (WebSocket): The websocket connection.

        Returns:
            None.
        """
        del kwargs

        await self.manager.handle_pool_message(
            websocket, pool_id, packet.payload.get("message")
        )
