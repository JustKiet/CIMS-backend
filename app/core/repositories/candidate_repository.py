from app.core.entities.candidate import Candidate
from abc import ABC, abstractmethod
from typing import Optional

class CandidateRepository(ABC):
    @abstractmethod
    def create_candidate(self, candidate: Candidate) -> Candidate:
        """
        Create a new candidate in the repository.

        :param Candidate candidate: The candidate entity to be created.
        :return: The created candidate entity.
        :rtype: Candidate
        """
        pass

    @abstractmethod
    def get_all_candidates(self, limit: int = 100, offset: int = 0) -> list[Candidate]:
        """
        Retrieve all candidates from the repository with pagination.

        :param int limit: The maximum number of candidates to return.
        :param int offset: The number of candidates to skip.
        :return: A list of candidate entities.
        :rtype: list[Candidate]
        """
        pass

    @abstractmethod
    def get_candidate_id_by_name(self, candidate_name: str) -> Optional[int]:
        """
        Retrieve the ID of a candidate by their name.

        :param str candidate_name: The name of the candidate to retrieve.
        :return: The ID of the candidate if found, otherwise None.
        :rtype: Optional[int]
        """
        pass

    @abstractmethod
    def search_candidates_by_name(self, name_query: str, limit: int = 100, offset: int = 0) -> list[Candidate]:
        """
        Search candidates by name using a partial match.

        :param str name_query: The name query to search for.
        :param int limit: The maximum number of candidates to return.
        :param int offset: The number of candidates to skip.
        :return: A list of matching candidate entities.
        :rtype: list[Candidate]
        """
        pass
    
    @abstractmethod
    def get_candidate_by_id(self, candidate_id: int) -> Optional[Candidate]:
        """
        Retrieve a candidate by their ID.

        :param int candidate_id: The ID of the candidate to retrieve.
        :return: The candidate entity if found, otherwise None.
        :rtype: Optional[Candidate]
        """
        pass
    
    @abstractmethod
    def update_candidate(self, candidate: Candidate) -> Candidate:
        """
        Update an existing candidate in the repository.

        :param Candidate candidate: The candidate entity with updated information.
        :return: The updated candidate entity.
        :rtype: Candidate
        :raises NotFoundError: If the candidate with the given ID does not exist.
        """
        pass

    @abstractmethod
    def delete_candidate(self, candidate_id: int) -> bool:
        """
        Delete a candidate by their ID.

        :param int candidate_id: The ID of the candidate to delete.
        :return: True if the candidate was successfully deleted, False otherwise.
        :rtype: bool
        :raises NotFoundError: If the candidate with the given ID does not exist.
        """
        pass