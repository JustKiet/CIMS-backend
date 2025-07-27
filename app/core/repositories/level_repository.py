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

    @abstractmethod
    def get_all_levels(self, limit: int = 100, offset: int = 0) -> list[Level]:
        """
        Retrieve all levels from the repository with pagination.

        :param int limit: The maximum number of levels to return.
        :param int offset: The number of levels to skip.
        :return: A list of level entities.
        :rtype: list[Level]
        """
        pass

    @abstractmethod
    def get_level_id_by_name(self, level_name: str) -> Optional[int]:
        """
        Retrieve the ID of a level by its name.

        :param str level_name: The name of the level to retrieve.
        :return: The ID of the level if found, otherwise None.
        :rtype: Optional[int]
        """
        pass

    @abstractmethod
    def search_levels_by_name(self, name_query: str, limit: int = 100, offset: int = 0) -> list[Level]:
        """
        Search levels by name using a partial match.

        :param str name_query: The name query to search for.
        :param int limit: The maximum number of levels to return.
        :param int offset: The number of levels to skip.
        :return: A list of matching level entities.
        :rtype: list[Level]
        """
        pass
