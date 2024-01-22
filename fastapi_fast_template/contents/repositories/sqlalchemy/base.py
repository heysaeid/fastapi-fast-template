from typing import Generic, TypeVar

from database import Base
from pydantic.types import PositiveInt
from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

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
        self, query: Select = None, **kwargs
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

    async def commit(self, commit: bool = True, rollback: bool = True) -> None:
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
        entity: ModelType,
        commit: bool = False,
        **kwargs,
    ) -> ModelType:
        """
        Updates the specified model instance with the provided data and persists the changes.

        :param entity: The instance of the model to be updated.
        :type entity: ModelType

        :param kwargs: Keyword arguments representing the updated data for the model instance.
        :type kwargs: Any

        :return: The updated instance of the model.
        :rtype: ModelType

        Example usage:
        ```
        # Retrieve a record by ID and update it
        record_id = 1
        existing_record = await base_repo.get_by_id(record_id)
        updated_record = await base_repo.update(existing_record, age=31, city='San Francisco')
        print(f"Record updated: {updated_record}")
        ```
        """
        for key, value in kwargs.items():
            setattr(entity, key, value)

        await self.commit(commit)
        return entity

    async def delete(self, entity: ModelType) -> None:
        """
        Deletes the specified model instance from the associated data storage.

        :param entity: The instance of the model to be deleted.
        :type entity: ModelType

        Example usage:
        ```
        # Retrieve a record by ID and delete it
        record_id = 1
        existing_record = await base_repo.get_by_id(record_id)
        await base_repo.delete(existing_record)
        print("Record deleted.")
        ```
        """
        await self.session.delete(entity)
        await self.session.commit()

    async def delete_by_id(self, id: PositiveInt) -> None:
        """
        Deletes a record of the associated model by its unique identifier.

        :param id: The unique identifier of the record to be deleted.
        :type id: PositiveInt

        Example usage:
        ```
        # Delete a record by ID
        record_id = 1
        await base_repo.delete_by_id(record_id)
        print("Record deleted.")
        ```
        """
        entity = await self.get_by_id(id)
        await self.delete(entity)

    async def exists(self, id: PositiveInt) -> bool:
        """
        Checks if a record with the specified unique identifier exists in the associated data storage.

        :param id: The unique identifier of the record to check for existence.
        :type id: PositiveInt

        :return: True if a record with the specified ID exists, False otherwise.
        :rtype: bool

        Example usage:
        ```
        # Check if a record with ID 1 exists
        record_id = 1
        if await base_repo.exists(record_id):
            print("Record exists.")
        else:
            print("Record does not exist.")
        ```
        """
        query = self._select()
        query = query.filter(self.model_class.id == id).exists()
        return await self.session.scalars(query)

    async def bulk_create(
        self, entities: list[ModelType], commit: bool = True
    ) -> list[ModelType]:
        """
        Creates multiple records of the associated model in bulk.

        :param entities: A list of model instances to be created in bulk.
        :type entities: list[ModelType]

        :return: The list of created model instances.
        :rtype: list[ModelType]

        Example usage:
        ```
        # Create multiple records in bulk
        records_to_create = [
            MyModel(name='John Doe', age=30, city='New York'),
            MyModel(name='Jane Doe', age=25, city='Los Angeles'),
        ]
        created_records = await base_repo.bulk_create(records_to_create)
        print(f"{len(created_records)} records created in bulk.")
        ```
        """
        for entity in entities:
            self.session.add(entity)

        await self.commit(commit)
        return entities

    async def bulk_update(
        self,
        entities: list[ModelType],
        commit: bool = True,
    ) -> list[ModelType]:
        """
        Updates multiple records of the associated model in bulk.

        :param entities: A list of model instances with updated data to be applied in bulk.
        :type entities: list[ModelType]

        :return: The list of updated model instances.
        :rtype: list[ModelType]

        Example usage:
        ```
        # Update multiple records in bulk
        records_to_update = [
            MyModel(id=1, name='John Doe', age=31, city='San Francisco'),
            MyModel(id=2, name='Jane Doe', age=26, city='Los Angeles'),
        ]
        updated_records = await base_repo.bulk_update(records_to_update)
        print(f"{len(updated_records)} records updated in bulk.")
        ```
        """
        for entity in entities:
            await self.session.merge(entity)
        await self.commit(commit)
        return entities

    async def bulk_delete(
        self, entities: list[ModelType], commit: bool = True
    ) -> None:
        """
        Deletes multiple records of the associated model in bulk.

        :param entities: A list of model instances to be deleted in bulk.
        :type entities: List[ModelType]

        Example usage:
        ```
        # Delete multiple records in bulk
        records_to_delete = [
            MyModel(id=1),
            MyModel(id=2),
        ]
        await base_repo.bulk_delete(records_to_delete)
        print(f"{len(records_to_delete)} records deleted in bulk.")
        ```
        """
        for entity in entities:
            await self.session.delete(entity)
        await self.commit(commit)
        return entities

    def _select(self) -> Select:
        return select(self.model_class)
