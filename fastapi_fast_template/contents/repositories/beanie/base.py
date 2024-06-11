from typing import Generic, Optional, TypeVar

from pydantic.types import PositiveInt

ModelType = TypeVar("ModelType")


class BaseRepository(Generic[ModelType]):
    """
    Generic base repository class for working with Beanie models.

    This class provides a set of methods for creating, reading, updating, and deleting models.
    It is designed to be subclassed by specific repository implementations.
    """

    model_class: ModelType

    def __str__(self):
        return f"{self.__class__.__name__}(model_class={self.model_class.__name__})"

    async def get_by_id(self, id: str) -> Optional[ModelType]:
        """
        Retrieves a single record of the associated model by its unique identifier.

        :param id: The unique identifier of the record to retrieve.
        :type id: str

        :return: An instance of the model if found, or None if no record with the specified ID exists.
        :rtype: ModelType

        Example usage:
        ```
        # Retrieve a record by ID
        record_id = 1c417e73-3133-47a9-9aeb-cd0ef835f2e1
        result = await base_repo.get_by_id(record_id)
        if result:
            print(f"Record found: {result}")
        else:
            print("Record not found.")
        ```
        """
        return await self.model_class.get(id)

    async def get_all(
        self, skip: PositiveInt = 0, limit: PositiveInt = 100
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
        return (
            await self.model_class.find_all().skip(skip).limit(limit).to_list()
        )

    async def filter_by(self, **kwargs) -> list[ModelType]:
        return await self.model_class.find(kwargs).to_list()

    async def save(self, entity: ModelType) -> ModelType:
        """
        Saves (adds or updates) an entity.

        Args:
            entity: The entity object to save.

        Returns:
            The saved entity object.
        """
        await entity.save()
        return entity

    async def create(self, entity: ModelType) -> ModelType:
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
        await entity.insert()
        return entity

    async def update(self, id: str, update_data: dict) -> Optional[ModelType]:
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
        record_id = 1c417e73-3133-47a9-9aeb-cd0ef835f2e1
        existing_record = await base_repo.get_by_id(record_id)
        updated_record = await base_repo.update(existing_record, age=31, city='San Francisco')
        print(f"Record updated: {updated_record}")
        ```
        """
        obj = await self.get_by_id(id)
        if obj:
            await obj.update({"$set": update_data})
            return obj
        return None

    async def delete(self, entity: ModelType) -> None:
        """
        Deletes the specified model instance from the associated data storage.

        :param entity: The instance of the model to be deleted.
        :type entity: ModelType

        Example usage:
        ```
        # Retrieve a record by ID and delete it
        record_id = 1c417e73-3133-47a9-9aeb-cd0ef835f2e1
        existing_record = await base_repo.get_by_id(record_id)
        await base_repo.delete(existing_record)
        print("Record deleted.")
        ```
        """
        await entity.delete()

    async def delete_by_id(self, id: str) -> None:
        """
        Deletes a record of the associated model by its unique identifier.

        :param id: The unique identifier of the record to be deleted.
        :type id: PositiveInt

        Example usage:
        ```
        # Delete a record by ID
        record_id = 1c417e73-3133-47a9-9aeb-cd0ef835f2e1
        await base_repo.delete_by_id(record_id)
        print("Record deleted.")
        ```
        """
        entity = await self.model_class.get(id)
        if entity:
            await entity.delete()

    async def exists(self, id: str) -> bool:
        """
        Checks if a record with the specified unique identifier exists in the associated data storage.

        :param id: The unique identifier of the record to check for existence.
        :type id: PositiveInt

        :return: True if a record with the specified ID exists, False otherwise.
        :rtype: bool

        Example usage:
        ```
        # Check if a record with ID 1c417e73-3133-47a9-9aeb-cd0ef835f2e1 exists
        record_id = 1c417e73-3133-47a9-9aeb-cd0ef835f2e1
        if await base_repo.exists(record_id):
            print("Record exists.")
        else:
            print("Record does not exist.")
        ```
        """
        return await self.model_class.find_one({"_id": id}) is not None

    async def count(self) -> int:
        """
        Retrieves the total number of records in the associated data storage.

        :return: The count of records in the associated data storage.
        :rtype: PositiveInt

        Example usage:
        ```
        # Get the total count of records
        total_records = await base_repo.count()
        print(f"Total records: {total_records}")
        ```
        """
        return await self.model_class.find_all().count()

    async def bulk_create(self, entities: list[ModelType]) -> list[ModelType]:
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
        await self.model_class.insert_many(entities)
        return entities

    async def bulk_update(self, entities: list[ModelType]) -> list[ModelType]:
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
            await entity.save()
        return entities

    async def bulk_delete(self, entities: list[ModelType]) -> None:
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
            await entity.delete()
