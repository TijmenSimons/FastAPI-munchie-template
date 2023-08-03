"""
The module contains a repository class that defines database operations for user. 
"""

from typing import List
from sqlalchemy import select
from core.db.models import User
from core.db import session
from core.db.transactional import Transactional
from core.repository.base import BaseRepo
from core.repository.enum import SynchronizeSessionEnum


class UserRepository(BaseRepo):
    """Repository class for accessing and manipulating User objects in the database."""

    def __init__(self):
        super().__init__(User)

    def query_options(self, query):
        return query.options()

    @Transactional()
    async def update_by_id(
        self,
        model_id: int,
        params: dict,
        synchronize_session: SynchronizeSessionEnum = "auto",
    ):
        await super().update_by_id(model_id, params, synchronize_session)

    async def get_by_username(self, username: str) -> User:
        """Get user by username.

        Parameters
        ----------
        username : str
            Username.

        Returns
        -------
        User
            User instance.
        """
        query = select(User).where(User.username == username)
        query = self.query_options(query)
        result = await session.execute(query)
        return result.scalars().first()

    async def get_user_list(self) -> List[User]:
        """Get user list.

        Returns
        -------
        List[User]
            User list.
        """
        query = select(User)
        query = self.query_options(query)
        result = await session.execute(query)
        return result.scalars().all()

    @Transactional()
    async def set_admin(self, user: User, is_admin: bool):
        """Set the admin status of a user.

        Parameters
        ----------
        user : User
            User instance.
        is_admin : bool
            Whether or not the user is an admin.

        Returns
        -------
        None
        """
        user.is_admin = is_admin
