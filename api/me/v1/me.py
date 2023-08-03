"""Me endpoints."""

from fastapi import APIRouter, Depends
from app.user.schemas.user import UpdateUserSchema, UserSchema
from app.user.services.user import UserService
from core.exceptions import ExceptionResponseSchema
from core.fastapi.dependencies.permission import IsAuthenticated, PermissionDependency
from core.fastapi.dependencies.user import get_current_user
from core.fastapi_versioning.versioning import version


me_v1_router = APIRouter()


@me_v1_router.get(
    "",
    response_model=UserSchema,
    dependencies=[Depends(PermissionDependency([[IsAuthenticated]]))],
)
@version(1)
async def get_me(user=Depends(get_current_user)):
    """Retrieve your own account info."""
    return user


@me_v1_router.patch(
    "",
    response_model=UserSchema,
    responses={"400": {"model": ExceptionResponseSchema}},
    dependencies=[Depends(PermissionDependency([[IsAuthenticated]]))],
)
@version(1)
async def update_me(request: UpdateUserSchema, user=Depends(get_current_user)):
    """Update your own account."""
    return await UserService().update(user.id, request)


@me_v1_router.delete(
    "",
    status_code=204,
    dependencies=[Depends(PermissionDependency([[IsAuthenticated]]))],
)
@version(1)
async def delete_me(user=Depends(get_current_user)):
    """Delete your own account."""
    return await UserService().delete_user(user.id)
