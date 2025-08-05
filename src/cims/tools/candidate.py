import httpx
from cims.config import settings
from cims.schemas import (
    ErrorResponse,
)
from typing import Optional

class CandidateToolset:
    @staticmethod
    async def get_candidates(
        page: int = 1,
        page_size: int = 10,
    ):
        """
        Retrieve a paginated list of candidates with optional search query.

        :param int page: Page number for pagination.
        :param int page_size: Number of candidates per page.
        :return: A paginated list of candidates matching the criteria.
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"http://backend:8000/api/v1/candidates/",
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
                message=f"HTTP error retrieving candidates: {str(e)}"
            )
        except Exception as e:
            return ErrorResponse(
                success=False,
                message=f"Error retrieving candidates: {str(e)}"
            )

    @staticmethod
    async def get_candidate(candidate_id: int):
        """
        Retrieve a candidate by their unique ID.

        :param int candidate_id: The unique ID of the candidate.
        :return: The details of the candidate with the specified ID.
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"http://backend:8000/api/v1/candidates/{candidate_id}"
                )
                response.raise_for_status()
                return response.json()
        except httpx.HTTPError as e:
            return ErrorResponse(
                success=False,
                message=f"HTTP error retrieving candidate: {str(e)}"
            )
        except Exception as e:
            return ErrorResponse(
                success=False,
                message=f"Error retrieving candidate: {str(e)}"
            )
    
    @staticmethod
    async def search_candidates(
        query: str,
        expertise_id: Optional[int] = None,
        field_id: Optional[int] = None,
        area_id: Optional[int] = None,
        level_id: Optional[int] = None,
        headhunter_id: Optional[int] = None, 
        page: int = 1, 
        page_size: int = 10
    ):
        """
        Search for candidates by name or email with pagination.

        :param str query: Search query to filter candidates by name or email.
        :param Optional[int] expertise_id: Filter by expertise ID.
        :param Optional[int] field_id: Filter by field ID.
        :param Optional[int] area_id: Filter by area ID.
        :param Optional[int] level_id: Filter by level ID.
        :param Optional[int] headhunter_id: Filter by headhunter ID.
        :param int page: Page number for pagination.
        :param int page_size: Number of candidates per page.
        :return: A paginated list of candidates matching the search criteria.
        """
        try:
            params = {
                "query": query,
                "page": page,
                "page_size": page_size,
            }
            
            # Add optional filters if provided
            if expertise_id is not None:
                params["expertise_id"] = expertise_id
            if field_id is not None:
                params["field_id"] = field_id
            if area_id is not None:
                params["area_id"] = area_id
            if level_id is not None:
                params["level_id"] = level_id
            if headhunter_id is not None:
                params["headhunter_id"] = headhunter_id
            
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"http://backend:8000/api/v1/candidates/search",
                    params=params
                )
                response.raise_for_status()
                return response.json()
        except httpx.HTTPError as e:
            return await CandidateToolset._get_error_with_available_options(
                f"HTTP error searching candidates: {str(e)}"
            )
        except Exception as e:
            return await CandidateToolset._get_error_with_available_options(
                f"Error searching candidates: {str(e)}"
            )
    
    @staticmethod
    async def _get_error_with_available_options(error_message: str):
        """
        Helper method to get available options for error messages.
        """
        try:
            async with httpx.AsyncClient() as client:
                # Get available expertises
                expertise_response = await client.get("http://backend:8000/api/v1/expertises/")
                expertises = expertise_response.json().get("expertises", []) if expertise_response.status_code == 200 else []
                
                # Get available fields
                field_response = await client.get("http://backend:8000/api/v1/fields/")
                fields = field_response.json().get("fields", []) if field_response.status_code == 200 else []
                
                # Get available areas
                area_response = await client.get("http://backend:8000/api/v1/areas/")
                areas = area_response.json().get("areas", []) if area_response.status_code == 200 else []
                
                # Get available levels
                level_response = await client.get("http://backend:8000/api/v1/levels/")
                levels = level_response.json().get("levels", []) if level_response.status_code == 200 else []
                
                # Get available headhunters
                headhunter_response = await client.get("http://backend:8000/api/v1/headhunters/")
                headhunters = headhunter_response.json().get("headhunters", []) if headhunter_response.status_code == 200 else []

                message = f"""
                {error_message}

                Please ensure all required fields are provided and valid.
                Available expertises and their IDs:
                {', '.join([f"{exp.get('name', 'Unknown')} (ID: {exp.get('expertise_id', 'Unknown')})" for exp in expertises]) if expertises else 'No expertises available'}

                Available fields and their IDs:
                {', '.join([f"{fld.get('name', 'Unknown')} (ID: {fld.get('field_id', 'Unknown')})" for fld in fields]) if fields else 'No fields available'}

                Available areas and their IDs:
                {', '.join([f"{area.get('name', 'Unknown')} (ID: {area.get('area_id', 'Unknown')})" for area in areas]) if areas else 'No areas available'}

                Available levels and their IDs:
                {', '.join([f"{lvl.get('name', 'Unknown')} (ID: {lvl.get('level_id', 'Unknown')})" for lvl in levels]) if levels else 'No levels available'}

                Available headhunters and their IDs:
                {', '.join([f"{hh.get('name', 'Unknown')} (ID: {hh.get('headhunter_id', 'Unknown')})" for hh in headhunters]) if headhunters else 'No headhunters available'}
                """

                return ErrorResponse(
                    success=False,
                    message=message
                )
        except Exception:
            return ErrorResponse(
                success=False,
                message=error_message
            )