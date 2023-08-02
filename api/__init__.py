from fastapi import APIRouter

from api.user.v1.user import user_v1_router
from api.auth.v1.auth import auth_v1_router
from api.me.v1.me import me_v1_router

router = APIRouter()
router.include_router(me_v1_router, prefix="/me", tags=["Me"])
router.include_router(user_v1_router, prefix="/users", tags=["User"])
router.include_router(auth_v1_router, prefix="/auth", tags=["Auth"])


__all__ = ["router"]
