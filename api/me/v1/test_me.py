import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_me(
    normal_user_token_headers: dict[str, str],
    client: AsyncClient,
):
    res = await client.get("/api/v1/me", headers=await normal_user_token_headers)

    assert res.status_code == 200


@pytest.mark.asyncio
async def test_me_no_auth(
    client: AsyncClient,
):
    res = await client.get("/api/v1/me")

    assert res.status_code == 401


@pytest.mark.asyncio
async def test_update_me(
    normal_user_token_headers: dict[str, str],
    client: AsyncClient,
):
    user_headers = await normal_user_token_headers
    res = await client.patch(
        "/api/v1/me",
        headers=user_headers,
        json={
            "display_name": "normie",
            "username": "normie",
        },
    )

    assert res.status_code == 200
    assert res.json().get("display_name") == "normie"
    assert res.json().get("username") == "normie"

    res = await client.patch(
        "/api/v1/me",
        headers=user_headers,
        json={
            "display_name": "normal_user",
            "username": "normal_user",
        },
    )

    assert res.status_code == 200
    assert res.json().get("display_name") == "normal_user"
    assert res.json().get("username") == "normal_user"


@pytest.mark.asyncio
async def test_delete_me(
    client: AsyncClient,
    admin_token_headers: dict[str, str], 
):
    user_data = {
        "display_name": "delete_user",
        "username": "delete_user",
        "password": "delete_user",
    }

    res = await client.post("/api/v1/users", json=user_data)

    assert res.status_code == 200

    res = await client.post("/api/v1/auth/login", json=user_data)

    assert res.status_code == 200
    user_headers = {"Authorization": f"Bearer {res.json().get('access_token')}"}

    res = await client.delete("/api/v1/me", headers=user_headers)

    assert res.status_code == 204

    res = await client.get("/api/v1/users", headers=await admin_token_headers)

    assert not any(user.get("username") == "delete_user" for user in res.json())
