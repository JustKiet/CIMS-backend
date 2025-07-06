from typing import Optional, Any
import datetime

class Customer:
    def __init__(
        self,
        name: str,
        field_id: int,
        customer_id: Optional[int] = None,
        created_at: Optional[datetime.datetime] = None,
        updated_at: Optional[datetime.datetime] = None
    ) -> None:
        self._customer_id = customer_id
        self._name = name.strip()
        self._field_id = field_id
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

    def to_dict(self) -> dict[str, Any]:
        return {
            "customer_id": self._customer_id,
            "name": self._name,
            "field_id": self._field_id
        }
    
    def __repr__(self) -> str:
        return (
            f"Customer(customer_id={self._customer_id}, name={self._name}, "
            f"field_id={self._field_id})"
        )