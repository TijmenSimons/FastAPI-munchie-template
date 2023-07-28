"""GET CURRENT USER DEPENDENCY"""

from fastapi import Request
from app.user.exceptions.user import UserNotFoundException
from app.user.repository.user import UserRepository
from core.db.models import User


async def get_current_user(request: Request) -> User:
    """
    Get current user from request.

    Parameters
    ----------
    request : Request
        Request object.
    
    Returns
    -------
    User
        User object.

    Raises
    ------
    User not found
        UserNotFoundException
    """
    user = request.user

    if not user or not user.id:
        return None

    user = await UserRepository().get_by_id(user.id)

    if not user:
        raise UserNotFoundException
    
    return user
