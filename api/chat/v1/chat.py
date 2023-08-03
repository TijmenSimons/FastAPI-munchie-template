"""Chat enpoints."""

from fastapi import APIRouter, WebSocket
from app.chat.services.chat_websocket import ChatWebsocketService

chat_v1_router = APIRouter()


@chat_v1_router.websocket("/{pool_id}/{username}")
async def websocket_endpoint(
    websocket: WebSocket,
    pool_id: str,
    username: str,
):
    """Chat WebSocket endpoint to connect to."""
    await ChatWebsocketService().handler(websocket, pool_id, username)
