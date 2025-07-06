from app.core.entities.expertise import Expertise
from abc import ABC, abstractmethod
from typing import Optional

class ExpertiseRepository(ABC):
    @abstractmethod
    def create_expertise(self, expertise: Expertise) -> Expertise:
        """
        Create a new expertise in the repository.

        :param Expertise expertise: The expertise entity to be created.
        :return: The created expertise entity.
        :rtype: Expertise
        """
        pass
    
    @abstractmethod
    def get_expertise_by_id(self, expertise_id: int) -> Optional[Expertise]:
        """
        Retrieve an expertise by its ID.

        :param int expertise_id: The ID of the expertise to retrieve.
        :return: The expertise entity if found, otherwise None.
        :rtype: Optional[Expertise]
        """
        pass
    
    @abstractmethod
    def update_expertise(self, expertise: Expertise) -> Expertise:
        """
        Update an existing expertise in the repository.

        :param Expertise expertise: The expertise entity with updated information.
        :return: The updated expertise entity.
        :rtype: Expertise
        :raises NotFoundError: If the expertise with the given ID does not exist.
        """
        pass

    @abstractmethod
    def delete_expertise(self, expertise_id: int) -> bool:
        """
        Delete an expertise by its ID.

        :param int expertise_id: The ID of the expertise to delete.
        :return: True if the expertise was successfully deleted, False otherwise.
        :rtype: bool
        :raises NotFoundError: If the expertise with the given ID does not exist.
        """
        pass