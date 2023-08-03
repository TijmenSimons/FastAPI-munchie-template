"""Unit tests for the base endpoints."""

import pytest
from httpx import AsyncClient

from core.exceptions.base import CustomException


@pytest.mark.asyncio
async def test_health(
    client: AsyncClient,
):
    """Test the health endpoints"""
    res = await client.get("/api/v1/health")

    assert res.status_code == 200

@pytest.mark.asyncio
async def test_other():
    """Test the custom exception"""
    exception = CustomException(message="message")
    str(exception)
