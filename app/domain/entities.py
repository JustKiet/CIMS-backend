from pydantic import BaseModel, StringConstraints
from typing import Literal, Annotated

class Candidate(BaseModel):
    candidate_id: Annotated[
        str, 
        StringConstraints(
            strip_whitespace=True,
            max_length=20,
            pattern=r'^[A-Za-z0-9_]+$'
        )
    ]
    name: Annotated[
        str,
        StringConstraints(
            strip_whitespace=True,
            max_length=40,
        )
    ]
    phone: Annotated[
        str,
        StringConstraints(
            strip_whitespace=True,
            max_length=15,
            pattern=r'^\+?[0-9\s]+$'
        )
    ]
    email: Annotated[
        str,
        StringConstraints(
            strip_whitespace=True,
            max_length=60,
            pattern=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        )
    ]
    year_of_birth: int
    gender: Literal["Nam", "Nu", "Khac"]
    education: Annotated[
        str,
        StringConstraints(
            strip_whitespace=True,
            max_length=255,
        )
    ]
    source: Annotated[
        str,
        StringConstraints(
            strip_whitespace=True,
            max_length=120,
        )
    ]
    expertise_id: Annotated[
        str, 
        StringConstraints(
            strip_whitespace=True,
            max_length=20,
            pattern=r'^[A-Za-z0-9_]+$'
        )
    ]
    field_id: Annotated[
        str, 
        StringConstraints(
            strip_whitespace=True,
            max_length=20,
            pattern=r'^[A-Za-z0-9_]+$'
        )
    ]
    area_id: Annotated[
        str, 
        StringConstraints(
            strip_whitespace=True,
            max_length=20,
            pattern=r'^[A-Za-z0-9_]+$'
        )
    ]
    level_id: Annotated[
        str, 
        StringConstraints(
            strip_whitespace=True,
            max_length=20,
            pattern=r'^[A-Za-z0-9_]+$'
        )
    ]
    hr_id: Annotated[
        str, 
        StringConstraints(
            strip_whitespace=True,
            max_length=20,
            pattern=r'^[A-Za-z0-9_]+$'
        )
    ]
    note: Annotated[
        str, 
        StringConstraints(
            strip_whitespace=True,
            max_length=60,
        )
    ]

class Project(BaseModel):
    project_id: Annotated[
        str, 
        StringConstraints(
            strip_whitespace=True,
            max_length=20,
            pattern=r'^[A-Za-z0-9_]+$'
        )
    ]
    name: Annotated[
        str, 
        StringConstraints(
            strip_whitespace=True,
            max_length=60,
        )
    ]
    start_date: int
    end_date: int
    budget: float
    type: Literal["CoDinh", "ThoiVu"]
    required_recruits: int
    recruited: int
    progress: Literal[
        "TimKiemUngVien", 
        "UngVienPhongVan", 
        "UngVienThuViec", 
        "TamNgung", 
        "Huy",
        "HoanThanh"
    ]
    expertise_id: Annotated[
        str, 
        StringConstraints(
            strip_whitespace=True,
            max_length=20,
            pattern=r'^[A-Za-z0-9_]+$'
        )
    ]
    area_id: Annotated[
        str, 
        StringConstraints(
            strip_whitespace=True,
            max_length=20,
            pattern=r'^[A-Za-z0-9_]+$'
        )
    ]
    level_id: Annotated[
        str, 
        StringConstraints(
            strip_whitespace=True,
            max_length=20,
            pattern=r'^[A-Za-z0-9_]+$'
        )
    ]

class Nominee(BaseModel):
    nominee_id: Annotated[
        str, 
        StringConstraints(
            strip_whitespace=True,
            max_length=20,
            pattern=r'^[A-Za-z0-9_]+$'
        )
    ]
    campaign: Annotated[
        str, 
        StringConstraints(
            strip_whitespace=True,
            max_length=40,
        )
    ]
    years_of_experience: int
    salary_expectation: float
    notice_period: int
    candidate_id: Annotated[
        str, 
        StringConstraints(
            strip_whitespace=True,
            max_length=20,
            pattern=r'^[A-Za-z0-9_]+$'
        )
    ]
    project_id: Annotated[
        str, 
        StringConstraints(
            strip_whitespace=True,
            max_length=20,
            pattern=r'^[A-Za-z0-9_]+$'
        )
    ]

class Customer(BaseModel):
    customer_id: Annotated[
        str, 
        StringConstraints(
            strip_whitespace=True,
            max_length=20,
            pattern=r'^[A-Za-z0-9_]+$'
        )
    ]
    name: Annotated[
        str, 
        StringConstraints(
            strip_whitespace=True,
            max_length=60,
        )
    ]
    field_id: Annotated[
        str, 
        StringConstraints(
            strip_whitespace=True,
            max_length=20,
            pattern=r'^[A-Za-z0-9_]+$'
        )
    ]

class HR(BaseModel):
    hr_id: Annotated[
        str, 
        StringConstraints(
            strip_whitespace=True,
            max_length=20,
            pattern=r'^[A-Za-z0-9_]+$'
        )
    ]
    name: Annotated[
        str, 
        StringConstraints(
            strip_whitespace=True,
            max_length=40,
        )
    ]
    phone: Annotated[
        str, 
        StringConstraints(
            strip_whitespace=True,
            max_length=15,
            pattern=r'^\+?[0-9\s]+$'
        )
    ]
    email: Annotated[
        str, 
        StringConstraints(
            strip_whitespace=True,
            max_length=60,
            pattern=r'^[A-Za-z0-9_]+$'
        )
    ]
    role: Annotated[
        str, 
        StringConstraints(
            strip_whitespace=True,
            max_length=40,
        )
    ]
    area_id: Annotated[
        str, 
        StringConstraints(
            strip_whitespace=True,
            max_length=20,
            pattern=r'^[A-Za-z0-9_]+$'
        )
    ]

class Level(BaseModel):
    level_id: Annotated[
        str, 
        StringConstraints(
            strip_whitespace=True,
            max_length=20,
            pattern=r'^[A-Za-z0-9_]+$'
        )
    ]
    name: Annotated[
        str, 
        StringConstraints(
            strip_whitespace=True,
            max_length=40,
        )
    ]

class Expertise(BaseModel):
    expertise_id: Annotated[
        str, 
        StringConstraints(
            strip_whitespace=True,
            max_length=20,
            pattern=r'^[A-Za-z0-9_]+$'
        )
    ]
    name: Annotated[
        str, 
        StringConstraints(
            strip_whitespace=True,
            max_length=40,
        )
    ]

class Field(BaseModel):
    field_id: Annotated[
        str, 
        StringConstraints(
            strip_whitespace=True,
            max_length=20,
            pattern=r'^[A-Za-z0-9_]+$'
        )
    ]
    name: Annotated[
        str, 
        StringConstraints(
            strip_whitespace=True,
            max_length=40,
        )
    ]

class Area(BaseModel):
    area_id: Annotated[
        str, 
        StringConstraints(
            strip_whitespace=True,
            max_length=20,
            pattern=r'^[A-Za-z0-9_]+$'
        )
    ]
    name: Annotated[
        str, 
        StringConstraints(
            strip_whitespace=True,
            max_length=40,
        )
    ]