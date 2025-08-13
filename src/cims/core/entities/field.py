from typing import Optional, Any
import datetime

class Field:
    def __init__(
        self,
        name: str,
        field_id: Optional[int] = None,
        created_at: Optional[datetime.datetime] = None,
        updated_at: Optional[datetime.datetime] = None
    ) -> None:
        self._field_id = field_id
        self._name = name.strip()
        self._created_at = created_at if created_at else datetime.datetime.now(datetime.timezone.utc)
        self._updated_at = updated_at if updated_at else datetime.datetime.now(datetime.timezone.utc)

    @property
    def field_id(self) -> Optional[int]:
        return self._field_id
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def created_at(self) -> datetime.datetime:
        return self._created_at
    
    @property
    def updated_at(self) -> datetime.datetime:
        return self._updated_at

    def to_dict(self) -> dict[str, Any]:
        return {
            "field_id": self._field_id,
            "name": self._name,
            "created_at": self._created_at,
            "updated_at": self._updated_at
        }
    
    def __repr__(self) -> str:
        return (
            f"Field(field_id={self._field_id}, name={self._name})"
        )