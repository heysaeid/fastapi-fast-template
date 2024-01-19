from typing import Generic, TypeVar
from sqlalchemy import select, Select
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic.types import PositiveInt
from database import Base


ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """
    Generic base repository class for working with SQLAlchemy models.

    This class provides a set of methods for creating, reading, updating, and deleting models.
    It is designed to be subclassed by specific repository implementations.

    Parameters:
    - db_session (AsyncSession): The asynchronous database session to use for database operations.
    """
    model_class: ModelType
    
    def __init__(self, db_session: AsyncSession) -> None:
        self.session = db_session

    async def get_by_id(self, id: PositiveInt) -> ModelType | None:
        """
        Retrieves a single record of the associated model by its unique identifier.

        :param id: The unique identifier of the record to retrieve.
        :type id: PositiveInt

        :return: An instance of the model if found, or None if no record with the specified ID exists.
        :rtype: ModelType | None

        Example usage:
        ```
        # Retrieve a record by ID
        record_id = 1
        result = await base_repo.get_by_id(record_id)
        if result:
            print(f"Record found: {result}")
        else:
            print("Record not found.")
        ```
        """
        query = self._select()
        query = query.filter(self.model_class.id == id)
        query = await self.session.scalars(query)
        return query.one_or_none()
    
    async def get_all(
        self, 
        skip: PositiveInt = 0, 
        limit: PositiveInt = 100, 
    ) -> list[ModelType]:
        """
        Retrieves a specified range of records of the associated model.

        :param skip: The number of records to skip before starting to retrieve.
                    Defaults to 0, meaning no records are skipped.
        :type skip: PositiveInt

        :param limit: The maximum number of records to retrieve.
                    Defaults to 100, limiting the number of records returned.
        :type limit: PositiveInt

        :return: A list of instances of the model within the specified range.
        :rtype: list[ModelType]

        Example usage:
        ```
        # Retrieve a range of records with skipping and limiting
        records_range = await base_repo.get_all(skip=10, limit=20)
        for record in records_range:
            print(record)
        ```
        """
        query = self._select()
        query = query.offset(skip).limit(limit)
        query = await self.session.scalars(query)
        return query.all()
    
    async def filter_by(
        self, 
        query: Select = None, 
        **kwargs
    ) -> list[ModelType]:
        """
        Filters records of the associated model based on provided filters and keyword arguments.

        :param query: An optional SQLAlchemy Select query object. If not provided,
                    a default query is created using the `_select` method.
        :type query: Select | None

        :param kwargs: Additional filters provided as keyword arguments.
                    These are applied using the standard filter syntax of SQLAlchemy.
        :type kwargs: Any

        :return: A list of model instances that satisfy the specified filters.
        :rtype: list[ModelType]

        Example usage:
        ```
        # Filter records using a custom query and additional keyword filters
        custom_query = session.query(ModelType).join(OtherModel)
        results = await base_repo.filter_by(query=custom_query, name='John', age=25)

        # Filter records using the default query and additional keyword filters
        results = await base_repo.filter_by(name='John', city='New York')
        ```
        """
        query = self._select() if query is None else query
        query = query.filter_by(**kwargs)
        query = await self.session.scalars(query)
        return query.all()

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
        entity: ModelType = None,
        commit: bool = False,
        **kwargs,
    ) -> ModelType:
        """
        Creates a new record of the associated model, optionally initializing it with provided data.

        :param entity: An optional instance of the model to be created. If not provided, a new instance
                    is created with the specified keyword arguments.
        :type entity: ModelType | None

        :param kwargs: Optional keyword arguments to initialize the new model instance.
        :type kwargs: Any

        :return: The created instance of the model.
        :rtype: ModelType

        Example usage:
        ```
        # Create a new record with specific data
        new_record_data = {'name': 'John Doe', 'age': 30, 'city': 'New York'}
        new_record = await base_repo.create(**new_record_data)
        print(f"New record created: {new_record}")

        # Create a new record with a pre-existing instance
        existing_record = MyModel(name='Jane Doe', age=25, city='Los Angeles')
        created_record = await base_repo.create(entity=existing_record)
        print(f"New record created: {created_record}")
        ```
        """  
        if entity is None:
            entity = self.model_class(**kwargs)
        
        self.session.add(entity)
        await self.commit(commit)
        return entity
    
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
    
    async def get_by(self, field: str, value: any) -> list[ModelType] | None:
        """
        Retrieves a list of model instance from the database based on the specified field and value.

        Parameters:
        - field: The name of the field to filter on.
        - value: The value to filter the field by.

        Returns:
        - ModelType or None: The retrieved model instance, or None if no matching instance is found.

        """
        
        query = self._select()
        query = query.filter(getattr(self.model_class, field) == value)
        query = await self.session.scalars(query)
        return query.all()
    
    async def one_or_none(self, field: str, value: any) -> ModelType | None:
        """
        Retrieves a single model instance from the database based on the specified field and value.

        Parameters:
        - field: The name of the field to filter on.
        - value: The value to filter the field by.

        Returns:
        - ModelType or None: The retrieved model instance, or None if no matching instance is found.

        """
        
        query = self._select()
        query = query.filter(getattr(self.model_class, field) == value)
        query = await self.session.scalars(query)
        return query.one_or_none()
    
    def _select(self) -> Select:
        return select(self.model_class)