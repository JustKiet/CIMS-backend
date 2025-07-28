from cims.core.entities.project import Project
from abc import ABC, abstractmethod
from typing import Optional

class ProjectRepository(ABC):
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