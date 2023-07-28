"""
Permission class to approve and refuse access on websockets.
"""

from abc import ABC, abstractmethod
from typing import Annotated, List, Type

from fastapi import Cookie, Query, WebSocketException, status
from app.swipe_session.services.swipe_session import SwipeSessionService
from app.user.services.user import UserService
from app.group.services.group import GroupService
from core.db.enums import SwipeSessionEnum

from core.exceptions.base import CustomException, UnauthorizedException
from core.exceptions.hashids import IncorrectHashIDException
from core.exceptions.websocket import InactiveException, InvalidIdException
from core.helpers.hashid import decode_single
from core.utils.token_helper import TokenHelper

# pylint: disable=too-few-public-methods


async def get_cookie_or_token(
    access_token: Annotated[str | None, Cookie()] = None,
    token: Annotated[str | None, Query()] = None,
):
    """Retrieve access_token from cookie or query parameter"""
    if access_token is None and token is None:
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)
    return access_token or token


class BaseWebsocketPermission(ABC):
    """Base permission for websocket authentication and authorization"""

    exception = UnauthorizedException

    @abstractmethod
    async def has_permission(self, **kwargs) -> bool:
        """Placeholder function to check permission"""


class AllowAll(BaseWebsocketPermission):
    """Always allow access"""

    async def has_permission(self, **kwargs) -> bool:
        """Function to check permission"""
        return True


class IsAuthenticated(BaseWebsocketPermission):
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


class IsSessionMember(BaseWebsocketPermission):
    """Only allow access if authenticated"""

    async def has_permission(self, **kwargs) -> bool:
        """Function to check permission"""
        access_token = kwargs.get("access_token")
        swipe_session_id = kwargs.get("swipe_session_id")

        if not access_token or not swipe_session_id:
            return False

        try:
            decoded_token = TokenHelper.decode(token=access_token)
        except CustomException:
            return False

        try:
            user_id = decode_single(decoded_token.get("user_id"))
            swipe_session_id = decode_single(swipe_session_id)
        except IncorrectHashIDException:
            self.exception = InvalidIdException
            return False

        try:
            await UserService().get_by_id(user_id)
            swipe_session = await SwipeSessionService().get_swipe_session_by_id(
                swipe_session_id
            )
        except CustomException:
            return False

        return await GroupService().is_member(swipe_session.group_id, user_id)


class IsActiveSession(BaseWebsocketPermission):
    """Only allow access if session is active"""
    exception = InactiveException

    async def has_permission(self, **kwargs) -> bool:
        """Function to check permission"""
        swipe_session_id = kwargs.get("swipe_session_id")

        if not swipe_session_id:
            return False

        try:
            swipe_session_id = decode_single(swipe_session_id)
        except IncorrectHashIDException:
            return False

        swipe_session = await SwipeSessionService().get_swipe_session_by_id(
            swipe_session_id
        )
        if not swipe_session:
            return False

        return swipe_session.status == SwipeSessionEnum.IN_PROGRESS


class WebsocketPermission:
    """Callable class to check permissions with the given access token"""

    def __init__(self, permissions: List[List[Type[BaseWebsocketPermission]]]):
        self.permissions = permissions

    async def __call__(self, **kwargs):
        exceptions = {}
        for i, permission_combo in enumerate(self.permissions):
            exceptions[i] = []

            for permission in permission_combo:
                cls = permission()
                if not await cls.has_permission(**kwargs):
                    exceptions[i].append(cls.exception)

        if any(len(excs) == 0 for _, excs in exceptions.items()):
            return

        for _, excs in exceptions.items():
            if len(excs) > 0:
                raise excs[0]
