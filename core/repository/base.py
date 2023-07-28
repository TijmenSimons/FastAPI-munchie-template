"""
Base reposity to contain crud logic
"""

from typing import TypeVar, Type, Optional, Generic

from sqlalchemy import select, update, delete
from sqlalchemy.inspection import inspect

from core.db.session import Base, session
from core.db.transactional import Transactional
from core.repository.enum import SynchronizeSessionEnum

Model = TypeVar("Model", bound=Base)


class BaseRepo(Generic[Model]):
    """
    A generic repository that provides basic database operations for a given SQLAlchemy model.
    """

    def __init__(self, model: Type[Model]):
        """
        Initializes the repository.

        :param model: The SQLAlchemy model class for which the repository should provide operations.
        """
        self.model = model
    
    def query_options(self, query):
        return query

    async def get_by_id(self, model_id: int) -> Optional[Model]:
        """
        Returns a single model instance with the given ID.

        :param model_id: The ID of the model instance to return.
        :return: The model instance with the given ID, or None if no such instance exists.
        """
        query = select(self.model).where(self.model.id == model_id)
        query = self.query_options(query)
        result = await session.execute(query)
        return result.scalars().first()

    async def update_by_id(
        self,
        model_id: int,
        params: dict,
        synchronize_session: SynchronizeSessionEnum = False,
    ) -> None:
        """
        Updates a single model instance with the given ID.

        :param model_id: The ID of the model instance to update.
        :param params: A dictionary containing the attribute-value pairs to update.
        :param synchronize_session: An optional parameter specifying the level of synchronization
        to use.
        """
        query = (
            update(self.model)
            .where(self.model.id == model_id)
            .values(**params)
            .execution_options(synchronize_session=synchronize_session)
        )
        query = self.query_options(query)
        await session.execute(query)

    @Transactional()
    async def delete(self, model: Model) -> None:
        """
        Deletes the given model instance.

        :param model: The model instance to delete.
        """
        await session.delete(model)

    async def delete_by_id(
        self,
        model_id: int,
        synchronize_session: SynchronizeSessionEnum = False,
    ) -> None:
        """
        Deletes a single model instance with the given ID.

        :param model_id: The ID of the model instance to delete.
        :param synchronize_session: An optional parameter specifying the level of synchronization to use.
        """
        query = (
            delete(self.model)
            .where(self.model.id == model_id)
            .execution_options(synchronize_session=synchronize_session)
        )
        await session.execute(query)

    async def create(self, model: Model) -> int:
        """
        Creates a new model instance.

        :param model: The model instance to create.
        :return: The ID of the newly created model instance.
        """
        session.add(model)
        await session.flush()
        return model.__dict__.get(inspect(self.model).primary_key[0].name)
