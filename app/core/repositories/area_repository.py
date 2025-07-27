from app.core.entities.area import Area
from abc import ABC, abstractmethod
from typing import Optional

class AreaRepository(ABC):
    @abstractmethod
    def create_area(self, area: Area) -> Area:
        """
        Create a new area in the repository.

        :param Area area: The area entity to be created.
        :return: The created area entity.
        :rtype: Area
        """
        pass

    @abstractmethod
    def get_all_areas(self, limit: int = 100, offset: int = 0) -> list[Area]:
        """
        Retrieve all areas from the repository with pagination.

        :param int limit: The maximum number of areas to return.
        :param int offset: The number of areas to skip.
        :return: A list of Area entities.
        :rtype: list[Area]
        """
        pass

    @abstractmethod
    def search_areas_by_name(self, name_query: str, limit: int = 100, offset: int = 0) -> list[Area]:
        """
        Search areas by name using a partial match.

        :param str name_query: The name query to search for.
        :param int limit: The maximum number of areas to return.
        :param int offset: The number of areas to skip.
        :return: A list of matching area entities.
        :rtype: list[Area]
        """
        pass
    
    @abstractmethod
    def get_area_id_by_name(self, area_name: str) -> Optional[int]:
        """
        Retrieve the ID of an area by its name.

        :param str area_name: The name of the area to retrieve.
        :return: The ID of the area if found, otherwise None.
        :rtype: Optional[int]
        """
        pass
    
    @abstractmethod
    def get_area_by_id(self, area_id: int) -> Optional[Area]:
        """
        Retrieve an area by its ID.

        :param int area_id: The ID of the area to retrieve.
        :return: The area entity if found, otherwise None.
        :rtype: Optional[Area]
        """
        pass
    
    @abstractmethod
    def update_area(self, area: Area) -> Area:
        """
        Update an existing area in the repository.

        :param Area area: The area entity with updated information.
        :return: The updated area entity.
        :rtype: Area
        :raises NotFoundError: If the area with the given ID does not exist.
        """
        pass

    @abstractmethod
    def delete_area(self, area_id: int) -> bool:
        """
        Delete an area by its ID.

        :param int area_id: The ID of the area to delete.
        :return: True if the area was successfully deleted, False otherwise.
        :rtype: bool
        :raises NotFoundError: If the area with the given ID does not exist.
        """
        pass