import httpx
from cims.schemas import ErrorResponse

class LevelToolset:
    @staticmethod
    async def get_levels():
        """
        Retrieve all levels.

        :return: A list of all levels.
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    "http://backend:8000/api/v1/levels/",
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
                message=f"HTTP error retrieving levels: {str(e)}"
            )
        except Exception as e:
            return ErrorResponse(
                success=False,
                message=f"Error retrieving levels: {str(e)}"
            )