import httpx
from cims.schemas import ErrorResponse

class AreaToolset:
    @staticmethod
    async def get_areas():
        """
        Retrieve all areas.

        :return: A list of all areas.
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    "http://backend:8000/api/v1/areas/",
                    params={
                        "page": 1,
                        "page_size": 100,
                    }
                )
                response.raise_for_status()
                return response.json()
        except httpx.HTTPError as e:
            return ErrorResponse(
                success=False,
                message=f"HTTP error retrieving areas: {str(e)}"
            )
        except Exception as e:
            return ErrorResponse(
                success=False,
                message=f"Error retrieving areas: {str(e)}"
            )