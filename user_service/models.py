from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    student_id: Optional[str] = None
    role: str = "Student"
    password: str

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    student_id: Optional[str] = None
    role: Optional[str] = None

class UserResponse(BaseModel):
    id: str
    full_name: str
    email: str
    student_id: Optional[str] = None
    role: str