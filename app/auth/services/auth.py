"""
Class business logic for the authentication
"""

import uuid
from api.auth.v1.response.auth import TokensSchema
from app.auth.exceptions.auth import BadUUIDException
from app.auth.services.jwt import JwtService
from app.user.exceptions.user import IncorrectPasswordException, UserNotFoundException
from app.user.services.user import UserService
from app.user.utils import verify_password


class AuthService:
    """
    Service class for handling authentication-related functionality.

    Attributes:
        jwt (JwtService): An instance of the JwtService class for handling JSON Web Tokens.
        user_serv (UserService): An instance of the UserService class for interacting with user 
        data.

    Methods:
        login(username: str, password: str) -> TokensSchema:
            Authenticates a user by their display name and password, and returns a pair of JSON 
            Web Tokens.

        client_token_login(ctoken: str) -> TokensSchema:
            Authenticates a user by their client token, and returns a pair of JSON Web Tokens.
    """

    def __init__(self) -> None:
        """
        Initializes an instance of the AuthService class.
        """
        self.jwt = JwtService()
        self.user_serv = UserService()

    async def login(self, username: str, password: str) -> TokensSchema:
        """
        Authenticates a user by their display name and password, and returns a pair of JSON Web 
        Tokens.

        Args:
            username (str): The user's display name.
            password (str): The user's password.

        Raises:
            UserNotFoundException: If a user with the provided display name is not found.
            IncorrectPasswordException: If the provided password does not match the user's password.

        Returns:
            TokensSchema: A pair of JSON Web Tokens (access and refresh tokens).
        """
        user = await self.user_serv.get_by_username(username)
        if not user:
            raise UserNotFoundException()
        if not verify_password(password, user.account_auth.password):
            raise IncorrectPasswordException()

        return await self.jwt.create_login_tokens(user_id=user.id)

    async def client_token_login(self, ctoken) -> TokensSchema:
        """
        Authenticates a user by their client token, and returns a pair of JSON Web Tokens.

        Args:
            ctoken (str): The user's client token.

        Raises:
            BadUUIDException: If the provided client token is not a valid UUID.

        Returns:
            TokensSchema: A pair of JSON Web Tokens (access and refresh tokens).
        """
        try:
            ctoken = uuid.UUID(str(ctoken), version=4)
        except ValueError as exc:
            raise BadUUIDException from exc

        user = await self.user_serv.get_by_client_token(ctoken=ctoken)

        if not user:
            user_id = await self.user_serv.create_user_with_client_token(
                ctoken=ctoken, display_name=None
            )
        else:
            user_id = user.id

        return await self.jwt.create_login_tokens(user_id=user_id)
