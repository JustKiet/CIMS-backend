from app.domain.entities.customer import Customer
from app.domain.repositories.customer_repository import CustomerRepository
from app.domain.exceptions import NotFoundError
from app.infrastructure.database.models import CustomerDB
from sqlalchemy.orm import Session
from typing import Optional

class SQLAlchemyCustomerRepository(CustomerRepository):
    def __init__(self, db_session: Session) -> None:
        self.db_session = db_session

    def _to_domain_entity(self, db_obj: CustomerDB) -> Customer:
        return Customer(
            customer_id=db_obj.customer_id,
            name=db_obj.name,
            field_id=db_obj.field_id,
            created_at=db_obj.created_at,
            updated_at=db_obj.updated_at
        )

    def create_customer(self, customer: Customer) -> Customer:
        new_customer = CustomerDB(**customer.to_dict())
        self.db_session.add(new_customer)
        self.db_session.commit()
        self.db_session.refresh(new_customer)
        return self._to_domain_entity(new_customer)

    def get_customer_by_id(self, customer_id: int) -> Optional[Customer]:
        if not customer_id:
            raise ValueError("Customer ID must be provided.")
        
        db_obj = self.db_session.get(CustomerDB, customer_id)
        if not db_obj:
            return None
        return self._to_domain_entity(db_obj)

    def update_customer(self, customer: Customer) -> Customer:
        if not customer.customer_id:
            raise ValueError("Customer ID must be provided for update.")
        
        db_obj = self.db_session.get(CustomerDB, customer.customer_id)
        if not db_obj:
            raise NotFoundError(entity="Customer", identifier=customer.customer_id)
        
        for key, value in customer.to_dict().items():
            setattr(db_obj, key, value)

        self.db_session.commit()
        self.db_session.refresh(db_obj)
        return self._to_domain_entity(db_obj)

    def delete_customer(self, customer_id: int) -> bool:
        if not customer_id:
            raise ValueError("Customer ID must be provided for deletion.")
        
        db_obj = self.db_session.get(CustomerDB, customer_id)
        if not db_obj:
            raise NotFoundError(entity="Customer", identifier=customer_id)

        self.db_session.delete(db_obj)
        self.db_session.commit()
        return True