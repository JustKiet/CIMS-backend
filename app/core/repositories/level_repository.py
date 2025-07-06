from app.core.entities.level import Level
from abc import ABC, abstractmethod
from typing import Optional

class LevelRepository(ABC):
    @abstractmethod
    def create_level(self, level: Level) -> Level:
        """
        Create a new level in the repository.

        :param Level level: The level entity to be created.
        :return: The created level entity.
        :rtype: Level
        """
        pass
    
    @abstractmethod
    def get_level_by_id(self, level_id: int) -> Optional[Level]:
        """
        Retrieve a level by its ID.

        :param int level_id: The ID of the level to retrieve.
        :return: The level entity if found, otherwise None.
        :rtype: Optional[Level]
        """
        pass
    
    @abstractmethod
    def update_level(self, level: Level) -> Level:
        """
        Update an existing level in the repository.

        :param Level level: The level entity with updated information.
        :return: The updated level entity.
        :rtype: Level
        :raises NotFoundError: If the level with the given ID does not exist.
        """
        pass

    @abstractmethod
    def delete_level(self, level_id: int) -> bool:
        """
        Delete a level by its ID.

        :param int level_id: The ID of the level to delete.
        :return: True if the level was successfully deleted, False otherwise.
        :rtype: bool
        :raises NotFoundError: If the level with the given ID does not exist.
        """
        pass
