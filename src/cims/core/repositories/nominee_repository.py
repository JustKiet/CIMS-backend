from cims.core.entities.nominee import Nominee
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

    @abstractmethod
    def get_all_nominees(self, limit: int = 100, offset: int = 0) -> list[Nominee]:
        """
        Retrieve all nominees from the repository with pagination.

        :param int limit: The maximum number of nominees to return.
        :param int offset: The number of nominees to skip.
        :return: A list of nominee entities.
        :rtype: list[Nominee]
        """
        pass

    @abstractmethod
    def get_nominees_by_candidate_id(self, candidate_id: int, limit: int = 100, offset: int = 0) -> list[Nominee]:
        """
        Retrieve nominees by candidate ID.

        :param int candidate_id: The candidate ID to filter by.
        :param int limit: The maximum number of nominees to return.
        :param int offset: The number of nominees to skip.
        :return: A list of nominee entities.
        :rtype: list[Nominee]
        """
        pass

    @abstractmethod
    def get_nominees_by_project_id(self, project_id: int, limit: int = 100, offset: int = 0) -> list[Nominee]:
        """
        Retrieve nominees by project ID.

        :param int project_id: The project ID to filter by.
        :param int limit: The maximum number of nominees to return.
        :param int offset: The number of nominees to skip.
        :return: A list of nominee entities.
        :rtype: list[Nominee]
        """
        pass

    @abstractmethod
    def search_nominees_by_campaign(self, campaign_query: str, limit: int = 100, offset: int = 0) -> list[Nominee]:
        """
        Search nominees by campaign using a partial match.

        :param str campaign_query: The campaign query to search for.
        :param int limit: The maximum number of nominees to return.
        :param int offset: The number of nominees to skip.
        :return: A list of matching nominee entities.
        :rtype: list[Nominee]
        """
        pass

    @abstractmethod
    def search_nominees_by_status(self, status_query: str, limit: int = 100, offset: int = 0) -> list[Nominee]:
        """
        Search nominees by status.

        :param str status_query: The status to search for.
        :param int limit: The maximum number of nominees to return.
        :param int offset: The number of nominees to skip.
        :return: A list of matching nominee entities.
        :rtype: list[Nominee]
        """
        pass