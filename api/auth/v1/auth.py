from fastapi import APIRouter, Depends, Response
from core.exceptions import ExceptionResponseSchema, DecodeTokenException
from core.fastapi.dependencies.permission import AllowAll, PermissionDependency
from core.fastapi_versioning import version

from api.auth.v1.request.auth import RefreshTokenRequest, UUIDSchema, VerifyTokenRequest
from api.auth.v1.response.auth import TokensSchema
from api.auth.v1.request.auth import LoginRequest
from app.auth.services.auth import AuthService
from app.auth.services.jwt import JwtService

auth_v1_router = APIRouter()


@auth_v1_router.post(
    "/refresh",
    response_model=TokensSchema,
    responses={"400": {"model": ExceptionResponseSchema}},
    dependencies=[Depends(PermissionDependency([[AllowAll]]))],
)
@version(1)
async def refresh_token(request: RefreshTokenRequest):
    return await JwtService().refresh_tokens(refresh_token=request.refresh_token)


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
    try:
        await JwtService().verify_token(token=request.token)

    except DecodeTokenException:
        return Response(status_code=400)

    except Exception as exc:
        print(exc)
        return Response(status_code=500)

    return Response(status_code=200)


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


@auth_v1_router.post(
    "/client-token-login",
    response_model=TokensSchema,
    responses={"404": {"model": ExceptionResponseSchema}},
    dependencies=[Depends(PermissionDependency([[AllowAll]]))],
)
@version(1)
async def client_token_login(request: UUIDSchema):
    return await AuthService().client_token_login(ctoken=request.token)
