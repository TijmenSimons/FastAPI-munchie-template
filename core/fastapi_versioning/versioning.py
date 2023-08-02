from collections import defaultdict
from typing import Any, Callable, Dict, List, Tuple, TypeVar, cast

from fastapi import FastAPI
from fastapi.routing import APIRoute
from starlette.routing import BaseRoute

CallableT = TypeVar("CallableT", bound=Callable[..., Any])


def version(major: int, minor: int = 0) -> Callable[[CallableT], CallableT]:
    def decorator(func: CallableT) -> CallableT:
        func._api_version = (major, minor)  # pylint: disable=protected-access
        return func

    return decorator


def version_to_route(
    route: BaseRoute,
    default_version: Tuple[int, int],
) -> Tuple[Tuple[int, int], APIRoute]:
    api_route = cast(APIRoute, route)
    _version = getattr(api_route.endpoint, "_api_version", default_version)
    return _version, api_route


def VersionedFastAPI(
    app: FastAPI,
    init_func,
    version_format: str = "{major}.{minor}",
    prefix_format: str = "/v{major}_{minor}",
    app_prefix: str = "",
    default_version: Tuple[int, int] = (1, 0),
    enable_latest: bool = False,
    **kwargs: Any,
) -> FastAPI:
    parent_app = FastAPI(
        title=app.title,
        **kwargs,
    )

    init_func(parent_app)

    version_route_mapping: Dict[Tuple[int, int], List[APIRoute]] = defaultdict(list)
    version_routes = [version_to_route(route, default_version) for route in app.routes]

    for _version, route in version_routes:
        version_route_mapping[_version].append(route)

    unique_routes = {}
    versions = sorted(version_route_mapping.keys())
    for _version in versions:
        major, minor = _version
        prefix = prefix_format.format(major=major, minor=minor)
        endpoint_version = version_format.format(major=major, minor=minor)

        versioned_app = FastAPI(
            title=app.title,
            description=app.description,
            version=f"{app.version}-{prefix}",
        )
        init_func(versioned_app)
        for route in version_route_mapping[_version]:
            try:
                for method in route.methods:
                    unique_routes[route.path + "|" + method] = route

            except AttributeError:
                unique_routes[route.path] = route

        for route in unique_routes.values():
            versioned_app.router.routes.append(route)

        parent_app.mount(f"{app_prefix}{prefix}", versioned_app)

        @parent_app.get(
            f"{app_prefix}{prefix}/openapi.json",
            name=endpoint_version,
            tags=["Versions"],
        )
        @parent_app.get(
            f"{app_prefix}{prefix}/docs",
            name=endpoint_version,
            tags=["Documentations"],
        )
        def noop() -> None:
            ...

    if enable_latest:
        prefix = "/latest"
        major, minor = _version
        endpoint_version = version_format.format(major=major, minor=minor)

        versioned_app = FastAPI(
            title=app.title,
            description=app.description,
            version=f"{app.version}-latest",
        )
        init_func(versioned_app)

        for route in unique_routes.values():
            versioned_app.router.routes.append(route)
        parent_app.mount(f"{app_prefix}{prefix}", versioned_app)

        @parent_app.get(
            f"{app_prefix}{prefix}/openapi.json",
            name=endpoint_version,
            tags=["Versions"],
        )
        @parent_app.get(
            f"{app_prefix}{prefix}/docs", name=endpoint_version, tags=["Documentations"]
        )
        def noop() -> None:
            ...

    return parent_app
