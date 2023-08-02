from typing import List

from fastapi import APIRouter, Depends
from app.user.schemas.user import SetAdminSchema, UpdateUserSchema
from core.exceptions import ExceptionResponseSchema
from core.fastapi.dependencies.hashid import get_path_user_id
from core.fastapi.dependencies.permission import IsAuthenticated, IsUserOwner
from core.fastapi_versioning.versioning import version

from app.user.schemas import (
    UserSchema,
    CreateUserSchema,
)
from app.user.services import UserService
from core.fastapi.dependencies.permission import (
    PermissionDependency,
    IsAdmin,
)

user_v1_router = APIRouter()


@user_v1_router.get(
    "",
    response_model=List[UserSchema],
    responses={"400": {"model": ExceptionResponseSchema}},
    dependencies=[Depends(PermissionDependency([[IsAdmin]]))],
)
@version(1)
async def get_user_list():
    return await UserService().get_user_list()


@user_v1_router.post(
    "",
    response_model=UserSchema,
    responses={"400": {"model": ExceptionResponseSchema}},
)
@version(1)
async def create_user(request: CreateUserSchema):
    user_id = await UserService().create_user(**request.dict())
    return await UserService().get_by_id(user_id)


@user_v1_router.patch(
    "/{user_id}",
    response_model=UserSchema,
    responses={"400": {"model": ExceptionResponseSchema}},
    dependencies=[
        Depends(PermissionDependency([[IsAdmin], [IsAuthenticated, IsUserOwner]]))
    ],
)
@version(1)
async def update_user(
    request: UpdateUserSchema, user_id: str = Depends(get_path_user_id)
):
    return await UserService().update(user_id, request)


@user_v1_router.patch(
    "/{user_id}/admin",
    response_model=UserSchema,
    responses={"400": {"model": ExceptionResponseSchema}},
    dependencies=[
        Depends(PermissionDependency([[IsAdmin]]))
    ],
)
async def set_admin(
    request: SetAdminSchema, user_id: str = Depends(get_path_user_id)
):
    return await UserService().set_admin(user_id, request)


@user_v1_router.delete(
    "/{user_id}",
    status_code=204,
    dependencies=[
        Depends(PermissionDependency([[IsAdmin], [IsAuthenticated, IsUserOwner]]))
    ],
)
@version(1)
async def delete_user(user_id=Depends(get_path_user_id)):
    return await UserService().delete_user(user_id)
