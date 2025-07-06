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