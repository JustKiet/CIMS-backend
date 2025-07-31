from cims.core.entities.customer import Customer
from abc import ABC, abstractmethod
from typing import Optional

class CustomerRepository(ABC):
    @abstractmethod
    def create_customer(self, customer: Customer) -> Customer:
        """
        Create a new customer in the repository.

        :param Customer customer: The customer entity to be created.
        :return: The created customer entity.
        :rtype: Customer
        """
        pass

    @abstractmethod
    def get_customer_id_by_name(self, customer_name: str) -> Optional[int]:
        """
        Retrieve the ID of a customer by their name.

        :param str customer_name: The name of the customer to retrieve.
        :return: The ID of the customer if found, otherwise None.
        :rtype: Optional[int]
        """
        pass

    @abstractmethod
    def get_customers_by_ids(self, customer_ids: list[int]) -> list[Customer]:
        """
        Retrieve customers by their IDs.

        :param list[int] customer_ids: The list of customer IDs to retrieve.
        :return: A list of customer entities.
        :rtype: list[Customer]
        """
        pass
    
    @abstractmethod
    def get_customer_by_id(self, customer_id: int) -> Optional[Customer]:
        """
        Retrieve a customer by its ID.

        :param int customer_id: The ID of the customer to retrieve.
        :return: The customer entity if found, otherwise None.
        :rtype: Optional[Customer]
        """
        pass
    
    @abstractmethod
    def update_customer(self, customer: Customer) -> Customer:
        """
        Update an existing customer in the repository.

        :param Customer customer: The customer entity with updated information.
        :return: The updated customer entity.
        :rtype: Customer
        :raises NotFoundError: If the customer with the given ID does not exist.
        """
        pass

    @abstractmethod
    def delete_customer(self, customer_id: int) -> bool:
        """
        Delete a customer by its ID.

        :param int customer_id: The ID of the customer to delete.
        :return: True if the customer was successfully deleted, False otherwise.
        :rtype: bool
        :raises NotFoundError: If the customer with the given ID does not exist.
        """
        pass

    @abstractmethod
    def get_all_customers(self, limit: int = 100, offset: int = 0) -> list[Customer]:
        """
        Retrieve all customers from the repository with pagination.

        :param int limit: The maximum number of customers to return.
        :param int offset: The number of customers to skip.
        :return: A list of customer entities.
        :rtype: list[Customer]
        """
        pass

    @abstractmethod
    def search_customers_by_name(self, name_query: str, limit: int = 100, offset: int = 0) -> list[Customer]:
        """
        Search customers by name using a partial match.

        :param str name_query: The name query to search for.
        :param int limit: The maximum number of customers to return.
        :param int offset: The number of customers to skip.
        :return: A list of matching customer entities.
        :rtype: list[Customer]
        """
        pass