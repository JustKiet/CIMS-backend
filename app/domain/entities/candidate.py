from typing import Literal, Optional, Any, cast
import datetime

Gender = Literal["NAM", "NU", "KHAC"]

class Candidate:
    def __init__(
        self,
        name: str,
        phone: str,
        email: str,
        year_of_birth: int,
        gender: Gender,
        education: str,
        source: str,
        expertise_id: int,
        field_id: int,
        area_id: int,
        level_id: int,
        headhunter_id: int,
        note: Optional[str] = None,
        candidate_id: Optional[int] = None,
        created_at: Optional[datetime.datetime] = None,
        updated_at: Optional[datetime.datetime] = None
    ) -> None:
        self._candidate_id = candidate_id
        self._name = name.strip()
        self._phone = phone.strip()
        self._email = email.strip()
        self._year_of_birth = year_of_birth
        self._gender: Gender = gender
        self._education = education.strip()
        self._source = source.strip()
        self._expertise_id = expertise_id
        self._field_id = field_id
        self._area_id = area_id
        self._level_id = level_id
        self._headhunter_id = headhunter_id
        self._note = note.strip() if note else None
        self._created_at = created_at if created_at else datetime.datetime.now(datetime.timezone.utc)
        self._updated_at = updated_at if updated_at else datetime.datetime.now(datetime.timezone.utc)

    @staticmethod
    def validate_gender_value(value: str) -> Gender:
        if value not in Gender.__args__:
            raise ValueError(f"{value} is not a valid gender value. Must be one of 'Nam', 'Nu', or 'Khac'.")
        return cast(Gender, value)
    
    @property
    def candidate_id(self) -> Optional[int]:
        return self._candidate_id
    
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
    def year_of_birth(self) -> int:
        return self._year_of_birth
    
    @property
    def gender(self) -> Gender:
        return self._gender
    
    @property
    def education(self) -> str:
        return self._education
    
    @property
    def source(self) -> str:
        return self._source
    
    @property
    def expertise_id(self) -> int:
        return self._expertise_id
    
    @property
    def field_id(self) -> int:
        return self._field_id
    
    @property
    def area_id(self) -> int:
        return self._area_id
    
    @property
    def level_id(self) -> int:
        return self._level_id
    
    @property
    def headhunter_id(self) -> int:
        return self._headhunter_id
    
    @property
    def note(self) -> Optional[str]:
        return self._note
    
    @property
    def created_at(self) -> datetime.datetime:
        return self._created_at
    
    @property
    def updated_at(self) -> datetime.datetime:
        return self._updated_at

    def to_dict(self) -> dict[str, Any]:
        return {
            "candidate_id": str(self._candidate_id),
            "name": self._name,
            "phone": self._phone,
            "email": self._email,
            "year_of_birth": self._year_of_birth,
            "gender": self._gender,
            "education": self._education,
            "source": self._source,
            "expertise_id": self._expertise_id,
            "field_id": self._field_id,
            "area_id": self._area_id,
            "level_id": self._level_id,
            "headhunter_id": self._headhunter_id,
            "note": self._note,
            "created_at": self._created_at.isoformat(),
            "updated_at": self._updated_at.isoformat()
        }

    def __repr__(self) -> str:
        return (
            f"Candidate(candidate_id={self._candidate_id}, name={self._name}, "
            f"phone={self._phone}, email={self._email}, year_of_birth={self._year_of_birth}, "
            f"gender={self._gender}, education={self._education}, source={self._source}, "
            f"expertise_id={self._expertise_id}, field_id={self._field_id}, "
            f"area_id={self._area_id}, level_id={self._level_id}, headhunter_id={self._headhunter_id}, "
            f"note={self._note}, created_at={self._created_at}, updated_at={self._updated_at})"
        )