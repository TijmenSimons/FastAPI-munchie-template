from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from app.group.schemas.group import GroupSchema
from app.group.services.group import GroupService
from app.user.schemas.user import UpdateMeSchema, UpdateUserSchema, UserSchema
from app.filter.schemas.filter import FilterSchema, UserCreateSchema
from app.filter.services.filter import FilterService
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
    return user


@me_v1_router.patch(
    "",
    response_model=UserSchema,
    responses={"400": {"model": ExceptionResponseSchema}},
    dependencies=[Depends(PermissionDependency([[IsAuthenticated]]))],
)
@version(1)
async def update_me(request: UpdateMeSchema, user=Depends(get_current_user)):
    user_req = UpdateUserSchema(id=user.id, **request.dict())
    return await UserService().update(user_req)


@me_v1_router.delete(
    "",
    status_code=204,
    dependencies=[Depends(PermissionDependency([[IsAuthenticated]]))],
)
@version(1)
async def delete_me(user=Depends(get_current_user)):
    return await UserService().delete_user(user.id)


@me_v1_router.get(
    "/groups",
    response_model=list[GroupSchema],
    dependencies=[Depends(PermissionDependency([[IsAuthenticated]]))],
)
@version(1)
async def get_user_groups(user: int = Depends(get_current_user)):
    return await GroupService().get_groups_by_user(user.id)


@me_v1_router.get(
    "/filters",
    response_model=list[FilterSchema],
    dependencies=[Depends(PermissionDependency([[IsAuthenticated]]))],
)
@version(1)
async def get_user_filters(user: int = Depends(get_current_user)):
    return await FilterService().get_all_filters_user(user.id)


@me_v1_router.post(
    "/filters", dependencies=[Depends(PermissionDependency([[IsAuthenticated]]))]
)
@version(1)
async def create_user_filter(
    user_filter: UserCreateSchema, user: int = Depends(get_current_user)
):
    await FilterService().store_filters(user.id, user_filter.tags)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"message": "Filter created successfully."},
    )


@me_v1_router.delete(
    "/filters/{filter_id}",
    responses={"400": {"model": ExceptionResponseSchema}},
    dependencies=[Depends(PermissionDependency([[IsAuthenticated]]))],
)
@version(1)
async def delete_user_filter(filter_id: int, user: int = Depends(get_current_user)):
    await FilterService().delete_filter(user.id, filter_id)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": "Filter deleted successfully."},
    )
