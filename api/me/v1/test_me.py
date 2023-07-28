# pylint: skip-file

import pytest
from httpx import AsyncClient
from typing import Dict


@pytest.mark.asyncio
async def test_me(
    normal_user_token_headers: Dict[str, str],
    client: AsyncClient,
):
    res = await client.get("/api/v1/me", headers=await normal_user_token_headers)

    assert res.status_code == 200


@pytest.mark.asyncio
async def test_me_groups(
    normal_user_token_headers: Dict[str, str],
    client: AsyncClient,
):
    res = await client.get("/api/v1/me/groups", headers=await normal_user_token_headers)

    assert res.status_code == 200


@pytest.mark.asyncio
async def test_add_filters(
    normal_user_token_headers: Dict[str, str],
    client: AsyncClient,
):
    res = await client.post(
        "/api/v1/me/filters",
        json={"tags": [3]},
        headers=await normal_user_token_headers,
    )

    assert res.status_code == 201

@pytest.mark.asyncio
async def test_me_filters(
    normal_user_token_headers: Dict[str, str],
    client: AsyncClient,
):
    res = await client.get("/api/v1/me/filters", headers=await normal_user_token_headers)
    assert len(res.json()) == 1
    assert res.status_code == 200


@pytest.mark.asyncio
async def test_me_filters_delete(
    normal_user_token_headers: Dict[str, str],
    client: AsyncClient,
):
    normal_user_token_headers  = await normal_user_token_headers
    res = await client.delete(
        f"/api/v1/me/filters/{3}",
        headers=normal_user_token_headers,
    )
    res = await client.get("/api/v1/me/filters", headers=normal_user_token_headers)
    assert len(res.json()) == 0