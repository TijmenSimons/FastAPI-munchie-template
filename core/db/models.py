"""Database models."""

from datetime import datetime
from typing import List
import uuid
from sqlalchemy import (
    Column,
    String,
    ForeignKey,
    JSON,
    func,
)
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.ext.hybrid import hybrid_property
from core.db import Base
from core.db.mixins import TimestampMixin
from core.db.enums import SwipeSessionEnum, TagType
from core.config import config

# pylint: disable=too-few-public-methods
# pylint: disable=missing-class-docstring


class RecipeJudgement(Base, TimestampMixin):
    __tablename__ = "recipe_judgement"

    recipe_id: Mapped[int] = mapped_column(
        ForeignKey("recipe.id", ondelete="CASCADE"), primary_key=True
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"), primary_key=True
    )
    like: Mapped[bool] = mapped_column(default=False)

    user: Mapped["User"] = relationship(back_populates="judged_recipes")
    recipe: Mapped["Recipe"] = relationship(back_populates="judgements")


class User(Base, TimestampMixin):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    display_name: Mapped[str] = mapped_column(String(50), nullable=False)
    is_admin: Mapped[bool] = mapped_column(default=False)
    client_token: Mapped[uuid.UUID] = mapped_column(unique=True, nullable=False)
    filename: Mapped[str] = mapped_column(
        ForeignKey("file.filename", ondelete="CASCADE"), nullable=True
    )

    image: Mapped["File"] = relationship(
        back_populates="user", lazy="immediate", foreign_keys=[filename]
    )
    account_auth: Mapped["AccountAuth"] = relationship(
        back_populates="user",
        lazy="immediate",
        cascade="all, delete",
        passive_deletes=True,
    )
    recipes: Mapped[List["Recipe"]] = relationship(back_populates="creator")
    judged_recipes: Mapped[List[RecipeJudgement]] = relationship(
        back_populates="user", cascade="all, delete"
    )
    groups: Mapped[List["GroupMember"]] = relationship(
        back_populates="user", cascade="all, delete"
    )
    filters: Mapped[List["UserTag"]] = relationship(
        back_populates="user", cascade="all, delete"
    )
    uploaded_files: Mapped[List["File"]] = relationship(
        back_populates="uploaded_by",
        cascade="all, delete",
        foreign_keys="[File.user_id]",
    )


class AccountAuth(Base, TimestampMixin):
    __tablename__ = "account_auth"

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)
    username: Mapped[str] = mapped_column(String(50))
    password: Mapped[str] = mapped_column()

    user: Mapped[User] = relationship(
        back_populates="account_auth", cascade="all, delete", passive_deletes=True
    )


class RecipeIngredient(Base):
    __tablename__ = "recipe_ingredient"

    recipe_id: Mapped[int] = mapped_column(
        ForeignKey("recipe.id", ondelete="CASCADE"), primary_key=True
    )
    ingredient_id: Mapped[int] = mapped_column(
        ForeignKey("ingredient.id", ondelete="CASCADE"), primary_key=True
    )
    unit: Mapped[str] = mapped_column()
    amount: Mapped[float] = mapped_column()

    recipe: Mapped["Recipe"] = relationship(back_populates="ingredients")
    ingredient: Mapped["Ingredient"] = relationship(back_populates="recipes")


class RecipeTag(Base):
    __tablename__ = "recipe_tag"

    recipe_id: Mapped[int] = mapped_column(
        ForeignKey("recipe.id", ondelete="CASCADE"), primary_key=True
    )
    tag_id: Mapped[int] = mapped_column(
        ForeignKey("tag.id", ondelete="CASCADE"), primary_key=True
    )

    recipe: Mapped["Recipe"] = relationship(back_populates="tags")
    tag: Mapped["Tag"] = relationship(back_populates="recipes")

    def __repr__(self) -> str:
        return f"RecipeTag({self.recipe.name}/{self.tag.name})"


class UserTag(Base):
    __tablename__ = "user_tag"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"), primary_key=True
    )
    tag_id: Mapped[int] = mapped_column(
        ForeignKey("tag.id", ondelete="CASCADE"), primary_key=True
    )

    user: Mapped["User"] = relationship(back_populates="filters")
    tag: Mapped["Tag"] = relationship(back_populates="users")


class File(Base):
    __tablename__ = "file"

    filename: Mapped[str] = mapped_column(String(), primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"), primary_key=True
    )
    recipe: Mapped["Recipe"] = relationship(back_populates="image")
    group: Mapped["Group"] = relationship(back_populates="image")
    user: Mapped["User"] = relationship(
        back_populates="image", foreign_keys="[User.filename]"
    )
    uploaded_by: Mapped["User"] = relationship(
        back_populates="uploaded_files", foreign_keys=[user_id]
    )

    @hybrid_property
    def file_url(self):
        """Get the URL of the original file."""
        return config.AZURE_IMAGE_URL_BASE + self.filename

    @hybrid_property
    def urls(self):
        """URLs of the file."""
        filename_prefix = config.AZURE_IMAGE_URL_BASE + self.filename.split(".")[0]
        return {
            "thumbnail": filename_prefix + "-thumbnail.webp",
            "xs": filename_prefix + "-xs.webp",
            "sm": filename_prefix + "-sm.webp",
            "md": filename_prefix + "-md.webp",
            "lg": filename_prefix + "-lg.webp",
        }


class Recipe(Base, TimestampMixin):
    __tablename__ = "recipe"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String())
    description: Mapped[str] = mapped_column()
    instructions = Column(JSON, nullable=False)
    materials = Column(JSON, nullable=True)
    preparation_time: Mapped[int | None] = mapped_column()
    filename: Mapped[str] = mapped_column(
        ForeignKey("file.filename", ondelete="CASCADE")
    )
    creator_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))
    spiciness: Mapped[int] = mapped_column()

    image: Mapped[File] = relationship(back_populates="recipe")
    ingredients: Mapped[List[RecipeIngredient]] = relationship(
        back_populates="recipe", cascade="all, delete"
    )
    tags: Mapped[List[RecipeTag]] = relationship(
        back_populates="recipe", cascade="all, delete"
    )
    creator: Mapped[User] = relationship(back_populates="recipes")
    judgements: Mapped[RecipeJudgement] = relationship(
        back_populates="recipe", cascade="all, delete"
    )
    swipe_session_matches: Mapped[list["SwipeSession"]] = relationship(
        back_populates="swipe_match"
    )

    def __repr__(self) -> str:
        return (
            f"Recipe(id='{self.id}' "
            + f"name='{self.name}' "
            + f"creator_id='{self.creator_id}')"
        )

    @hybrid_property
    def likes(self):
        return len([judgement for judgement in self.judgements if judgement.like])

    def to_dict(self) -> dict:
        result = self.__dict__
        result["likes"] = self.likes
        return result


class Tag(Base):
    __tablename__ = "tag"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True)
    tag_type: Mapped[TagType] = mapped_column()

    recipes: Mapped[RecipeTag] = relationship(
        back_populates="tag", cascade="all, delete"
    )
    users: Mapped[UserTag] = relationship(back_populates="tag")

    def __repr__(self) -> str:
        return f"Tag({self.name})"


class Ingredient(Base):
    __tablename__ = "ingredient"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True)

    recipes: Mapped[RecipeIngredient] = relationship(
        back_populates="ingredient", cascade="all, delete"
    )


class SwipeSession(Base, TimestampMixin):
    __tablename__ = "swipe_session"

    id: Mapped[int] = mapped_column(primary_key=True)
    session_date: Mapped[datetime] = mapped_column(
        default=func.now(), server_default=func.now()  # pylint: disable=not-callable
    )
    status: Mapped[SwipeSessionEnum] = mapped_column(default=SwipeSessionEnum.READY)
    group_id: Mapped[int] = mapped_column(ForeignKey("group.id"), nullable=True)
    match_recipe_id: Mapped[int] = mapped_column(ForeignKey("recipe.id"), nullable=True)

    swipe_match: Mapped[Recipe] = relationship(back_populates="swipe_session_matches")
    swipes: Mapped[List["Swipe"]] = relationship(
        back_populates="swipe_session", cascade="all, delete", uselist=True
    )
    group: Mapped["Group"] = relationship(
        back_populates="swipe_sessions", cascade="all, delete"
    )
    recipe_queue: Mapped["SwipeSessionRecipeQueue"] = relationship(
        back_populates="swipe_session", cascade="all, delete"
    )

    def __repr__(self) -> str:
        return f"SwipeSession({self.id}, {self.session_date}, {self.status})"


class SwipeSessionRecipeQueue(Base):
    __tablename__ = "session_recipe_queue"

    swipe_session_id: Mapped[int] = mapped_column(
        ForeignKey("swipe_session.id", ondelete="cascade"), primary_key=True
    )
    swipe_session: Mapped[SwipeSession] = relationship(
        back_populates="recipe_queue", cascade="all, delete"
    )
    queue: Mapped[JSON] = Column(JSON)


class Swipe(Base, TimestampMixin):
    __tablename__ = "swipe"

    id: Mapped[int] = mapped_column(primary_key=True)
    like: Mapped[bool] = mapped_column()
    swipe_session_id: Mapped[int] = mapped_column(ForeignKey("swipe_session.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    recipe_id: Mapped[int] = mapped_column(ForeignKey("recipe.id"))

    swipe_session: Mapped[SwipeSession] = relationship(back_populates="swipes")


class Group(Base, TimestampMixin):
    __tablename__ = "group"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String())
    filename: Mapped[str] = mapped_column(
        ForeignKey("file.filename", ondelete="CASCADE")
    )

    image: Mapped[File] = relationship(back_populates="group")
    users: Mapped[List["GroupMember"]] = relationship(
        back_populates="group", cascade="all, delete"
    )
    swipe_sessions: Mapped[List[SwipeSession]] = relationship(
        back_populates="group", cascade="all, delete"
    )


class GroupMember(Base):
    __tablename__ = "group_member"

    group_id: Mapped[int] = mapped_column(ForeignKey("group.id"), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)
    is_admin: Mapped[bool] = mapped_column(default=False)

    group: Mapped[Group] = relationship(back_populates="users")
    user: Mapped[User] = relationship(back_populates="groups")
