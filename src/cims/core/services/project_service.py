from cims.core.entities.project import Project
from abc import ABC, abstractmethod
from typing import Optional

class ProjectService(ABC):
    @abstractmethod
    def create_project(self, project: Project) -> Project:
        """
        Create a new project in the repository.

        :param Project project: The project entity to be created.
        :return: The created project entity.
        :rtype: Project
        """
        pass

    @abstractmethod
    def get_projects_by_ids(self, project_ids: list[int]) -> list[Project]:
        """
        Retrieve projects by their IDs.

        :param list[int] project_ids: The list of project IDs to retrieve.
        :return: A list of project entities.
        :rtype: list[Project]
        """
        pass
    
    @abstractmethod
    def get_project_by_id(self, project_id: int) -> Optional[Project]:
        """
        Retrieve a project by its ID.

        :param int project_id: The ID of the project to retrieve.
        :return: The project entity if found, otherwise None.
        :rtype: Optional[Project]
        """
        pass
    
    @abstractmethod
    def update_project(self, project: Project) -> Project:
        """
        Update an existing project in the repository.

        :param Project project: The project entity with updated information.
        :return: The updated project entity.
        :rtype: Project
        :raises NotFoundError: If the project with the given ID does not exist.
        """
        pass

    @abstractmethod
    def delete_project(self, project_id: int) -> bool:
        """
        Delete a project by its ID.

        :param int project_id: The ID of the project to delete.
        :return: True if the project was successfully deleted, False otherwise.
        :rtype: bool
        :raises NotFoundError: If the project with the given ID does not exist.
        """
        pass

    @abstractmethod
    def get_all_projects(self, limit: int = 100, offset: int = 0) -> list[Project]:
        """
        Retrieve all projects from the repository with pagination.

        :param int limit: The maximum number of projects to return.
        :param int offset: The number of projects to skip.
        :return: A list of project entities.
        :rtype: list[Project]
        """
        pass

    @abstractmethod
    def search_projects_by_name(self, name_query: str, limit: int = 100, offset: int = 0) -> list[Project]:
        """
        Search projects by name using a partial match.

        :param str name_query: The name query to search for.
        :param int limit: The maximum number of projects to return.
        :param int offset: The number of projects to skip.
        :return: A list of matching project entities.
        :rtype: list[Project]
        """
        pass

    @abstractmethod
    def search_projects_comprehensive(self, query: str, limit: int = 100, offset: int = 0) -> list[Project]:
        """
        Search projects by name, customer name, or expertise name using a partial match.

        :param str query: The search query to match against project name, customer name, or expertise name.
        :param int limit: The maximum number of projects to return.
        :param int offset: The number of projects to skip.
        :return: A list of matching project entities.
        :rtype: list[Project]
        """
        pass

    @abstractmethod
    def count_all_projects(self) -> int:
        """
        Count the total number of projects in the repository.

        :return: Total count of projects.
        :rtype: int
        """
        pass

    @abstractmethod
    def count_projects_comprehensive(self, query: str) -> int:
        """
        Count projects matching the comprehensive search query.

        :param str query: The search query to match against project name, customer name, or expertise name.
        :return: Count of matching projects.
        :rtype: int
        """
        pass

    @abstractmethod
    def get_projects_by_customer_id(self, customer_id: int, limit: int = 100, offset: int = 0) -> list[Project]:
        """
        Retrieve all projects for a specific customer with pagination.

        :param int customer_id: The customer ID to filter projects by.
        :param int limit: The maximum number of projects to return.
        :param int offset: The number of projects to skip.
        :return: A list of project entities for the customer.
        :rtype: list[Project]
        """
        pass

    @abstractmethod
    def count_projects_by_customer_id(self, customer_id: int) -> int:
        """
        Count total projects for a specific customer.

        :param int customer_id: The customer ID to count projects for.
        :return: Count of projects for the customer.
        :rtype: int
        """
        pass