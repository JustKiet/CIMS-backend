from typing import Optional, Any
import datetime

class Headhunter:
    def __init__(
        self,
        name: str,
        phone: str,
        email: str,
        hashed_password: str,
        role: str,
        area_id: int,
        headhunter_id: Optional[int] = None,
        created_at: Optional[datetime.datetime] = None,
        updated_at: Optional[datetime.datetime] = None
    ) -> None:
        self._headhunter_id = headhunter_id
        self._name = name.strip()
        self._phone = phone.strip()
        self._email = email.strip()
        self._hashed_password = hashed_password.strip()
        self._role = role.strip()
        self._area_id = area_id
        self._created_at = created_at if created_at else datetime.datetime.now(datetime.timezone.utc)
        self._updated_at = updated_at if updated_at else datetime.datetime.now(datetime.timezone.utc)

    @property
    def headhunter_id(self) -> Optional[int]:
        return self._headhunter_id
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def phone(self) -> str:
        return self._phone
    
    @property
    def email(self) -> str:
        return self._email
    
    @property
    def hashed_password(self) -> str:
        return self._hashed_password
    
    @property
    def role(self) -> str:
        return self._role
    
    @property
    def area_id(self) -> int:
        return self._area_id

    def to_dict(self) -> dict[str, Any]:
        return {
            "headhunter_id": self._headhunter_id,
            "name": self._name,
            "phone": self._phone,
            "email": self._email,
            "hashed_password": self._hashed_password,
            "role": self._role,
            "area_id": self._area_id,
            "created_at": self._created_at.isoformat() if self._created_at else None,
            "updated_at": self._updated_at.isoformat() if self._updated_at else None
        }
    
    def __repr__(self) -> str:
        return (
            f"Headhunter(headhunter_id={self._headhunter_id}, name={self._name}, "
            f"phone={self._phone}, email={self._email}, role={self._role}, "
            f"area_id={self._area_id}), created_at={self._created_at.isoformat() if self._created_at else None}, "
            f"updated_at={self._updated_at.isoformat() if self._updated_at else None})"
        )