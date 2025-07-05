from typing import Literal, Optional, Any, cast
import datetime

ProjectType = Literal["CODINH", "THOIVU"]
ProjectStatus = Literal[
    "TIMKIEMUNGVIEN", 
    "UNGVIENPHONGVAN", 
    "UNGVIENTHUVIEC",
    "TAMNGUNG", 
    "HUY",
    "HOANTHANH"
]

class Project:
    def __init__(
        self,
        name: str,
        start_date: datetime.date,
        end_date: datetime.date,
        budget: float,
        budget_currency: str,
        type: ProjectType,
        required_recruits: int,
        recruited: int,
        status: ProjectStatus,
        customer_id: int,
        expertise_id: int,
        area_id: int,
        level_id: int,
        project_id: Optional[int] = None,
        created_at: Optional[datetime.datetime] = None,
        updated_at: Optional[datetime.datetime] = None
    ) -> None:
        self._project_id = project_id
        self._name = name.strip()
        self._start_date = start_date
        self._end_date = end_date
        self._budget = budget
        self._budget_currency = budget_currency.strip()
        self._type: ProjectType = type
        self._required_recruits = required_recruits
        self._recruited = recruited
        self._status: ProjectStatus = status
        self._customer_id = customer_id
        self._expertise_id = expertise_id
        self._area_id = area_id
        self._level_id = level_id
        self._created_at = created_at if created_at else datetime.datetime.now(datetime.timezone.utc)
        self._updated_at = updated_at if updated_at else datetime.datetime.now(datetime.timezone.utc)

    @staticmethod
    def validate_project_type(value: str) -> ProjectType:
        if value not in ProjectType.__args__:
            raise ValueError(f"{value} is not a valid project type. Must be one of 'CoDinh' or 'ThoiVu'.")
        return cast(ProjectType, value)

    @staticmethod
    def validate_project_status(value: str) -> ProjectStatus:
        if value not in ProjectStatus.__args__:
            raise ValueError(f"{value} is not a valid project status. Must be one of 'TimKiemUngVien', 'UngVienPhongVan', 'UngVienThuViec', 'TamNgung', 'Huy', or 'HoanThanh'.")
        return cast(ProjectStatus, value)

    @property
    def project_id(self) -> Optional[int]:
        return self._project_id
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def start_date(self) -> datetime.date:
        return self._start_date
    
    @property
    def end_date(self) -> datetime.date:
        return self._end_date
    
    @property
    def budget(self) -> float:
        return self._budget
    
    @property
    def budget_currency(self) -> str:
        return self._budget_currency
    
    @property
    def type(self) -> ProjectType:
        return self._type
    
    @property
    def required_recruits(self) -> int:
        return self._required_recruits
    
    @property
    def recruited(self) -> int:
        return self._recruited
    
    @property
    def status(self) -> ProjectStatus:
        return self._status
    
    @property
    def customer_id(self) -> int:
        return self._customer_id
    
    @property
    def expertise_id(self) -> int:
        return self._expertise_id
    
    @property
    def area_id(self) -> int:
        return self._area_id
    
    @property
    def level_id(self) -> int:
        return self._level_id

    def to_dict(self) -> dict[str, Any]:
        return {
            "project_id": self._project_id,
            "name": self._name,
            "start_date": self._start_date,
            "end_date": self._end_date,
            "budget": self._budget,
            "budget_currency": self._budget_currency,
            "type": self._type,
            "required_recruits": self._required_recruits,
            "recruited": self._recruited,
            "status": self._status,
            "customer_id": self._customer_id,
            "expertise_id": self._expertise_id,
            "area_id": self._area_id,
            "level_id": self._level_id
        }
    
    def __repr__(self) -> str:
        return (
            f"Project(project_id={self._project_id}, name={self._name}, "
            f"start_date={self._start_date}, end_date={self._end_date}, "
            f"budget={self._budget}, budget_currency={self._budget_currency}, type={self._type}, "
            f"required_recruits={self._required_recruits}, recruited={self._recruited}, "
            f"status={self._status}, customer_id={self._customer_id}, "
            f"expertise_id={self._expertise_id}, area_id={self._area_id}, level_id={self._level_id})"
        )