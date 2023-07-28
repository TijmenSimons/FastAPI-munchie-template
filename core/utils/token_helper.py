from datetime import datetime, timedelta

import jwt

from core.config import config
from core.exceptions import DecodeTokenException, ExpiredTokenException
from core.utils.token_checker import token_checker


class TokenHelper:
    @staticmethod
    def encode_access(payload: dict):
        return TokenHelper.encode(payload, config.ACCESS_TOKEN_EXPIRE_PERIOD)

    @staticmethod
    def encode_refresh(payload: dict = None):
        if not payload:
            payload = {}

        if not payload.get("sub"):
            payload["sub"] = "refresh"

        if not payload.get("jti"):
            payload["jti"] = token_checker.generate_add()

        return TokenHelper.encode(payload, config.REFRESH_TOKEN_EXPIRE_PERIOD)

    @staticmethod
    def encode(payload: dict, expire_period: int) -> str:
        token = jwt.encode(
            payload={
                **payload,
                "exp": datetime.utcnow() + timedelta(seconds=expire_period),
            },
            key=config.JWT_SECRET_KEY,
            algorithm=config.JWT_ALGORITHM,
        )  # .decode("utf8")
        return token

    @staticmethod
    def decode(token: str) -> dict:
        try:
            return jwt.decode(
                token,
                config.JWT_SECRET_KEY,
                config.JWT_ALGORITHM,
            )
        except jwt.exceptions.DecodeError as exc:
            raise DecodeTokenException from exc
        except jwt.exceptions.ExpiredSignatureError as exc:
            raise ExpiredTokenException from exc

    @staticmethod
    def decode_expired_token(token: str) -> dict:
        try:
            return jwt.decode(
                token,
                config.JWT_SECRET_KEY,
                config.JWT_ALGORITHM,
                options={"verify_exp": False},
            )
        except jwt.exceptions.DecodeError as exc:
            raise DecodeTokenException from exc
