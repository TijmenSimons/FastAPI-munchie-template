from fastapi import APIRouter, Response, Depends

from core.fastapi.dependencies.permission import PermissionDependency, AllowAll, IsAdmin
from app.swipe_session.services.swipe_session_websocket import manager

home_router = APIRouter()


@home_router.get("/health", dependencies=[Depends(PermissionDependency([[AllowAll]]))])
async def home():
    return Response(status_code=200)


@home_router.get("/cheat", dependencies=[Depends(PermissionDependency([[IsAdmin]]))])
async def cheat():
    result = {}

    for key, item in manager.active_pools.items():
        item["connections"] = ["WebSocket" for _ in item["connections"]]
        result[key] = item

    return result
