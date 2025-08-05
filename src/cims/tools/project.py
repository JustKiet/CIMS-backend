import httpx
from cims.schemas import ErrorResponse

class ProjectToolset:
    @staticmethod
    async def get_projects(
        page: int = 1,
        page_size: int = 10,
    ):
        """
        Retrieve a paginated list of projects.
        
        :param int page: Page number for pagination.
        :param int page_size: Number of projects per page.
        :return: A paginated list of projects.
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    "http://backend:8000/api/v1/projects/",
                    params={
                        "page": page,
                        "page_size": page_size,
                    }
                )
                response.raise_for_status()
                return response.json()
        except httpx.HTTPError as e:
            return ErrorResponse(
                success=False,
                message=f"HTTP error retrieving projects: {str(e)}"
            )
        except Exception as e:
            return ErrorResponse(
                success=False,
                message=f"Error retrieving projects: {str(e)}"
            )

    @staticmethod
    async def get_project(project_id: int):
        """
        Retrieve a project by its unique ID.

        :param int project_id: The unique ID of the project.
        :return: The details of the project with the specified ID.
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"http://backend:8000/api/v1/projects/{project_id}"
                )
                response.raise_for_status()
                return response.json()
        except httpx.HTTPError as e:
            return ErrorResponse(
                success=False,
                message=f"HTTP error retrieving project: {str(e)}"
            )
        except Exception as e:
            return ErrorResponse(
                success=False,
                message=f"Error retrieving project: {str(e)}"
            )
    
    @staticmethod
    async def search_projects(
        query: str,
        page: int = 1,
        page_size: int = 10,
    ):
        """
        Search for projects by name or description.

        :param str query: Search query to filter projects.
        :param int page: Page number for pagination.
        :param int page_size: Number of projects per page.
        :return: A paginated list of projects matching the search criteria.
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    "http://backend:8000/api/v1/projects/search",
                    params={
                        "query": query,
                        "page": page,
                        "page_size": page_size,
                    }
                )
                response.raise_for_status()
                return response.json()
        except httpx.HTTPError as e:
            return ErrorResponse(
                success=False,
                message=f"HTTP error searching projects: {str(e)}"
            )
        except Exception as e:
            return ErrorResponse(
                success=False,
                message=f"Error searching projects: {str(e)}"
            )