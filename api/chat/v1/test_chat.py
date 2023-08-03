from fastapi.testclient import TestClient
from starlette.testclient import WebSocketTestSession
from core.db.enums import ChatWebsocketActionEnum as ChatEnum
import pytest

import core.exceptions.websocket as exc


def assert_status_code(data, exception):
    assert data.get("action") == ChatEnum.CONNECTION_CODE

    payload = data.get("payload")
    assert payload is not None

    assert payload.get("status_code") == exception.code
    assert payload.get("message") == exception.message


def send_message(ws: WebSocketTestSession, message: str):
    packet = {"action": ChatEnum.POOL_USER_MESSAGE, "payload": {"message": message}}
    ws.send_json(packet)

@pytest.mark.asyncio
async def test_websocket(fastapi_client: TestClient):
    with fastapi_client.websocket_connect("/api/v1/chat/pool/ws_1") as ws_1:
        ws_1: WebSocketTestSession

        data_1 = ws_1.receive_json()
        assert_status_code(data_1, exc.SuccessfullConnection)
        
        packet = {"action": "NonExist", "payload": {}}
        ws_1.send_json(packet)

        data_1 = ws_1.receive_json()
        assert_status_code(data_1, exc.ActionNotFoundException)
        
        ws_1.send_text("well this is not json")

        data_1 = ws_1.receive_json()
        assert_status_code(data_1, exc.JSONSerializableException)


@pytest.mark.asyncio
async def test_chat(fastapi_client: TestClient):
    with (fastapi_client.websocket_connect("/api/v1/chat/pool/ws_1") as ws_1, 
          fastapi_client.websocket_connect("/api/v1/chat/pool/ws_2") as ws_2):
        ws_1: WebSocketTestSession
        ws_2: WebSocketTestSession

        data_1 = ws_1.receive_json()
        data_2 = ws_2.receive_json()

        assert_status_code(data_1, exc.SuccessfullConnection)
        assert_status_code(data_2, exc.SuccessfullConnection)

        send_message(ws_1, "Hello!")

        data_1 = ws_1.receive_json()
        data_2 = ws_2.receive_json()

        assert data_1.get("action") == ChatEnum.POOL_USER_MESSAGE
        assert data_1.get("payload").get("username") == "ws_1"
        assert data_1.get("payload").get("message") == "Hello!"

        assert data_2.get("action") == ChatEnum.POOL_USER_MESSAGE
        assert data_2.get("payload").get("username") == "ws_1"
        assert data_2.get("payload").get("message") == "Hello!"

        packet = {"action": ChatEnum.GLOBAL_MESSAGE, "payload": {}}
        ws_1.send_json(packet)

        data_1 = ws_1.receive_json()

        assert_status_code(data_1, exc.NoMessageException)

        packet = {"action": ChatEnum.GLOBAL_MESSAGE, "payload": {"message": "GLOBAL"}}
        ws_1.send_json(packet)

        data_1 = ws_1.receive_json()
        data_2 = ws_2.receive_json()

        assert data_1.get("action") == ChatEnum.GLOBAL_MESSAGE
        assert data_1.get("payload").get("message") == "GLOBAL"

        assert data_2.get("action") == ChatEnum.GLOBAL_MESSAGE
        assert data_2.get("payload").get("message") == "GLOBAL"

        packet = {"action": ChatEnum.POOL_MESSAGE, "payload": {}}
        ws_1.send_json(packet)

        data_1 = ws_1.receive_json()

        assert_status_code(data_1, exc.NoMessageException)

        packet = {"action": ChatEnum.POOL_MESSAGE, "payload": {"message": "POOL"}}
        ws_1.send_json(packet)

        data_1 = ws_1.receive_json()
        data_2 = ws_2.receive_json()

        assert data_1.get("action") == ChatEnum.POOL_MESSAGE
        assert data_1.get("payload").get("message") == "POOL"

        assert data_2.get("action") == ChatEnum.POOL_MESSAGE
        assert data_2.get("payload").get("message") == "POOL"

        packet = {"action": ChatEnum.POOL_USER_MESSAGE, "payload": {}}
        ws_1.send_json(packet)

        data_1 = ws_1.receive_json()

        assert_status_code(data_1, exc.NoMessageException)


