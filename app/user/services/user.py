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
from app.user.schemas.user import SetAdminSchema, UpdateUserSchema
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

    async def update(self, user_id: int, updated_user: UpdateUserSchema) -> User:
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
        if not updated_user.password:
            user: User = await self.repo.get_by_id(user_id)
            updated_user.password = user.password

        else:
            updated_user.password = get_password_hash(updated_user.password)

        user_dict = updated_user.dict()

        await self.repo.update_by_id(model_id=user_id, params=user_dict)
        user = await self.repo.get_by_id(user_id)
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

        user = User(display_name=display_name, username=username, password=hashed_pwd)
        user_id = await self.repo.create(user)
        return user_id

    async def set_admin(self, user_id: int, request: SetAdminSchema):
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

        await self.repo.set_admin(user, request.is_admin)
        return user

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

        await self.repo.delete(user)
