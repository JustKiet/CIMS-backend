from typing import Optional, Any
import datetime

class Expertise:
    def __init__(
        self,
        name: str,
        expertise_id: Optional[int] = None,
        created_at: Optional[datetime.datetime] = None,
        updated_at: Optional[datetime.datetime] = None
    ) -> None:
        self._expertise_id = expertise_id
        self._name = name.strip()
        self._created_at = created_at if created_at else datetime.datetime.now(datetime.timezone.utc)
        self._updated_at = updated_at if updated_at else datetime.datetime.now(datetime.timezone.utc)

    @property
    def expertise_id(self) -> Optional[int]:
        return self._expertise_id
    
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
            "expertise_id": self._expertise_id,
            "name": self._name,
            "created_at": self._created_at,
            "updated_at": self._updated_at
        }
    
    def __repr__(self) -> str:
        return (
            f"Expertise(expertise_id={self._expertise_id}, name={self._name})"
        )