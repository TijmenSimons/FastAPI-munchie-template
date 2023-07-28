"""
Class business logic for json web tokens
"""

from api.auth.v1.response.auth import TokensSchema
from core.exceptions.base import UnauthorizedException
from core.exceptions.token import DecodeTokenException
from core.helpers.hashid import decode_single, encode
from core.utils.token_checker import token_checker
from core.utils.token_helper import TokenHelper


class JwtService:
    """
    Class for JSON Web Token business logic
    """

    async def verify_token(self, token: str) -> None:
        """
        Verify the given token

        Args:
            token (str): The token to verify

        Raises:
            DecodeTokenException: If the token cannot be decoded
        """
        TokenHelper.decode(token=token)

    async def refresh_tokens(
        self,
        refresh_token: str,
    ) -> TokensSchema:
        """
        Create a new refresh token

        Args:
            refresh_token (str): The old refresh token to use as a template for the new
            refresh token

        Returns:
            TokensSchema: A new set of tokens containing the new access token and refresh token

        Raises:
            DecodeTokenException: If the old refresh token cannot be decoded
            UnauthorizedException: If the new token ID cannot be generated
        """
        refresh_token = TokenHelper.decode(token=refresh_token)

        if refresh_token.get("jti") is None:
            raise DecodeTokenException

        if refresh_token.get("sub") != "refresh":
            raise DecodeTokenException

        user_id = decode_single(refresh_token.get("user_id"))
        user_id = encode(user_id)

        try:
            jti = token_checker.generate_add(refresh_token.get("jti"))

        except ValueError as exc:
            raise UnauthorizedException from exc

        except KeyError as exc:
            raise DecodeTokenException from exc

        return TokensSchema(
            access_token=TokenHelper.encode_access(payload={"user_id": user_id}),
            refresh_token=TokenHelper.encode_refresh(
                payload={"jti": jti, "user_id": user_id}
            ),
        )

    async def create_login_tokens(self, user_id: int):
        """
        Create a new set of access and refresh tokens for the given user

        Args:
            user_id (int): The ID of the user to create tokens for

        Returns:
            TokensSchema: A new set of tokens containing the access and refresh tokens
        """
        user_id = encode(int(user_id))

        return TokensSchema(
            access_token=TokenHelper.encode_access(payload={"user_id": user_id}),
            refresh_token=TokenHelper.encode_refresh(payload={"user_id": user_id}),
        )
