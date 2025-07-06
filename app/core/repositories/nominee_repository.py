from app.core.entities.nominee import Nominee
from abc import ABC, abstractmethod
from typing import Optional

class NomineeRepository(ABC):
    @abstractmethod
    def create_nominee(self, nominee: Nominee) -> Nominee:
        """
        Create a new nominee in the repository.

        :param Nominee nominee: The nominee entity to be created.
        :return: The created nominee entity.
        :rtype: Nominee
        """
        pass
    
    @abstractmethod
    def get_nominee_by_id(self, nominee_id: int) -> Optional[Nominee]:
        """
        Retrieve a nominee by their ID.

        :param int nominee_id: The ID of the nominee to retrieve.
        :return: The nominee entity if found, otherwise None.
        :rtype: Optional[Nominee]
        """
        pass
    
    @abstractmethod
    def update_nominee(self, nominee: Nominee) -> Nominee:
        """
        Update an existing nominee in the repository.

        :param Nominee nominee: The nominee entity with updated information.
        :return: The updated nominee entity.
        :rtype: Nominee
        :raises NotFoundError: If the nominee with the given ID does not exist.
        """
        pass

    @abstractmethod
    def delete_nominee(self, nominee_id: int) -> bool:
        """
        Delete a nominee by their ID.

        :param int nominee_id: The ID of the nominee to delete.
        :return: True if the nominee was successfully deleted, False otherwise.
        :rtype: bool
        :raises NotFoundError: If the nominee with the given ID does not exist.
        """
        pass