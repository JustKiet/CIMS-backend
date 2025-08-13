import httpx
from cims.schemas import ErrorResponse

class FieldToolset:
    @staticmethod
    async def get_fields():
        """
        Retrieve all fields.

        :return: A list of all fields.
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    "http://backend:8000/api/v1/fields/",
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
                message=f"HTTP error retrieving fields: {str(e)}"
            )
        except Exception as e:
            return ErrorResponse(
                success=False,
                message=f"Error retrieving fields: {str(e)}"
            )