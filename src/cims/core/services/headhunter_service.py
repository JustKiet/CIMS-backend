from cims.core.entities.headhunter import Headhunter
from abc import ABC, abstractmethod
from typing import Optional

class HeadhunterService(ABC):
    @abstractmethod
    def create_headhunter(self, headhunter: Headhunter) -> Headhunter:
        """
        Create a new Headhunter in the repository.

        :param Headhunter headhunter: The Headhunter entity to be created.
        :return: The created Headhunter entity.
        :rtype: Headhunter
        """
        pass

    @abstractmethod
    def count_all_headhunters(self) -> int:
        """
        Count the total number of headhunters in the repository.

        :return: The total number of headhunters.
        :rtype: int
        """
        pass

    @abstractmethod
    def get_headhunters_by_ids(self, headhunter_ids: list[int]) -> list[Headhunter]:
        """
        Retrieve headhunters by their IDs.

        :param list[int] headhunter_ids: A list of headhunter IDs to retrieve.
        :return: A list of Headhunter entities corresponding to the provided IDs.
        :rtype: list[Headhunter]
        """
        pass
    
    @abstractmethod
    def get_headhunter_by_id(self, headhunter_id: int) -> Optional[Headhunter]:
        """
        Retrieve a Headhunter by their ID.

        :param int headhunter_id: The ID of the Headhunter to retrieve.
        :return: The Headhunter entity if found, otherwise None.
        :rtype: Optional[Headhunter]
        """
        pass

    @abstractmethod
    def get_headhunter_by_email(self, email: str) -> Optional[Headhunter]:
        """
        Retrieve a Headhunter by their email.

        :param str email: The email of the Headhunter to retrieve.
        :return: The Headhunter entity if found, otherwise None.
        :rtype: Optional[Headhunter]
        """
        pass
    
    @abstractmethod
    def update_headhunter(self, headhunter: Headhunter) -> Headhunter:
        """
        Update a existing Headhunter in the repository.

        :param Headhunter headhunter: The Headhunter entity with updated information.
        :return: The updated Headhunter entity.
        :rtype: Headhunter
        :raises NotFoundError: If the Headhunter with the given ID does not exist.
        """
        pass

    @abstractmethod
    def delete_headhunter(self, headhunter_id: int) -> bool:
        """
        Delete a Headhunter by their ID.

        :param int headhunter_id: The ID of the Headhunter to delete.
        :return: True if the Headhunter was successfully deleted, False otherwise.
        :rtype: bool
        :raises NotFoundError: If the Headhunter with the given ID does not exist.
        """
        pass

    @abstractmethod
    def get_all_headhunters(self, limit: int = 100, offset: int = 0) -> list[Headhunter]:
        """
        Retrieve all headhunters from the repository with pagination.

        :param int limit: The maximum number of headhunters to return.
        :param int offset: The number of headhunters to skip.
        :return: A list of headhunter entities.
        :rtype: list[Headhunter]
        """
        pass

    @abstractmethod
    def search_headhunters_by_name(self, name_query: str, limit: int = 100, offset: int = 0) -> list[Headhunter]:
        """
        Search headhunters by name using a partial match.

        :param str name_query: The name query to search for.
        :param int limit: The maximum number of headhunters to return.
        :param int offset: The number of headhunters to skip.
        :return: A list of matching headhunter entities.
        :rtype: list[Headhunter]
        """
        pass