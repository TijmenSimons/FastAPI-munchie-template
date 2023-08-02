# pylint: skip-file

import pytest
from httpx import AsyncClient
from fastapi import Response
from core.helpers.hashid import encode


@pytest.mark.asyncio
async def test_create_user(client: AsyncClient):
    response: Response = await client.post(
        "/api/v1/users",
        json={"display_name": "user3", "username": "user3", "password": "user3"},
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_delete_user(client: AsyncClient, admin_token_headers: dict[str, str]):
    admin_headers = await admin_token_headers

    res = await client.get("/api/v1/users", headers=admin_headers)
    users = res.json()

    users = filter(lambda user: (user.get("username") == "user3"), users)
    user = list(users)[0]

    res = await client.delete(f"/api/v1/users/{user.get('id')}", headers=admin_headers)
    assert res.status_code == 204
    
    res = await client.delete(f"/api/v1/users/{user.get('id')}", headers=admin_headers)
    assert res.status_code == 404


@pytest.mark.asyncio
async def test_update_user(
    client: AsyncClient,
    admin_token_headers: dict[str, str],
    normal_user_token_headers: dict[str, str],
):
    admin_headers = await admin_token_headers
    normal_user_headers = await normal_user_token_headers

    res = await client.get("/api/v1/users", headers=admin_headers)
    users = res.json()

    response: Response = await client.patch(
        f"/api/v1/users/{users[0].get('id')}",
        json={
            "id": users[1].get("id"),
            "display_name": "mr. user",
            "username": users[1].get("username"),
            "password": "normal_user",
        },
        headers=normal_user_headers,
    )
    assert response.status_code == 401

    response: Response = await client.patch(
        f"/api/v1/users/{users[1].get('id')}",
        json={
            "id": users[1].get("id"),
            "display_name": "mr. user",
            "username": users[1].get("username"),
            "password": "normal_user",
        },
        headers=normal_user_headers,
    )
    assert response.status_code == 200
    assert response.json().get("display_name") == "mr. user"

    response: Response = await client.patch(
        f"/api/v1/users/{users[1].get('id')}",
        json={
            "id": users[1].get("id"),
            "display_name": users[1].get("display_name"),
            "username": users[1].get("username"),
            "password": users[1].get("password"),
        },
        headers=admin_headers,
    )
    assert response.status_code == 200
    assert response.json().get("display_name") == users[1].get("display_name")


@pytest.mark.asyncio
async def test_create_existing_user(client: AsyncClient):
    response: Response = await client.post(
        "/api/v1/users",
        json={"display_name": "admin", "username": "admin", "password": "admin"},
    )
    assert response.status_code == 409


@pytest.mark.asyncio
async def test_get_user_list(client: AsyncClient, admin_token_headers: dict[str, str]):
    admin_headers = await admin_token_headers
    res = await client.get("/api/v1/users", headers=admin_headers)
    users = res.json()

    assert users[0]["display_name"] == "admin"
    assert users[1]["display_name"] == "normal_user"
    assert res.status_code == 200

    res = await client.get(f"/api/v1/users/{users[1]['id']}", headers=admin_headers)
    res.status_code == 200

    res = await client.get(f"/api/v1/users/{encode(9000)}", headers=admin_headers)
    res.status_code == 404


@pytest.mark.asyncio
async def test_get_user_list_normal_user(
    client: AsyncClient, normal_user_token_headers: dict[str, str]
):
    res = await client.get("/api/v1/users", headers=await normal_user_token_headers)
    assert res.status_code == 401


@pytest.mark.asyncio
async def test_get_user_list_no_auth(client: AsyncClient):
    res = await client.get("/api/v1/users")
    assert res.status_code == 401


@pytest.mark.asyncio
async def test_set_admin(
    admin_token_headers: dict[str, str],
    client: AsyncClient,
):
    admin_headers = await admin_token_headers

    res = await client.get("/api/v1/users", headers=admin_headers)
    users = res.json()

    normal_user = users[1]

    res = await client.patch(
        f"/api/v1/users/{normal_user.get('id')}/admin",
        headers=admin_headers,
        json={"is_admin": True},
    )

    assert res.status_code == 200
    assert res.json().get("is_admin")

    res = await client.patch(
        f"/api/v1/users/{normal_user.get('id')}/admin",
        headers=admin_headers,
        json={"is_admin": False},
    )

    assert res.status_code == 200
    assert not res.json().get("is_admin")

    res = await client.patch(
        f"/api/v1/users/{encode(9000)}/admin",
        headers=admin_headers,
        json={"is_admin": False},
    )

    assert res.status_code == 404
