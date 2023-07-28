from abc import ABC, abstractmethod
import json
from typing import List, Type

from fastapi import Request
from fastapi.openapi.models import APIKey, APIKeyIn
from fastapi.security.base import SecurityBase

from app.group.services.group import GroupService
from app.swipe_session.services.swipe_session import SwipeSessionService
from app.image.services import ImageService
from app.user.services import UserService
from core.exceptions import (
    CustomException,
    UnauthorizedException,
)
from core.fastapi.dependencies.object_storage import get_object_storage
from core.helpers.hashid import decode_single


def get_group_id_from_path(request):
    hashed_id = request.path_params.get("group_id")
    if not hashed_id:
        return None

    return decode_single(hashed_id)


def get_user_id_from_path(request):
    hashed_id = request.path_params.get("user_id")
    if not hashed_id:
        return None

    return decode_single(hashed_id)


def get_session_id_from_path(request):
    hashed_id = request.path_params.get("session_id")
    if not hashed_id:
        return None

    return decode_single(hashed_id)


class BasePermission(ABC):
    exception = CustomException

    @abstractmethod
    async def has_permission(self, request: Request) -> bool:
        pass


class IsAuthenticated(BasePermission):
    exception = UnauthorizedException

    async def has_permission(self, request: Request) -> bool:
        return request.user.id is not None


class IsUserOwner(BasePermission):
    async def has_permission(self, request: Request) -> bool:
        user_id = get_user_id_from_path(request)

        if not user_id:
            return False

        if user_id != request.user.id:
            return False

        return True


class IsSessionOwner(BasePermission):
    async def has_permission(self, request: Request) -> bool:
        session_id = get_session_id_from_path(request)

        if not session_id:
            return False

        swipe_session = SwipeSessionService().get_swipe_session_by_id(session_id)

        if swipe_session.user_id != request.user.id:
            return False

        return True


class IsImageOwner(BasePermission):
    exception = UnauthorizedException

    async def has_permission(self, request: Request) -> bool:
        object_storage = await get_object_storage()
        image = await ImageService(object_storage).get_image_by_name(
            request.path_params.get("filename")
        )
        if image.user_id != request.user.id:
            return False

        return True


class IsAdmin(BasePermission):
    exception = UnauthorizedException

    async def has_permission(self, request: Request) -> bool:
        user_id = request.user.id
        if not user_id:
            return False

        return await UserService().is_admin(user_id=user_id)


class AllowAll(BasePermission):
    async def has_permission(self, request: Request) -> bool:
        return True


class IsGroupMember(BasePermission):
    exception = UnauthorizedException

    async def has_permission(self, request: Request) -> bool:
        user_id = request.user.id

        if not user_id:
            return False

        group_id = get_group_id_from_path(request)
        if not group_id:
            return False

        try:
            group_id = int(group_id)
        except ValueError as e:
            raise ValueError(str(e) + " did you forget to decode?")

        return await GroupService().is_member(group_id=group_id, user_id=user_id)


class IsGroupAdmin(BasePermission):
    exception = UnauthorizedException

    async def has_permission(self, request: Request) -> bool:
        user_id = request.user.id
        if not user_id:
            return False

        group_id = get_group_id_from_path(request)
        if not group_id:
            return False

        try:
            group_id = int(group_id)
        except ValueError as e:
            raise ValueError(str(e) + " did you forget to decode?")

        return await GroupService().is_admin(group_id=group_id, user_id=user_id)


class PermissionDependency(SecurityBase):
    def __init__(self, permissions: List[List[Type[BasePermission]]]):
        self.permissions = permissions
        self.model: APIKey = APIKey(**{"in": APIKeyIn.header}, name="Authorization")
        self.scheme_name = self.__class__.__name__

    async def __call__(self, request: Request):
        exceptions = {}
        for i, permission_combo in enumerate(self.permissions):
            exceptions[i] = []

            for permission in permission_combo:
                cls = permission()
                if not await cls.has_permission(request=request):
                    exceptions[i].append(cls.exception)

        if any(len(excs) == 0 for _, excs in exceptions.items()):
            return

        for _, excs in exceptions.items():
            if len(excs) > 0:
                raise excs[0]
