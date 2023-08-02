import pytest
from httpx import AsyncClient

from core.exceptions.base import CustomException


@pytest.mark.asyncio
async def test_refresh(
    client: AsyncClient,
):
    res = await client.get("/api/v1/health")

    assert res.status_code == 200

@pytest.mark.asyncio
async def test_other():
    exception = CustomException(message="message")
    str(exception)
