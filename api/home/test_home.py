import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_refresh(
    client: AsyncClient,
):
    res = await client.get("/api/v1/health")

    assert res.status_code == 200