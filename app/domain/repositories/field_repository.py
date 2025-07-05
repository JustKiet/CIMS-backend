from app.domain.entities.field import Field
from abc import ABC, abstractmethod
from typing import Optional

class FieldRepository(ABC):
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