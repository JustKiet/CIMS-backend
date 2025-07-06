from app.core.entities.headhunter import Headhunter
from abc import ABC, abstractmethod
from typing import Optional

class HeadhunterRepository(ABC):
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