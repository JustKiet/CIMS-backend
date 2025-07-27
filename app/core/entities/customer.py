from typing import Optional, Any
import datetime

class Customer:
    def __init__(
        self,
        name: str,
        field_id: int,
        representative_name: str,
        representative_phone: str,
        representative_email: str,
        representative_role: str,
        customer_id: Optional[int] = None,
        created_at: Optional[datetime.datetime] = None,
        updated_at: Optional[datetime.datetime] = None
    ) -> None:
        self._customer_id = customer_id
        self._name = name.strip()
        self._field_id = field_id
        self._representative_name = representative_name.strip()
        self._representative_phone = representative_phone.strip()
        self._representative_email = representative_email.strip()
        self._representative_role = representative_role.strip()
        self._created_at = created_at if created_at else datetime.datetime.now(datetime.timezone.utc)
        self._updated_at = updated_at if updated_at else datetime.datetime.now(datetime.timezone.utc)

    @property
    def customer_id(self) -> Optional[int]:
        return self._customer_id
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def field_id(self) -> int:
        return self._field_id
    
    @property
    def representative_name(self) -> str:
        return self._representative_name
    
    @property
    def representative_phone(self) -> str:
        return self._representative_phone
    
    @property
    def representative_email(self) -> str:
        return self._representative_email
    
    @property
    def representative_role(self) -> str:
        return self._representative_role
    
    @property
    def created_at(self) -> datetime.datetime:
        return self._created_at
    
    @property
    def updated_at(self) -> datetime.datetime:
        return self._updated_at

    def to_dict(self) -> dict[str, Any]:
        """Convert entity to dictionary for database storage."""
        return {
            "customer_id": self._customer_id,
            "name": self._name,
            "field_id": self._field_id,
            "representative_name": self._representative_name,
            "representative_phone": self._representative_phone,
            "representative_email": self._representative_email,
            "representative_role": self._representative_role,
            "created_at": self._created_at,
            "updated_at": self._updated_at
        }
    
    def __repr__(self) -> str:
        return (
            f"Customer(customer_id={self._customer_id}, name={self._name}, "
            f"field_id={self._field_id})"
        )