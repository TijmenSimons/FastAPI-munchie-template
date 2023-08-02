"""
Class business logic for the authentication
"""

from fastapi import Response
from core.exceptions.token import DecodeTokenException
from core.fastapi.schemas.token import TokensSchema
from app.auth.services.jwt import JwtService
from app.user.exceptions.user import IncorrectPasswordException, UserNotFoundException
from app.user.services.user import UserService
from app.user.utils import verify_password


class AuthService:
    """
    Service class for handling authentication-related functionality.

    Attributes:
        jwt (JwtService): An instance of the JwtService class for handling JSON Web 
        Tokens.
        user_serv (UserService): An instance of the UserService class for interacting 
        with user 
        data.

    Methods:
        login(username: str, password: str) -> TokensSchema:
            Authenticates a user by their display name and password, and returns a pair 
            of JSON Web Tokens.
    """

    def __init__(self) -> None:
        """
        Initializes an instance of the AuthService class.
        """
        self.jwt = JwtService()
        self.user_serv = UserService()

    async def login(self, username: str, password: str) -> TokensSchema:
        """
        Authenticates a user by their display name and password, and returns a pair of 
        JSON Web Tokens.

        Args:
            username (str): The user's display name.
            password (str): The user's password.

        Raises:
            UserNotFoundException: If a user with the provided display name is not 
            found.
            IncorrectPasswordException: If the provided password does not match the 
            user's password.

        Returns:
            TokensSchema: A pair of JSON Web Tokens (access and refresh tokens).
        """
        user = await self.user_serv.get_by_username(username)
        if not user:
            raise UserNotFoundException()
        if not verify_password(password, user.password):
            raise IncorrectPasswordException()

        return await self.jwt.create_login_tokens(user_id=user.id)
    
    async def refresh_tokens(self, refresh_token: str) -> str:
        return await JwtService().refresh_tokens(refresh_token=refresh_token)

    async def verify_token(self, token: str):
        try:
            await JwtService().verify_token(token=token)

        except DecodeTokenException:
            return Response(status_code=400)

        except Exception:
            return Response(status_code=500)

        return Response(status_code=200)
