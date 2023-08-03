"""
Permission class to approve and refuse access on websockets.
"""

from typing import Annotated, List, Type

from fastapi import Cookie, Query, WebSocketException, status
from core.exceptions.base import CustomException
from core.fastapi.dependencies.permission import BasePermission, PermissionDependency
from core.helpers.token import TokenHelper

# pylint: disable=too-few-public-methods


async def get_cookie_or_token(
    access_token: Annotated[str | None, Cookie()] = None,
    token: Annotated[str | None, Query()] = None,
):
    """Retrieve access_token from cookie or query parameter"""
    if access_token is None and token is None:
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)
    return access_token or token


class AllowAll(BasePermission):
    """Always allow access"""

    async def has_permission(self, **kwargs) -> bool:
        """Function to check permission"""
        del kwargs

        return True


class IsAuthenticated(BasePermission):
    """Only allow access if authenticated"""

    async def has_permission(self, **kwargs) -> bool:
        """Function to check permission"""
        access_token = kwargs.get("access_token")

        if not access_token:
            return False

        try:
            TokenHelper.decode(token=access_token)

        except CustomException:
            return False

        return True


class WebsocketPermission(PermissionDependency):
    """Callable class to check permissions with the given access token"""

    def __init__(self, permissions: List[List[Type[BasePermission]]]):
        self.permissions = permissions
