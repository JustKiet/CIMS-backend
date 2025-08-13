import httpx
from cims.schemas import ErrorResponse

class CustomerToolset:
    @staticmethod
    async def get_customers(
        page: int = 1,
        page_size: int = 10,
    ):
        """
        Retrieve a paginated list of customers.

        :param int page: Page number for pagination.
        :param int page_size: Number of customers per page.
        :return: A paginated list of customers.
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    "http://backend:8000/api/v1/customers/",
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
                message=f"HTTP error retrieving customers: {str(e)}"
            )
        except Exception as e:
            return ErrorResponse(
                success=False,
                message=f"Error retrieving customers: {str(e)}"
            )
    
    @staticmethod
    async def get_customer(customer_id: int):
        """
        Retrieve a customer by their unique ID.

        :param int customer_id: The unique ID of the customer.
        :return: The details of the customer with the specified ID.
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"http://backend:8000/api/v1/customers/{customer_id}"
                )
                response.raise_for_status()
                return response.json()
        except httpx.HTTPError as e:
            return ErrorResponse(
                success=False,
                message=f"HTTP error retrieving customer: {str(e)}"
            )
        except Exception as e:
            return ErrorResponse(
                success=False,
                message=f"Error retrieving customer: {str(e)}"
            )
    
    @staticmethod
    async def search_customers(
        query: str,
        page: int = 1,
        page_size: int = 10,
    ):
        """
        Search for customers by name, email, company, or phone.

        :param str query: Search query to filter customers.
        :param int page: Page number for pagination.
        :param int page_size: Number of customers per page.
        :return: A paginated list of customers matching the search criteria.
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    "http://backend:8000/api/v1/customers/search",
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
                message=f"HTTP error searching customers: {str(e)}"
            )
        except Exception as e:
            return ErrorResponse(
                success=False,
                message=f"Error searching customers: {str(e)}"
            )