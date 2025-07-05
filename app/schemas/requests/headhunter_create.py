from pydantic import BaseModel, EmailStr

class HeadhunterCreate(BaseModel):
    name: str
    phone: str
    email: EmailStr
    password: str
    area_id: int
    role: str = "headhunter"
