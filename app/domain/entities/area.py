from typing import Optional, Any
import datetime

class Area:
    def __init__(
        self,
        name: str,
        area_id: Optional[int] = None,
        created_at: Optional[datetime.datetime] = None,
        updated_at: Optional[datetime.datetime] = None
    ) -> None:
        self._area_id = area_id
        self._name = name.strip()
        self._created_at = created_at if created_at else datetime.datetime.now(datetime.timezone.utc)
        self._updated_at = updated_at if updated_at else datetime.datetime.now(datetime.timezone.utc)

    @property
    def area_id(self) -> Optional[int]:
        return self._area_id
    
    @property
    def name(self) -> str:
        return self._name

    def to_dict(self) -> dict[str, Any]:
        return {
            "area_id": self._area_id,
            "name": self._name
        }
    
    def __repr__(self) -> str:
        return (
            f"Area(area_id={self._area_id}, name={self._name})"
        )