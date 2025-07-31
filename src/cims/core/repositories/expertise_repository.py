from cims.core.entities.expertise import Expertise
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
    def get_expertises_by_ids(self, expertise_ids: list[int]) -> list[Expertise]:
        """
        Retrieve expertises by their IDs.

        :param list[int] expertise_ids: The list of expertise IDs to retrieve.
        :return: A list of expertise entities.
        :rtype: list[Expertise]
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

    @abstractmethod
    def get_all_expertises(self, limit: int = 100, offset: int = 0) -> list[Expertise]:
        """
        Retrieve all expertises from the repository with pagination.

        :param int limit: The maximum number of expertises to return.
        :param int offset: The number of expertises to skip.
        :return: A list of expertise entities.
        :rtype: list[Expertise]
        """
        pass

    @abstractmethod
    def get_expertise_id_by_name(self, expertise_name: str) -> Optional[int]:
        """
        Retrieve the ID of an expertise by its name.

        :param str expertise_name: The name of the expertise to retrieve.
        :return: The ID of the expertise if found, otherwise None.
        :rtype: Optional[int]
        """
        pass

    @abstractmethod
    def search_expertises_by_name(self, name_query: str, limit: int = 100, offset: int = 0) -> list[Expertise]:
        """
        Search expertises by name using a partial match.

        :param str name_query: The name query to search for.
        :param int limit: The maximum number of expertises to return.
        :param int offset: The number of expertises to skip.
        :return: A list of matching expertise entities.
        :rtype: list[Expertise]
        """
        pass