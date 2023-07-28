from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from app.group.schemas.group import GroupSchema
from app.group.services.group import GroupService
from app.filter.services.filter import FilterService
from app.filter.schemas.filter import FilterSchema, UserCreateSchema
from app.user.schemas.user import UpdateMeSchema, UpdateUserSchema
from core.exceptions import ExceptionResponseSchema
from core.fastapi.dependencies.hashid import get_path_user_id
from core.fastapi.dependencies.permission import IsAuthenticated, IsUserOwner
from core.fastapi_versioning.versioning import version

from app.user.schemas import (
    UserSchema,
    CreateUserRequestSchema,
)
from app.user.services import UserService
from core.fastapi.dependencies import (
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
async def create_user(request: CreateUserRequestSchema):
    """Create new user with account auth"""
    user_id = await UserService().create_auth_user(**request.dict())
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
    request: UpdateMeSchema, user_id: str = Depends(get_path_user_id)
):
    user_req = UpdateUserSchema(id=user_id, **request.dict())
    return await UserService().update(user_req)


@user_v1_router.delete(
    "/{user_id}",
    status_code=204,
    dependencies=[
        Depends(PermissionDependency([[IsAdmin], [IsAuthenticated, IsUserOwner]]))
    ],
)
@version(1)
async def delete_me(user_id=Depends(get_path_user_id)):
    return await UserService().delete_user(user_id)


@user_v1_router.get(
    "/{user_id}/groups",
    response_model=list[GroupSchema],
    dependencies=[
        Depends(PermissionDependency([[IsAdmin], [IsAuthenticated, IsUserOwner]]))
    ],
)
@version(1)
async def get_user_groups(user_id: int = Depends(get_path_user_id)):
    return await GroupService().get_groups_by_user(user_id)


@user_v1_router.get(
    "/{user_id}/filters",
    response_model=list[FilterSchema],
    dependencies=[Depends(PermissionDependency([[IsAdmin]]))],
)
@version(1)
async def get_user_filters(user_id: int = Depends(get_path_user_id)):
    return await FilterService().get_all_filters_user(user_id)


@user_v1_router.post(
    "/{user_id}/filters", dependencies=[Depends(PermissionDependency([[IsAdmin]]))]
)
@version(1)
async def create_user_filter(
    user_filter: UserCreateSchema, user_id: int = Depends(get_path_user_id)
):
    await FilterService().store_filters(user_id, user_filter.tags)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"message": "Filter created successfully."},
    )


@user_v1_router.delete(
    "/{user_id}/filters",
    responses={"400": {"model": ExceptionResponseSchema}},
    dependencies=[Depends(PermissionDependency([[IsAdmin]]))],
)
@version(1)
async def delete_user_filter(id: int, user_id: int = Depends(get_path_user_id)):
    await FilterService().delete_filter(user_id, id)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": "Filter deleted successfully."},
    )
