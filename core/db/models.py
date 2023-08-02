"""Database models."""


from sqlalchemy import (
    String,
)
from sqlalchemy.orm import Mapped, mapped_column
from core.db import Base
from core.db.mixins import TimestampMixin

# pylint: disable=too-few-public-methods
# pylint: disable=missing-class-docstring


class User(Base, TimestampMixin):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    display_name: Mapped[str] = mapped_column(String(), nullable=False)
    username: Mapped[str] = mapped_column(String(), nullable=False)
    password: Mapped[str] = mapped_column(String(), nullable=False)
    is_admin: Mapped[bool] = mapped_column(default=False)

    def __repr__(self) -> str:
        return f"User('{self.username}')"
