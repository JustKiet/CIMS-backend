import httpx
from cims.schemas import ErrorResponse

class ExpertiseToolset:
    @staticmethod
    async def get_expertises():
        """
        Retrieve all expertises.

        :return: A list of all expertises.
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    "http://backend:8000/api/v1/expertises/",
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
                message=f"HTTP error retrieving expertises: {str(e)}"
            )
        except Exception as e:
            return ErrorResponse(
                success=False,
                message=f"Error retrieving expertises: {str(e)}"
            )