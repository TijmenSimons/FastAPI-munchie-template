from abc import ABC, abstractmethod
from typing import List, Type

from fastapi import Request
from fastapi.openapi.models import APIKey, APIKeyIn
from fastapi.security.base import SecurityBase

from app.user.services import UserService
from core.exceptions import (
    CustomException,
    UnauthorizedException,
)
from core.helpers.hashid import decode_single


def get_user_id_from_path(request):
    hashed_id = request.path_params.get("user_id")
    if not hashed_id:
        return None

    return decode_single(hashed_id)


class BasePermission(ABC):
    exception = CustomException

    @abstractmethod
    async def has_permission(self, request: Request, **kwargs) -> bool:
        del kwargs


class IsAuthenticated(BasePermission):
    exception = UnauthorizedException

    async def has_permission(self, request: Request, **kwargs) -> bool:
        del kwargs

        return request.user.id is not None


class IsUserOwner(BasePermission):
    async def has_permission(self, request: Request, **kwargs) -> bool:
        del kwargs

        user_id = get_user_id_from_path(request)

        if not user_id:
            return False

        if user_id != request.user.id:
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
    async def has_permission(self, request: Request, **kwargs) -> bool:
        del kwargs

        return True


class PermissionDependency(SecurityBase):
    def __init__(self, permissions: List[List[Type[BasePermission]]]):
        self.permissions = permissions
        self.model: APIKey = APIKey(**{"in": APIKeyIn.header}, name="Authorization")
        self.scheme_name = self.__class__.__name__

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
