from cims.core.entities.field import Field
from abc import ABC, abstractmethod
from typing import Optional

class FieldService(ABC):
    @abstractmethod
    def create_field(self, field: Field) -> Field:
        """
        Create a new field in the repository.

        :param Field field: The field entity to be created.
        :return: The created field entity.
        :rtype: Field
        """
        pass

    @abstractmethod
    def get_field_id_by_name(self, field_name: str) -> Optional[int]:
        """
        Retrieve the ID of a field by its name.

        :param str field_name: The name of the field to retrieve.
        :return: The ID of the field if found, otherwise None.
        :rtype: Optional[int]
        """
        pass

    @abstractmethod
    def get_fields_by_ids(self, field_ids: list[int]) -> list[Field]:
        """
        Retrieve fields by their IDs.

        :param list[int] field_ids: A list of field IDs to retrieve.
        :return: A list of Field entities corresponding to the provided IDs.
        :rtype: list[Field]
        """
        pass
    
    @abstractmethod
    def get_field_by_id(self, field_id: int) -> Optional[Field]:
        """
        Retrieve a field by its ID.

        :param int field_id: The ID of the field to retrieve.
        :return: The field entity if found, otherwise None.
        :rtype: Optional[Field]
        """
        pass
    
    @abstractmethod
    def update_field(self, field: Field) -> Field:
        """
        Update an existing field in the repository.

        :param Field field: The field entity with updated information.
        :return: The updated field entity.
        :rtype: Field
        :raises NotFoundError: If the field with the given ID does not exist.
        """
        pass

    @abstractmethod
    def delete_field(self, field_id: int) -> bool:
        """
        Delete a field by its ID.

        :param int field_id: The ID of the field to delete.
        :return: True if the field was successfully deleted, False otherwise.
        :rtype: bool
        :raises NotFoundError: If the field with the given ID does not exist.
        """
        pass

    @abstractmethod
    def get_all_fields(self, limit: int = 100, offset: int = 0) -> list[Field]:
        """
        Retrieve all fields from the repository with pagination.

        :param int limit: The maximum number of fields to return.
        :param int offset: The number of fields to skip.
        :return: A list of field entities.
        :rtype: list[Field]
        """
        pass

    @abstractmethod
    def search_fields_by_name(self, name_query: str, limit: int = 100, offset: int = 0) -> list[Field]:
        """
        Search fields by name using a partial match.

        :param str name_query: The name query to search for.
        :param int limit: The maximum number of fields to return.
        :param int offset: The number of fields to skip.
        :return: A list of matching field entities.
        :rtype: list[Field]
        """
        pass