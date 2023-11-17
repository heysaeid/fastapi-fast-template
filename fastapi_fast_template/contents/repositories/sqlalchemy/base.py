from typing import Generic, TypeVar
from database import Base
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic.types import PositiveInt, UUID


ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """
    Generic base repository class for working with SQLAlchemy models.

    This class provides a set of methods for creating, reading, updating, and deleting models.
    It is designed to be subclassed by specific repository implementations.

    Parameters:
    - db_session (AsyncSession): The asynchronous database session to use for database operations.

    Methods:
    - commit(commit: bool = False, rollback: bool = True) -> None:
        Commits the current transaction or rolls back changes based on the provided flags.

    - before_commit() -> None:
        Hook method called before committing changes to the database.

    - after_commit() -> None:
        Hook method called after committing changes to the database.

    - create(attributes: dict[str, any] = None, commit: bool = False) -> ModelType:
        Creates a new model instance in the database with the provided attributes.
        If `commit` is True, the changes will be committed to the database.

    - delete(obj: ModelType) -> None:
        Deletes the specified model instance from the database.
    """
    model_class: ModelType
    
    def __init__(self, db_session: AsyncSession) -> None:
        self.session = db_session
        
    async def commit(
        self, 
        commit: bool = True, 
        rollback: bool = True
    ) -> None:
        """
        Commits the current transaction or rolls back changes based on the provided flags.

        Parameters:
        - commit (bool): Flag indicating whether to commit changes (default: True).
        - rollback (bool): Flag indicating whether to rollback changes on exception (default: True).

        """
        try:
            if commit:
                self.before_commit()
                await self.session.commit()
                self.after_commit()
            else:
                await self.session.flush()
        except Exception as e:
            if not rollback:
                raise e
            await self.session.rollback()
                
    async def before_commit(self):
        """
        Hook method called before committing changes to the database.
        Implement this method in subclasses to perform any pre-commit operations.
        
        """
        ...
        
    async def after_commit(self):
        """
        Hook method called after committing changes to the database.
        Implement this method in subclasses to perform any post-commit operations.

        """
        ...
        
    async def create(
        self, 
        attributes: dict[str, any] = None,
        commit: bool = False,
    ) -> ModelType:
        """
        Creates a new model instance in the database with the provided attributes.

        Parameters:
        - attributes (dict[str, any]): Dictionary of attribute names and values for the new model (default: None).
        - commit (bool): Flag indicating whether to commit changes (default: False).

        Returns:
        - ModelType: The created model instance.

        """
        
        if attributes is None:
            attributes = {}
            
        model = self.model_class(**attributes)
        self.session.add(model)
        
        await self.commit(commit)
        return model
    
    async def update(
        self,
        obj: ModelType,
        attributes: dict[str, any],
        commit: bool = False,
    ) -> ModelType:
        """
        Updates the attributes of the specified model instance in the database.

        Parameters:
        - obj (ModelType): The model instance to update.
        - attributes (dict[str, any]): Dictionary of attribute names and new values.
        - commit (bool): Flag indicating whether to commit changes (default: False).

        Returns:
        - ModelType: The updated model instance.

        """
        for attr, value in attributes.items():
            setattr(obj, attr, value)

        await self.commit(commit)
        return obj
    
    async def delete(self, obj: ModelType, commit: bool = False) -> None:
        """
        Deletes the specified model instance from the database.

        Parameters:
        - obj (ModelType): The model instance to delete.
        - commit (bool): Flag indicating whether to commit changes (default: False).

        """
        await self.session.delete(obj)
        await self.session.commit(commit)
    
    async def get_by(self, field: str, value: any) -> ModelType | None:
        """
        Retrieves a single model instance from the database based on the specified field and value.

        Parameters:
        - field: The name of the field to filter on.
        - value: The value to filter the field by.

        Returns:
        - ModelType or None: The retrieved model instance, or None if no matching instance is found.

        """
        return await self.session.query(self.model_class).filter_by(
            **{field: value}
        ).one()
    
    async def get_by_id(self, id: PositiveInt | UUID) -> ModelType | None:
        """
        Retrieves a single model instance from the database based on the specified ID.

        Parameters:
        - id: The ID of the model instance to retrieve.

        Returns:
        - ModelType or None: The retrieved model instance, or None if no matching instance is found.

        """
        return await self.session.query(self.model_class).filter_by(
            id = id
        ).one()
        
    async def get_all(
        self, 
        skip: PositiveInt = 0, 
        limit: PositiveInt = 100, 
        **filters
    ) -> list[ModelType]:
        """
        Retrieves a list of model instances from the database based on the specified filters, with optional pagination.

        Parameters:
        - skip: The number of instances to skip (for pagination).
        - limit: The maximum number of instances to retrieve (for pagination).
        - **filters: Keyword arguments representing additional filters to apply.

        Returns:
        - list[ModelType]: A list of retrieved model instances.

        """
        return await self.session.query(self.model_class).filter_by(
            **filters
        ).offset(skip).limit(limit)
    
    async def count(self, **filters) -> PositiveInt:
        """
        Counts the number of model instances in the database based on the specified filters.

        Parameters:
        - **filters: Keyword arguments representing the filters to apply.

        Returns:
        - PositiveInt: The count of matching model instances.

        """
        return await self.session.query(self.model_class).filter_by(
            **filters
        ).count()