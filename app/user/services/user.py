"""
User service module
"""

from typing import List
from app.user.exceptions.user import (
    UserNotFoundException,
    DuplicateUsernameException,
)
from app.user.utils import get_password_hash
from app.user.repository.user import UserRepository
from app.user.schemas.user import UpdateUserSchema
from core.db.models import User
from core.db.session import session


class UserService:
    """Class that handles user-related business logic.

    Attributes
    ----------
    repo : UserRepository
        UserRepository instance used for database operations.
    """

    def __init__(self):
        """Constructor for the UserService class."""
        self.repo = UserRepository()

    async def get_user_list(self) -> List[User]:
        """Get the list of all users in the system.

        Returns
        -------
        List[User]
            The list of all users.
        """
        return await self.repo.get_user_list()

    async def update(self, updated_user: UpdateUserSchema) -> User:
        """
        Updates the user information in the repository.

        Args:
            updated_user (UpdateUserSchema): An object containing the updated user 
            information.

        Raises:
            FileNotFoundException: If the specified image filename does not exist in the
            image repository.

        Returns:
            int: The ID of the updated user.
        """
        user_dict = updated_user.dict()

        await self.repo.update_by_id(model_id=updated_user.id, params=user_dict)
        user = await self.repo.get_by_id(updated_user.id)
        await session.refresh(user)
        return user

    async def get_by_username(self, username) -> User:
        """Get the user with the given username.

        Parameters
        ----------
        username : str
            The username of the user.

        Returns
        -------
        User
            The user with the given username.

        Raises
        ------
        UserNotFoundException
            If the user with the given username does not exist.
        """
        return await self.repo.get_by_username(username)

    async def get_by_display_name(self, display_name) -> User:
        """Get the user with the given display name.

        Parameters
        ----------
        display_name : str
            The display name of the user.

        Returns
        -------
        User
            The user with the given display name.

        Raises
        ------
        UserNotFoundException
            If the user with the given display name does not exist.
        """
        return await self.repo.get_by_display_name(display_name)

    async def get_by_id(self, user_id: int) -> User:
        """Get a user by id.

        Parameters
        ----------
        user_id : int
            The id of the user to get.

        Returns
        -------
        User
            The user with the given id.

        Raises
        ------
        UserNotFoundException
            If the user with the given id does not exist.
        """
        user = await self.repo.get_by_id(user_id)
        if not user:
            raise UserNotFoundException()
        return user

    async def create_user(self, display_name: str, username: str, password: str) -> int:
        """Create a new authenticated user with the given username and password.

        Parameters
        ----------
        username : str
            The username of the new user.
        password : str
            The password of the new user.

        Returns
        -------
        int
            The id of the newly created user.

        Raises
        ------
        DuplicateUsernameException
            If a user with the given username already exists.
        """
        user = await self.repo.get_by_username(username)
        if user:
            raise DuplicateUsernameException()
        hashed_pwd = get_password_hash(password)

        user_id = await self.repo.create_user(display_name, username, hashed_pwd)
        return user_id

    async def set_admin(self, user_id: int, is_admin: bool):
        """Set admin status for a user.

        Parameters
        ----------
        user_id : int
            The id of the user whose admin status will be updated.
        is_admin : bool
            The value to set for the user's admin status.

        Raises
        ------
        UserNotFoundException
            If the user with the given id does not exist.
        """
        user = await self.get_by_id(user_id)
        await self.repo.set_admin(user, is_admin)

    async def is_admin(self, user_id: int) -> bool:
        """Check if a user is an admin.

        Parameters
        ----------
        user_id : int
            The id of the user to check.

        Returns
        -------
        bool
            True if the user is an admin, False otherwise.

        Raises
        ------
        UserNotFoundException
            If the user with the given id does not exist.
        """
        user = await self.get_by_id(user_id)
        return user.is_admin

    async def delete_user(self, user_id) -> None:
        """Delete's a user by given id.

        Parameters
        ----------
        user_id : int
            The id of the user to delete.
        """
        user = await self.repo.get_by_id(user_id)

        if not user:
            raise UserNotFoundException

        if user.account_auth:
            await self.repo.delete(user.account_auth)

        await self.repo.delete(user)
