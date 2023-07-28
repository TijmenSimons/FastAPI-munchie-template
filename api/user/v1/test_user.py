# pylint: skip-file

from typing import Dict
import pytest
from httpx import AsyncClient
from fastapi import Response
from fastapi.testclient import TestClient


@pytest.mark.asyncio
async def test_create_user(client: AsyncClient):
    response: Response = await client.post(
        "/api/v1/users",
        json={"username": "user3", "password": "user3"},
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_update_user(
    client: AsyncClient,
    admin_token_headers: Dict[str, str],
    normal_user_token_headers: Dict[str, str],
):
    admin_headers = await admin_token_headers
    normal_user_headers = await normal_user_token_headers

    res = await client.get("/api/v1/users", headers=admin_headers)
    users = res.json()

    response: Response = await client.patch(
        f"/api/v1/users/{users[1].get('id')}",
        json={"id": users[1].get("id"), "display_name": "mr. user"},
        headers=normal_user_headers,
    )
    assert response.status_code == 200
    assert response.json().get("display_name") == "mr. user"

    response: Response = await client.patch(
        f"/api/v1/users/{users[1].get('id')}",
        json={"id": users[1].get("id"), "display_name": users[1].get("display_name")},
        headers=admin_headers,
    )
    assert response.status_code == 200
    assert response.json().get("display_name") == users[1].get("display_name")


@pytest.mark.asyncio
async def test_create_existing_user(client: AsyncClient):
    response: Response = await client.post(
        "/api/v1/users",
        json={"username": "admin", "password": "admin"},
    )
    assert response.status_code == 409


@pytest.mark.asyncio
async def test_get_user_list(client: AsyncClient, admin_token_headers: Dict[str, str]):
    res = await client.get("/api/v1/users", headers=await admin_token_headers)
    users = res.json()

    assert users[0]["display_name"] == "admin"
    assert users[1]["display_name"] == "normal_user"
    assert res.status_code == 200


@pytest.mark.asyncio
async def test_get_user_list_normal_user(
    client: AsyncClient, normal_user_token_headers: Dict[str, str]
):
    res = await client.get("/api/v1/users", headers=await normal_user_token_headers)
    assert res.status_code == 401


@pytest.mark.asyncio
async def test_get_user_list_no_auth(client: AsyncClient):
    res = await client.get("/api/v1/users")
    assert res.status_code == 401


@pytest.mark.asyncio
async def test_get_user_groups(
    normal_user_token_headers: Dict[str, str],
    admin_token_headers: Dict[str, str],
    fastapi_client: TestClient,
):
    admin_headers = await admin_token_headers
    normal_headers = await normal_user_token_headers

    res = fastapi_client.get("/api/v1/users", headers=admin_headers)
    users = res.json()

    res = fastapi_client.get(
        f"/api/v1/users/{users[0].get('id')}/groups", headers=admin_headers
    )
    assert res.status_code == 200

    res = fastapi_client.get(
        f"/api/v1/users/{users[0].get('id')}/groups", headers=normal_headers
    )
    assert res.status_code == 401

    res = fastapi_client.get(
        f"/api/v1/users/{users[1].get('id')}/groups", headers=admin_headers
    )
    assert res.status_code == 200

    res = fastapi_client.get(
        f"/api/v1/users/{users[1].get('id')}/groups", headers=normal_headers
    )
    assert res.status_code == 200
