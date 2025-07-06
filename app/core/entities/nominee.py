from typing import Literal, Optional, Any, cast
import datetime

NomineeStatus = Literal[
    "DECU", 
    "PHONGVAN", 
    "THUONGLUONG", 
    "THUVIEC",
    "TUCHOI",
    "KYHOPDONG"
]

class Nominee:
    def __init__(
        self,
        campaign: str,
        status: NomineeStatus,
        years_of_experience: int,
        salary_expectation: float,
        notice_period: int,
        candidate_id: int,
        project_id: int,
        nominee_id: Optional[int] = None,
        created_at: Optional[datetime.datetime] = None,
        updated_at: Optional[datetime.datetime] = None
    ) -> None:
        self._nominee_id = nominee_id
        self._campaign = campaign.strip()
        self._status: NomineeStatus = status
        self._years_of_experience = years_of_experience
        self._salary_expectation = salary_expectation
        self._notice_period = notice_period
        self._candidate_id = candidate_id
        self._project_id = project_id
        self._created_at = created_at if created_at else datetime.datetime.now(datetime.timezone.utc)
        self._updated_at = updated_at if updated_at else datetime.datetime.now(datetime.timezone.utc)

    @staticmethod
    def validate_nominee_status(value: str) -> NomineeStatus:
        if value not in NomineeStatus.__args__:
            raise ValueError(f"{value} is not a valid nominee status. Must be one of 'DeCu', 'PhongVan', 'ThuongLuong', 'ThuViec', 'TuChoi', or 'KyHopDong'.")
        return cast(NomineeStatus, value)

    @property
    def nominee_id(self) -> Optional[int]:
        return self._nominee_id
    
    @property
    def campaign(self) -> str:
        return self._campaign
    
    @property
    def status(self) -> NomineeStatus:
        return self._status
    
    @property
    def years_of_experience(self) -> int:
        return self._years_of_experience
    
    @property
    def salary_expectation(self) -> float:
        return self._salary_expectation
    
    @property
    def notice_period(self) -> int:
        return self._notice_period
    
    @property
    def candidate_id(self) -> int:
        return self._candidate_id
    
    @property
    def project_id(self) -> int:
        return self._project_id

    def to_dict(self) -> dict[str, Any]:
        return {
            "nominee_id": self._nominee_id,
            "campaign": self._campaign,
            "status": self._status,
            "years_of_experience": self._years_of_experience,
            "salary_expectation": self._salary_expectation,
            "notice_period": self._notice_period,
            "candidate_id": self._candidate_id,
            "project_id": self._project_id
        }
    
    def __repr__(self) -> str:
        return (
            f"Nominee(nominee_id={self._nominee_id}, campaign={self._campaign}, "
            f"status={self._status}, years_of_experience={self._years_of_experience}, "
            f"salary_expectation={self._salary_expectation}, notice_period={self._notice_period}, "
            f"candidate_id={self._candidate_id}, project_id={self._project_id})"
        )