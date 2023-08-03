"""Base endpoints"""

from fastapi import APIRouter, Response, Depends

from core.fastapi.dependencies.permission import PermissionDependency, AllowAll

home_router = APIRouter()


@home_router.get("/health", dependencies=[Depends(PermissionDependency([[AllowAll]]))])
async def home():
    """Test if the server is healthy."""
    return Response(status_code=200)
