from contextvars import ContextVar, Token
import enum
from typing import Union
import sqlalchemy

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_scoped_session,
)
from sqlalchemy.orm import sessionmaker, Session, DeclarativeBase
from sqlalchemy.sql.expression import Update, Delete, Insert

from core.config import config

session_context: ContextVar[str] = ContextVar("session_context")


def get_session_context() -> str:
    return session_context.get()


def set_session_context(session_id: str) -> Token:
    return session_context.set(session_id)


def reset_session_context(context: Token) -> None:
    session_context.reset(context)


engines = {
    "writer": create_async_engine(config.WRITER_DB_URL, pool_recycle=3600),
    "reader": create_async_engine(config.READER_DB_URL, pool_recycle=3600),
}


class RoutingSession(Session):
    def get_bind(self, mapper=None, clause=None, **kw):
        if self._flushing or isinstance(clause, (Update, Delete, Insert)):
            return engines["writer"].sync_engine
        else:
            return engines["reader"].sync_engine


# Added `expire_on_commit=False` because of the error: 
# " 
#   greenlet_spawn has not been called; can't call await_only() here. 
#   Was IO attempted in an unexpected place?
# " 
async_session_factory = sessionmaker(
    class_=AsyncSession,
    sync_session_class=RoutingSession,
    expire_on_commit=False,
)
session: Union[AsyncSession, async_scoped_session] = async_scoped_session(
    session_factory=async_session_factory,
    scopefunc=get_session_context,
)


class Base(DeclarativeBase):
    """Base class for SQLAlchemy"""

    # type annotation map is for the enums to be represented as their value, not their key
    type_annotation_map = {
        enum.Enum: sqlalchemy.Enum(enum.Enum, values_callable=lambda x: [e.value for e in x]),
    }
