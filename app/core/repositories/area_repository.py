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