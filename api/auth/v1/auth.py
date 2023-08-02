from fastapi import APIRouter, Depends
from core.exceptions import ExceptionResponseSchema
from core.fastapi.dependencies.permission import AllowAll, PermissionDependency
from core.fastapi_versioning import version

from core.fastapi.schemas.token import (
    RefreshTokenRequest,
    VerifyTokenRequest,
    TokensSchema,
    LoginRequest,
)
from app.auth.services.auth import AuthService

auth_v1_router = APIRouter()


@auth_v1_router.post(
    "/refresh",
    response_model=TokensSchema,
    responses={"400": {"model": ExceptionResponseSchema}},
    dependencies=[Depends(PermissionDependency([[AllowAll]]))],
)
@version(1)
async def refresh_token(request: RefreshTokenRequest):
    return await AuthService().refresh_tokens(request.refresh_token)


@auth_v1_router.post(
    "/verify", dependencies=[Depends(PermissionDependency([[AllowAll]]))]
)
@version(1)
async def verify_token(request: VerifyTokenRequest):
    """
    Verifies token.

    Returns
        200: Token is valid.
        400: Token is invalid (expired or other).
        500: Something went wrong.
    """
    return await AuthService().verify_token(request.token)


@auth_v1_router.post(
    "/login",
    response_model=TokensSchema,
    responses={"404": {"model": ExceptionResponseSchema}},
    dependencies=[Depends(PermissionDependency([[AllowAll]]))],
)
@version(1)
async def login(request: LoginRequest):
    token = await AuthService().login(
        username=request.username, password=request.password
    )
    return {"access_token": token.access_token, "refresh_token": token.refresh_token}
