"""
Initialize app
"""


import logging

from fastapi import FastAPI, Depends, Request
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse

from api import router
from api.home.home import home_router

from core.config import config
from core.exceptions import CustomException
from core.fastapi.dependencies import Logging
from core.fastapi.middlewares import (
    AuthenticationMiddleware,
    AuthBackend,
    SQLAlchemyMiddleware,
    ResponseLogMiddleware,
)
from core.fastapi_versioning import VersionedFastAPI
from core.helpers.cache import Cache, RedisBackend, CustomKeyMaker
from core.helpers.logger import get_logger
from core.tasks import start_tasks


def init_routers(app_: FastAPI) -> None:
    """
    Initialize app routers
    """
    app_.include_router(home_router)
    app_.include_router(router)


def init_listeners(app_: FastAPI) -> None:
    """
    Initialize app listeners
    """

    @app_.exception_handler(CustomException)
    async def custom_exception_handler(request: Request, exc: CustomException):
        del request

        return JSONResponse(
            status_code=exc.code,
            content={"error_code": exc.error_code, "message": exc.message},
        )

    @app_.exception_handler(Exception)
    async def unicorn_exception_handler(request: Request, exc: Exception):
        log_name = get_logger(exc)

        logging.info(request.scope.get("raw_path"))
        logging.info(request.__dict__)
        logging.exception(exc)

        return JSONResponse(
            status_code=500,
            content={
                "Exception": f"{exc.__class__.__name__}{exc.args}",
                "message": f"See internal log '{log_name}.log' for more info",
            },
        )


def on_auth_error(exc: Exception):
    """
    Authentication exception handler
    """
    status_code, error_code, message = 401, None, str(exc)
    if isinstance(exc, CustomException):
        status_code = int(exc.code)
        error_code = exc.error_code
        message = exc.message

    return JSONResponse(
        status_code=status_code,
        content={"error_code": error_code, "message": message},
    )


def make_middleware() -> list[Middleware]:
    """
    Initialize FastAPI middleware
    """
    middleware = [
        Middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        ),
        Middleware(
            AuthenticationMiddleware,
            backend=AuthBackend(),
            on_error=on_auth_error,
        ),
        Middleware(SQLAlchemyMiddleware),
        Middleware(ResponseLogMiddleware),
    ]
    return middleware


def init_cache() -> None:
    """
    Initialize cache
    """
    Cache.init(backend=RedisBackend(), key_maker=CustomKeyMaker())


def create_app() -> FastAPI:
    """
    Create app
    """
    app_ = FastAPI(
        title="Munchie",
        description="Munchie API",
        version="0.5.6",
        docs_url=None if config.ENV == "production" else "/docs",
        redoc_url=None if config.ENV == "production" else "/redoc",
        dependencies=[Depends(Logging)],
        middleware=make_middleware(),
    )

    init_routers(app_=app_)
    init_listeners(app_=app_)
    init_cache()
    start_tasks()

    app_ = VersionedFastAPI(
        app_,
        init_func=init_listeners,
        enable_latest=True,
        version_format="{major}",
        prefix_format="/v{major}",
        app_prefix="/api",
        dependencies=[Depends(Logging)],
        middleware=make_middleware(),
    )

    return app_


app = create_app()


@app.get("/")
async def get():
    with open("tests/ws_test.html", "r", encoding="utf-8") as ws_test:
        html = ws_test.read()
    return HTMLResponse(html)


# Greg is disappointed
