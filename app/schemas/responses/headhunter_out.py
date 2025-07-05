from pydantic import BaseModel, EmailStr

class HeadhunterOut(BaseModel):
    headhunter_id: int
    name: str
    phone: str
    email: EmailStr
    area_id: int
    role: str = "headhunter"