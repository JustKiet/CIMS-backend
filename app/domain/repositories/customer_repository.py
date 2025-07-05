from app.domain.entities.customer import Customer
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