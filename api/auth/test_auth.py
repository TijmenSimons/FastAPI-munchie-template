import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_refresh(
    client: AsyncClient,
):
    login_data = {
        "username": "normal_user",
        "password": "normal_user",
    }
    res = await client.post("/api/v1/auth/login", json=login_data)

    assert res.status_code == 200

    first_token = res.json().get("refresh_token")

    res = await client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": first_token},
    )

    assert res.status_code == 200

    second_token = res.json().get("refresh_token")
    assert second_token is not first_token

    res = await client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": second_token},
    )

    assert res.status_code == 200

    third_token = res.json().get("refresh_token")
    assert third_token is not second_token

    res = await client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": first_token},
    )

    assert res.status_code == 401


@pytest.mark.asyncio
async def test_verify(
    client: AsyncClient,
):
    login_data = {
        "username": "normal_user",
        "password": "normal_user",
    }
    res = await client.post("/api/v1/auth/login", json=login_data)

    assert res.status_code == 200

    response = res.json()

    res = await client.post(
        "/api/v1/auth/verify", json={"token": response.get("access_token")}
    )
    assert res.status_code == 200

    res = await client.post(
        "/api/v1/auth/verify", json={"token": response.get("refresh_token")}
    )
    assert res.status_code == 200

    res = await client.post("/api/v1/auth/verify", json={"token": "VeryFakeToken!"})
    assert res.status_code == 400


@pytest.mark.asyncio
async def test_user_not_found_login(client: AsyncClient):
    login_data = {
        "username": "no_user",
        "password": "no_user",
    }
    res = await client.post("/api/v1/auth/login", json=login_data)

    assert res.status_code == 404


@pytest.mark.asyncio
async def test_incorrect_password(client: AsyncClient):
    login_data = {
        "username": "normal_user",
        "password": "incorrect_password",
    }
    res = await client.post("/api/v1/auth/login", json=login_data)

    assert res.status_code == 403


@pytest.mark.asyncio
async def test_fake_tokens(client: AsyncClient):
    no_jti_bad = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoibEpyN1ZlejZHUXk0\
        WjJYRSIsInN1YiI6InJlZnJlc2giLCJleHAiOjE2OTEwOTU2NTN9.gOERoZeG0kreJ4D7zbNfILeWHN\
        PYJ3iUXK6QLIw8xqw"
    no_jti_real = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoibEpyN1ZlejZHUXk\
        0WjJYRSIsInN1YiI6InJlZnJlc2giLCJleHAiOjE2OTEwOTk1Nzl9.RuXUyeEBO7uA0bB22-_0cG2TY\
        80gE5AgrihAkDAPzss"
    no_refresh = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoibEpyN1ZlejZHUXk0\
        WjJYRSIsInN1YiI6InJlZnJvc2giLCJqdGkiOiIzZGFjNThhNGUxNTEzYjE2YmNiMWZmYzllOGM3NTg\
        iLCJleHAiOjE2OTExMDEwMzN9._Y3dO6t50ts8srzrcse_UCZBk0TjChaTo1WxW4vceJY"
    expired = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoibEpyN1ZlejZHUXk0WjJ\
        YRSIsInN1YiI6InJlZnJlc2giLCJqdGkiOiIzMjBiNGVlYjE5M2QyMzZlZGYxODg2NmNiODQ5M2YiLC\
        JleHAiOjE2OTAxMDEwODN9.zNmJXxuPFcc5t695eZUh-23TZqQuNCQ2TaFSffSCAbk"

    res = await client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": no_jti_bad},
    )
    assert res.status_code == 400

    res = await client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": no_jti_real},
    )
    assert res.status_code == 400

    res = await client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": no_refresh},
    )
    assert res.status_code == 400

    res = await client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": expired},
    )
    assert res.status_code == 400
